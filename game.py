# /game.py
import pygame
import sys
from typing import List, Tuple, Optional
import os # Needed for joining sound paths
import copy # For copying hands in multi-poker

import constants
from card import Card
from deck import Deck
from game_state import GameState
from poker_rules import evaluate_hand, HandRank
from renderer import Renderer
from input_handler import InputHandler

# Dummy Sound class for when sound system fails or is disabled
class DummySound:
    def play(self): pass


class Game:
    """Manages the main game loop and coordinates components."""

    def __init__(self):
        """Initializes Pygame, game components, and game state."""
        pygame.init()
        try:
            pygame.mixer.init()
            self.sound_enabled = True
            print("Sound system initialized.")
        except pygame.error as e:
            print(f"Warning: Failed to initialize sound system: {e}")
            print("Game will run without sound.")
            self.sound_enabled = False
            # Set dummy sound objects later to avoid errors on play() calls

        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Video Poker")
        self.clock = pygame.time.Clock()

        # Game Components
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler()
        self.game_state_manager = GameState(starting_money=10)
        self.deck = Deck()

        # Load sounds
        self._load_sounds()

        # Game State Variables
        self.current_state = constants.STATE_MAIN_MENU
        self.hand: List[Card] = []
        self.multi_hands: List[List[Card]] = [] # For multi-poker results
        self.multi_results: List[Tuple[HandRank, str, int]] = [] # Results for each multi-hand
        self.held_indices: List[int] = []
        self.message = "" # No message on main menu initially
        self.result_message = ""
        self.total_winnings = 0 # Track total winnings across multi-hands
        self.final_hand_rank: Optional[HandRank] = None # Store the rank enum/constant of the final hand

        # Money animation state
        self.money_animation_active = False
        self.money_animation_timer = 0
        self.money_animation_amount = 0

        self.running = True

    def _load_sounds(self):
        """Loads sound effects from files."""
        self.sounds = {}
        # Ensure all expected sound keys exist, even if sound is disabled or files are missing
        if not self.sound_enabled:
            for name in constants.SOUND_FILES.keys():
                self.sounds[name] = DummySound()
            print("Sound disabled. Using dummy sound objects.")
            return

        for name, filename in constants.SOUND_FILES.items():
            path = os.path.join(constants.SOUND_ASSET_PATH, filename)
            try:
                sound = pygame.mixer.Sound(path)
                self.sounds[name] = sound
                print(f"Loaded sound: {name} ({filename})")
            except pygame.error as e:
                print(f"Warning: Could not load sound '{filename}': {e}")
                # Assign a dummy sound object for this specific sound
                self.sounds[name] = DummySound()

    def _reset_game_variables(self):
        """Resets variables needed for starting a new game or returning to menu."""
        self.hand = []
        self.multi_hands = []
        self.multi_results = []
        self.held_indices = []
        self.message = ""
        self.result_message = ""
        self.final_hand_rank = None
        self.total_winnings = 0
        self.money_animation_active = False
        self.money_animation_timer = 0
        self.money_animation_amount = 0
        # Don't reset game_state_manager.money here

    def _start_draw_poker_round(self):
        """Starts a new round of standard Draw Poker."""
        self.game_state_manager.set_cost_per_game(1) # Ensure cost is 1
        if self.game_state_manager.start_game():
            self._reset_game_variables() # Reset common variables
            self.deck = Deck() # Get a fresh shuffled deck
            self.hand = self.deck.deal(5)
            self.message = "Click HOLD buttons, then click DRAW"
            self.current_state = constants.STATE_DRAW_POKER_WAITING_FOR_HOLD
            self.sounds["deal"].play() # Play deal sound
        else:
            self._reset_game_variables() # Reset variables even if game over
            self.message = "GAME OVER! Not enough money."
            self.result_message = ""
            self.current_state = constants.STATE_GAME_OVER

    def _start_multi_poker_round(self):
        """Starts a new round of Multi Poker."""
        self.game_state_manager.set_cost_per_game(constants.NUM_MULTI_HANDS) # Set cost for N hands
        if self.game_state_manager.start_game():
            self._reset_game_variables()
            self.deck = Deck() # Fresh deck for the initial deal
            self.hand = self.deck.deal(5) # Deal the base hand
            self.message = f"Click HOLD buttons (Cost: {constants.NUM_MULTI_HANDS}), then click DRAW"
            self.current_state = constants.STATE_MULTI_POKER_WAITING_FOR_HOLD
            self.sounds["deal"].play()
        else:
            self._reset_game_variables()
            self.message = f"GAME OVER! Need ${constants.NUM_MULTI_HANDS} to play Multi Poker."
            self.current_state = constants.STATE_GAME_OVER

    def _process_drawing(self):
        """Handles the logic for drawing new cards."""
        cards_to_draw = 5 - len(self.held_indices)
        new_hand: List[Optional[Card]] = [None] * 5 # Placeholder for the new hand

        # Keep held cards
        for i in self.held_indices:
            new_hand[i] = self.hand[i]

        # Get new cards for non-held positions
        try:
            new_cards = self.deck.deal(cards_to_draw)
        except IndexError:
             print("Error: Not enough cards left in deck to draw. This shouldn't happen in standard poker.")
             # Handle this case gracefully - maybe reshuffle discard pile if implementing that?
             # For now, might just end the round or show an error.
             self.message = "Deck error! Please restart."
             self.current_state = constants.STATE_GAME_OVER # Or another error state
             return

        # Place new cards into the empty slots
        new_card_idx = 0
        for i in range(5):
            if new_hand[i] is None: # If this position needs a new card
                if new_card_idx < len(new_cards):
                    new_hand[i] = new_cards[new_card_idx]
                    new_card_idx += 1
                else:
                    # This indicates a logic error if reached
                    print(f"Error: Mismatch drawing cards. Needed card for index {i}, but ran out of new cards.")
                    self.message = "Card drawing error!"
                    self.current_state = constants.STATE_GAME_OVER
                    return

        # Ensure the hand is fully reconstructed
        if None in new_hand:
            print("Error: Final hand reconstruction failed. Hand contains None.")
            self.message = "Hand reconstruction error!"
            self.current_state = constants.STATE_GAME_OVER
            return

        # Explicitly cast List[Optional[Card]] to List[Card] after checks
        self.hand = [card for card in new_hand if card is not None] # Should be safe now

        # Evaluate the final hand
        rank, hand_name, payout = evaluate_hand(self.hand)
        self.final_hand_rank = rank # Store the actual rank

        if payout > 0:
            winnings = payout * 1 # Payout is based on a 1-unit bet
            self.result_message = f"WINNER! {hand_name}! +${winnings}"
            self.sounds["win"].play() # Play win sound
            self.game_state_manager.add_winnings(winnings)
            # Trigger money animation
            self.money_animation_active = True
            self.money_animation_amount = winnings
            self.money_animation_timer = constants.MONEY_ANIMATION_DURATION
        else:
            self.result_message = f"Result: {hand_name}. No win."
            self.sounds["lose"].play() # Play lose sound

        self.sounds["draw"].play() # Play draw sound (after cards are replaced)
        self.message = "" # Clear the action message
        self.current_state = constants.STATE_DRAW_POKER_SHOWING_RESULT

    def _process_multi_drawing(self):
        """Handles drawing cards for multiple hands in Multi Poker."""
        num_hands = constants.NUM_MULTI_HANDS
        self.multi_hands = []
        self.multi_results = []
        self.total_winnings = 0

        # Create separate decks for each hand draw (excluding the base hand's deck)
        # Each new deck should be a standard 52-card deck.
        draw_decks = [Deck() for _ in range(num_hands)]

        # The base hand (self.hand) was dealt from self.deck.
        # The subsequent draws for each of the N hands will use the new decks.

        held_cards = {i: self.hand[i] for i in self.held_indices}

        for i in range(num_hands):
            current_hand = [None] * 5
            # Place held cards
            for index, card in held_cards.items():
                current_hand[index] = card

            # Determine cards needed
            cards_to_draw = 5 - len(held_cards)

            # Deal new cards from the corresponding draw deck
            try:
                # Ensure dealt cards don't conflict with held cards (though unlikely with fresh decks)
                new_cards = []
                deck_for_draw = draw_decks[i]
                attempts = 0
                while len(new_cards) < cards_to_draw and attempts < 100 and len(deck_for_draw) > 0:
                    potential_card = deck_for_draw.deal(1)[0]
                    # Check if this card (rank and suit) is already held
                    is_held = any(potential_card == held_card for held_card in held_cards.values())
                    if not is_held:
                         # Also check if it's already been drawn for *this specific hand*
                         is_drawn_for_this_hand = any(potential_card == drawn_card for drawn_card in new_cards)
                         if not is_drawn_for_this_hand:
                             new_cards.append(potential_card)
                    attempts += 1 # Prevent infinite loops in edge cases

                if len(new_cards) < cards_to_draw:
                     raise IndexError(f"Could not deal enough unique cards for hand {i+1}")

            except IndexError as e:
                print(f"Error dealing for multi-hand {i+1}: {e}")
                self.message = "Deck error during multi-draw!"
                self.current_state = constants.STATE_GAME_OVER # Or error state
                return

            # Place new cards
            new_card_idx = 0
            for j in range(5):
                if current_hand[j] is None:
                    current_hand[j] = new_cards[new_card_idx]
                    new_card_idx += 1

            final_hand = [card for card in current_hand if card is not None]
            if len(final_hand) != 5:
                 print(f"Error: Multi-hand {i+1} reconstruction failed.")
                 self.message = "Multi-hand reconstruction error!"
                 self.current_state = constants.STATE_GAME_OVER
                 return

            # Evaluate this hand
            rank, name, payout = evaluate_hand(final_hand)
            self.multi_hands.append(final_hand)
            self.multi_results.append((rank, name, payout))
            self.total_winnings += payout # Payout is per unit bet (1)

        # Update game state
        if self.total_winnings > 0:
            self.result_message = f"WINNER! Total: +${self.total_winnings}"
            self.sounds["win"].play()
            self.game_state_manager.add_winnings(self.total_winnings)
            # Trigger money animation for total amount
            self.money_animation_active = True
            self.money_animation_amount = self.total_winnings
            self.money_animation_timer = constants.MONEY_ANIMATION_DURATION
        else:
            self.result_message = "No winning hands."
            self.sounds["lose"].play()

        self.sounds["draw"].play() # Play draw sound once after all hands are set
        self.message = "" # Clear action message
        self.current_state = constants.STATE_MULTI_POKER_SHOWING_RESULT

    def _process_input(self, actions: List[Tuple[str, Optional[any]]]):
        """Processes actions received from the InputHandler."""
        for action, payload in actions:
            if action == constants.ACTION_QUIT:
                self.running = False
                self.sounds["button"].play() # Optional: sound on quit
                break # Exit loop immediately on quit

            elif action == constants.ACTION_CHOOSE_DRAW_POKER:
                self.sounds["button"].play()
                if self.current_state == constants.STATE_MAIN_MENU:
                    self._start_draw_poker_round() # Start the first round

            elif action == constants.ACTION_CHOOSE_MULTI_POKER:
                self.sounds["button"].play()
                if self.current_state == constants.STATE_MAIN_MENU:
                    self._start_multi_poker_round()

            elif action == constants.ACTION_RETURN_TO_MENU:
                self.sounds["button"].play()
                self._reset_game_variables()
                self.message = "" # Clear any lingering game messages
                self.current_state = constants.STATE_MAIN_MENU

            elif action == constants.ACTION_DEAL_DRAW:
                self.sounds["button"].play()
                # Deal/Draw button now only works in specific game states
                if self.current_state == constants.STATE_DRAW_POKER_WAITING_FOR_HOLD:
                    self._process_drawing()
                elif self.current_state == constants.STATE_MULTI_POKER_WAITING_FOR_HOLD:
                    self._process_multi_drawing()
                elif self.current_state == constants.STATE_DRAW_POKER_SHOWING_RESULT:
                    self._start_draw_poker_round() # Start next game if possible
                    # Deal sound is played inside _start_new_round
                elif self.current_state == constants.STATE_MULTI_POKER_SHOWING_RESULT:
                    self._start_multi_poker_round() # Start next multi-poker game

            elif action == constants.ACTION_HOLD_TOGGLE:
                if self.current_state in [constants.STATE_DRAW_POKER_WAITING_FOR_HOLD, constants.STATE_MULTI_POKER_WAITING_FOR_HOLD]:
                    index = payload
                    if index is not None:
                        if index in self.held_indices:
                            self.held_indices.remove(index)
                            self.sounds["hold"].play() # Play un-hold sound (same sound for hold/unhold)
                        else:
                            self.held_indices.append(index)
                            self.held_indices.sort() # Keep sorted for consistency
                            self.sounds["hold"].play() # Play hold sound

            elif action == constants.ACTION_PLAY_AGAIN:
                 if self.current_state == constants.STATE_GAME_OVER:
                     self.sounds["button"].play()
                Okay, here's the continuation of the updated `game.py` file:

/game.py

import pygame
import sys
from typing import List, Tuple, Optional
import os # Needed for joining sound paths

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
        self.held_indices: List[int] = []
        self.message = "" # No message on main menu initially
        self.result_message = ""
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
        self.held_indices = []
        self.message = ""
        self.result_message = ""
        self.final_hand_rank = None
        self.money_animation_active = False
        self.money_animation_timer = 0
        self.money_animation_amount = 0
        # Don't reset game_state_manager.money here

    def _start_draw_poker_round(self):
        """Resets variables for a new round of play."""
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
            winnings = payout * self.game_state_manager.cost_per_game
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
                elif self.current_state == constants.STATE_DRAW_POKER_SHOWING_RESULT:
                    self._start_draw_poker_round() # Start next game if possible
                    # Deal sound is played inside _start_new_round

            elif action == constants.ACTION_HOLD_TOGGLE:
                if self.current_state == constants.STATE_DRAW_POKER_WAITING_FOR_HOLD:
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
                     # Reset game state completely
                     self.game_state_manager = GameState(starting_money=10) # Or original starting money
                     self._reset_game_variables()
                     self.message = "" # No message on main menu
                     self.current_state = constants.STATE_MAIN_MENU

    def _update(self):
        """Handles game logic updates, like animations."""
        # Update money animation timer
        if self.money_animation_active:
            self.money_animation_timer -= 1
            if self.money_animation_timer <= 0:
                self.money_animation_active = False
                self.money_animation_amount = 0 # Reset amount

    def _render(self):
        """Draws the current game state to the screen."""
        # Check if we are in the main menu state
        if self.current_state == constants.STATE_MAIN_MENU:
            self.renderer.draw_main_menu()
            pygame.display.flip()
            return # Don't draw the rest of the game screen

        game_data = {
            "money": self.game_state_manager.money,
            "can_play": self.game_state_manager.can_play(),
            "hand": self.hand,
            "held_indices": self.held_indices,
            "message": self.message,
            "result_message": self.result_message,
            "current_state": self.current_state,
            "winning_rank": self.final_hand_rank, # Pass the winning rank
            # Pass animation state
            "money_animation_active": self.money_animation_active,
            "money_animation_amount": self.money_animation_amount,
        }
        self.renderer.draw_game_screen(game_data)
        pygame.display.flip() # Update the full screen

    def run(self):
        """The main game loop."""
        while self.running:
            # 1. Handle Input
            actions = self.input_handler.handle_events(self.current_state)

            # 2. Process Input & Update Game State
            self._process_input(actions)

            # 3. Update Game Logic (if any time-based updates needed)
            self._update()

            # 4. Render Output
            self._render()

            # 5. Control Frame Rate
            self.clock.tick(30) # Limit FPS to 30

        # Cleanup
        pygame.quit()
        sys.exit()

import pygame
import sys
from typing import List, Tuple, Optional

import constants
from card import Card
from deck import Deck
from game_state import GameState
from poker_rules import evaluate_hand
from renderer import Renderer
from input_handler import InputHandler

class Game:
    """Manages the main game loop and coordinates components."""

    def __init__(self):
        """Initializes Pygame, game components, and game state."""
        pygame.init()
        # Consider adding error handling for pygame initialization if needed
        # pygame.mixer.init() # Uncomment if adding sounds

        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Video Poker")
        self.clock = pygame.time.Clock()

        # Game Components
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler()
        self.game_state_manager = GameState(starting_money=10)
        self.deck = Deck()

        # Game State Variables
        self.current_state = constants.STATE_START_MENU
        self.hand: List[Card] = []
        self.held_indices: List[int] = []
        self.message = "Welcome! Click DEAL to start."
        self.result_message = ""
        self.final_hand_rank_name = "" # Store the name of the final hand

        self.running = True

    def _start_new_round(self):
        """Resets variables for a new round of play."""
        if self.game_state_manager.start_game():
            self.deck = Deck() # Get a fresh shuffled deck
            self.hand = self.deck.deal(5)
            self.held_indices = []
            self.message = "Click HOLD buttons, then click DRAW"
            self.result_message = ""
            self.final_hand_rank_name = ""
            self.current_state = constants.STATE_WAITING_FOR_HOLD
        else:
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
        self.final_hand_rank_name = hand_name # Store for display

        if payout > 0:
            winnings = payout * self.game_state_manager.cost_per_game
            self.result_message = f"WINNER! {hand_name}! +${winnings}"
            self.game_state_manager.add_winnings(winnings)
            # Play win sound (optional)
        else:
            self.result_message = f"Result: {hand_name}. No win."
            # Play lose sound (optional)

        self.message = "" # Clear the action message
        self.current_state = constants.STATE_SHOWING_RESULT

    def _process_input(self, actions: List[Tuple[str, Optional[any]]]):
        """Processes actions received from the InputHandler."""
        for action, payload in actions:
            if action == constants.ACTION_QUIT:
                self.running = False
                break # Exit loop immediately on quit

            elif action == constants.ACTION_DEAL_DRAW:
                if self.current_state == constants.STATE_START_MENU:
                    self._start_new_round()
                elif self.current_state == constants.STATE_WAITING_FOR_HOLD:
                    self._process_drawing()
                elif self.current_state == constants.STATE_SHOWING_RESULT:
                    self._start_new_round() # Start next game if possible

            elif action == constants.ACTION_HOLD_TOGGLE:
                if self.current_state == constants.STATE_WAITING_FOR_HOLD:
                    index = payload
                    if index is not None:
                        if index in self.held_indices:
                            self.held_indices.remove(index)
                            # Play un-hold sound (optional)
                        else:
                            self.held_indices.append(index)
                            self.held_indices.sort() # Keep sorted for consistency
                            # Play hold sound (optional)

            elif action == constants.ACTION_PLAY_AGAIN:
                 if self.current_state == constants.STATE_GAME_OVER:
                     # Reset game state completely
                     self.game_state_manager = GameState(starting_money=10) # Or original starting money
                     self.hand = []
                     self.held_indices = []
                     self.message = "Welcome! Click DEAL to start."
                     self.result_message = ""
                     self.final_hand_rank_name = ""
                     self.current_state = constants.STATE_START_MENU

    def _update(self):
        """Handles game logic updates (currently handled within _process_input)."""
        # This method could be used for animations or time-based events later.
        pass

    def _render(self):
        """Draws the current game state to the screen."""
        game_data = {
            "money": self.game_state_manager.money,
            "can_play": self.game_state_manager.can_play(),
            "hand": self.hand,
            "held_indices": self.held_indices,
            "message": self.message,
            "result_message": self.result_message,
            "current_state": self.current_state,
            # Add final_hand_rank_name if needed for display by renderer
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

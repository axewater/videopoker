from typing import Dict, Any

import constants
from deck import Deck
from game_state import GameState
from .reset_game_variables import reset_game_variables

def start_draw_poker_round(game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Starts a new round of standard Draw Poker.
    Returns a dictionary of the updated game state variables.
    """
    game_state_manager.set_cost_per_game(1) # Ensure cost is 1
    if game_state_manager.start_game():
        updated_state = reset_game_variables() # Get reset variables
        deck = Deck() # Get a fresh shuffled deck
        updated_state['hand'] = deck.deal(5)
        updated_state['deck'] = deck # Store the deck in the state
        updated_state['message'] = "Click HOLD buttons, then click DRAW"
        updated_state['current_state'] = constants.STATE_DRAW_POKER_WAITING_FOR_HOLD
        sounds["deal"].play() # Play deal sound
        return updated_state
    else:
        # Game Over state
        updated_state = reset_game_variables()
        updated_state['message'] = "GAME OVER! Not enough money."
        updated_state['result_message'] = ""
        updated_state['current_state'] = constants.STATE_GAME_OVER
        updated_state['deck'] = Deck() # Still provide a deck object
        return updated_state

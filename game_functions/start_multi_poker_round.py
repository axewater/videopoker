from typing import Dict, Any

import config_layout_cards as layout_cards
import config_states as states
from deck import Deck
from game_state import GameState
from .reset_game_variables import reset_game_variables

def start_multi_poker_round(game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Starts a new round of Multi Poker.
    Returns a dictionary of the updated game state variables.
    """
    cost = layout_cards.NUM_MULTI_HANDS
    game_state_manager.set_cost_per_game(cost) # Set cost for N hands
    if game_state_manager.start_fixed_cost_game(): 
        updated_state = reset_game_variables()
        deck = Deck() # Fresh deck for the initial deal
        updated_state['hand'] = deck.deal(5) # Deal the base hand
        updated_state['deck'] = deck # Store the deck
        updated_state['message'] = f"Click HOLD buttons (Cost: {cost}), then click DRAW"
        updated_state['current_state'] = states.STATE_MULTI_POKER_WAITING_FOR_HOLD
        if sounds.get("deal"):
            sounds["deal"].play()
        return updated_state
    else:
        # Game Over state
        updated_state = reset_game_variables()
        updated_state['message'] = f"GAME OVER! Need ${cost} to play Multi Poker."
        updated_state['current_state'] = states.STATE_GAME_OVER
        updated_state['deck'] = Deck() # Provide deck object
        return updated_state

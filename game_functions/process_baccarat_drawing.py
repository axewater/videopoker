# /game_functions/process_baccarat_drawing.py
"""
Handles the logic for drawing the third card for Player and Banker in Baccarat.
"""
from typing import Dict, Any, Optional

import config_states as states
from deck import Deck
from card import Card
from baccarat_rules import should_player_draw, should_banker_draw

def process_baccarat_drawing(current_game_state: Dict[str, Any], sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applies the third-card drawing rules for Player and Banker.
    Assumes initial deal is done and no Naturals occurred.
    Returns a dictionary of the updated game state variables, ready for resolution.
    """
    new_state = current_game_state.copy()
    player_hand: list[Card] = new_state.get('baccarat_player_hand', [])
    banker_hand: list[Card] = new_state.get('baccarat_banker_hand', [])
    deck: Optional[Deck] = new_state.get('deck')

    if not deck or len(player_hand) != 2 or len(banker_hand) != 2:
        print("Error: Invalid state for Baccarat drawing phase.")
        new_state['message'] = "Error during drawing phase."
        new_state['current_state'] = states.STATE_BACCARAT_BETTING # Go back to betting
        return new_state

    player_third_card: Optional[Card] = None

    # 1. Player's Draw
    if should_player_draw(player_hand):
        try:
            player_third_card = deck.deal(1)[0]
            player_hand.append(player_third_card)
            new_state['baccarat_player_hand'] = player_hand
            if sounds.get("draw"): sounds["draw"].play() # Play draw sound
            new_state['message'] = "Player draws. Checking Banker..."
        except IndexError:
            print("Error: Deck empty when Player needed to draw.")
            new_state['message'] = "Deck empty error!"
            new_state['current_state'] = states.STATE_GAME_OVER
            return new_state
    else:
        new_state['message'] = "Player stands. Checking Banker..."

    # 2. Banker's Draw (depends on Player's action)
    if should_banker_draw(banker_hand, player_third_card):
        try:
            banker_third_card = deck.deal(1)[0]
            banker_hand.append(banker_third_card)
            new_state['baccarat_banker_hand'] = banker_hand
            if sounds.get("draw"): sounds["draw"].play() # Play draw sound
            new_state['message'] = "Banker draws. Resolving..."
        except IndexError:
            print("Error: Deck empty when Banker needed to draw.")
            new_state['message'] = "Deck empty error!"
            new_state['current_state'] = states.STATE_GAME_OVER
            return new_state
    elif player_third_card is not None: # Only say Banker stands if Player drew
         new_state['message'] = "Banker stands. Resolving..."
    else: # Player stood, Banker stood
         new_state['message'] = "Both stand. Resolving..."

    # 3. Update Deck and Prepare for Resolution
    new_state['deck'] = deck
    # The actual resolution (comparing hands, calculating payout) happens in resolve_baccarat_round
    # We transition to the RESULT state implicitly by returning, and update_game will call resolve.
    return new_state

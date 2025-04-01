from typing import Dict, Any

import config_actions as actions
import config_states as states
from deck import Deck
from game_state import GameState
from blackjack_rules import get_hand_value, is_busted
from .resolve_blackjack_round import resolve_blackjack_round # Import resolve function

def process_blackjack_action(action: str, current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles player actions (Hit, Stand) during their turn in Blackjack.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()
    player_hand = new_state.get('player_hand', [])
    deck = new_state.get('deck')

    if action == actions.ACTION_BLACKJACK_HIT:
        if deck and len(deck) > 0:
            # Deal one card to player
            player_hand.extend(deck.deal(1))
            new_state['player_hand'] = player_hand
            if sounds.get("draw"): sounds["draw"].play() # Use draw sound for hit

            # Check for bust
            if is_busted(player_hand):
                if sounds.get("lose"): sounds["lose"].play()
                # Player busts, resolve the round immediately (player loses)
                # Pass the current state to resolve function
                resolve_state = resolve_blackjack_round(new_state, game_state_manager, sounds)
                new_state.update(resolve_state) # Update state with resolution results
            else:
                # Still player's turn, update message if needed
                new_state['message'] = "Hit or Stand?"
                new_state['current_state'] = states.STATE_BLACKJACK_PLAYER_TURN # Remain in player turn
        else:
            new_state['message'] = "Deck empty error!"
            new_state['current_state'] = states.STATE_GAME_OVER # Error state

    elif action == actions.ACTION_BLACKJACK_STAND:
        if sounds.get("button"): sounds["button"].play() # Sound for clicking stand
        # Player stands, move to dealer's turn and resolve the round
        new_state['message'] = "Dealer's Turn..."
        # Resolve function handles dealer's play and determines winner
        resolve_state = resolve_blackjack_round(new_state, game_state_manager, sounds)
        new_state.update(resolve_state) # Update state with resolution results

    return new_state

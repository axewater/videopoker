# /game_functions/handle_blackjack_input.py
from typing import Dict, Any, Optional, Tuple

import config_states as states
import config_actions as actions_cfg
from game_state import GameState
from .start_blackjack_round import start_blackjack_round
from .process_blackjack_action import process_blackjack_action
from .reset_game_variables import reset_game_variables

def handle_blackjack_action(action: str, payload: Optional[any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """Handles input actions for Blackjack states."""
    new_game_state = current_game_state.copy()
    current_state_str = new_game_state['current_state']

    # --- Return to Menu (Needs Confirmation Check) ---
    if action == actions_cfg.ACTION_RETURN_TO_MENU:
        if current_state_str == states.STATE_BLACKJACK_PLAYER_TURN:
            if sounds.get("button"): sounds["button"].play()
            # Trigger confirmation
            new_game_state['confirm_action_type'] = 'EXIT'
            new_game_state['confirm_exit_destination'] = states.STATE_GAME_SELECTION
            new_game_state['previous_state_before_confirm'] = current_state_str
            new_game_state['current_state'] = states.STATE_CONFIRM_EXIT
        elif current_state_str in [states.STATE_BLACKJACK_IDLE, states.STATE_BLACKJACK_SHOWING_RESULT]:
            # Allow direct exit from idle/result states
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['player_hand'] = [] # Clear blackjack specific state
            new_game_state['dealer_hand'] = []
            new_game_state['message'] = ""
            new_game_state['current_state'] = states.STATE_GAME_SELECTION
        return new_game_state # Return early after handling menu action

    # --- Deal Action (from Idle or Result) ---
    if action == actions_cfg.ACTION_DEAL_DRAW: # Reusing DEAL_DRAW for Blackjack Deal
        if current_state_str == states.STATE_BLACKJACK_IDLE:
            if sounds.get("button"): sounds["button"].play()
            round_state = start_blackjack_round(game_state_manager, sounds)
            new_game_state.update(round_state)
        elif current_state_str == states.STATE_BLACKJACK_SHOWING_RESULT:
            if sounds.get("button"): sounds["button"].play()
            if game_state_manager.can_afford_bet(1):
                round_state = start_blackjack_round(game_state_manager, sounds)
                new_game_state.update(round_state)
            else:
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['message'] = "GAME OVER! Not enough money for Blackjack."
                new_game_state['current_state'] = states.STATE_GAME_OVER

    # --- Hit/Stand Actions (Player Turn) ---
    elif action == actions_cfg.ACTION_BLACKJACK_HIT or action == actions_cfg.ACTION_BLACKJACK_STAND:
        if current_state_str == states.STATE_BLACKJACK_PLAYER_TURN:
            action_result_state = process_blackjack_action(action, new_game_state, game_state_manager, sounds)
            new_game_state.update(action_result_state)

    return new_game_state

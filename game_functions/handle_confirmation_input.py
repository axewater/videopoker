# /game_functions/handle_confirmation_input.py
from typing import Dict, Any, Optional, Tuple

import config_states as states
import config_actions as actions_cfg
from game_state import GameState
from .reset_game_variables import reset_game_variables

def handle_confirmation_action(action: str, payload: Optional[any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """Handles input actions for the Confirmation Dialog state."""
    new_game_state = current_game_state.copy()

    if new_game_state['current_state'] != states.STATE_CONFIRM_EXIT:
        return new_game_state # Should not happen, but safety check

    if action == actions_cfg.ACTION_CONFIRM_YES:
        if sounds.get("button"): sounds["button"].play()
        action_type = new_game_state.get('confirm_action_type')

        if action_type == 'QUIT':
            # Signal main loop to exit by setting 'running' to False
            new_game_state['running'] = False
            # No need to change state, loop will terminate

        elif action_type == 'RESTART':
            # Set flag for main loop to reset money and return to game selection
            new_game_state['needs_money_reset'] = True
            new_game_state['current_state'] = states.STATE_GAME_SELECTION
            # Clear confirmation flags
            new_game_state['confirm_action_type'] = None
            new_game_state['previous_state_before_confirm'] = None

        else: # Default to 'EXIT' action (Exit to Game Menu)
            destination_state = new_game_state.get('confirm_exit_destination', states.STATE_GAME_SELECTION)
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            # Clear potential game-specific state (redundant with reset, but safe)
            new_game_state['player_hand'] = []
            new_game_state['dealer_hand'] = []
            new_game_state['multi_hands'] = []
            new_game_state['multi_results'] = []
            new_game_state['roulette_bets'] = {}
            new_game_state['message'] = ""
            new_game_state['current_state'] = destination_state
            # Clear confirmation flags
            new_game_state['confirm_action_type'] = None
            new_game_state['confirm_exit_destination'] = None
            new_game_state['previous_state_before_confirm'] = None

    elif action == actions_cfg.ACTION_CONFIRM_NO:
        if sounds.get("button"): sounds["button"].play()
        previous_state = new_game_state.get('previous_state_before_confirm')
        if previous_state:
            new_game_state['current_state'] = previous_state
        else:
            # Fallback if previous state wasn't stored correctly
            new_game_state['current_state'] = states.STATE_GAME_SELECTION # Sensible default
        # Clear confirmation flags
        new_game_state['confirm_action_type'] = None
        new_game_state['confirm_exit_destination'] = None
        new_game_state['previous_state_before_confirm'] = None

    return new_game_state

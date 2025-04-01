# /game_functions/handle_slots_input.py
# NEW FILE
from typing import Dict, Any, Optional, Tuple

import config_states as states
import config_actions as actions_cfg
from game_state import GameState
from .process_slots_spin import process_slots_spin
from .reset_game_variables import reset_game_variables

def handle_slots_action(action: str, payload: Optional[any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """Handles input actions for Slots states."""
    new_game_state = current_game_state.copy()
    current_state_str = new_game_state['current_state']

    # --- Return to Menu (No confirmation needed for Slots) ---
    if action == actions_cfg.ACTION_RETURN_TO_MENU:
        if current_state_str != states.STATE_SLOTS_SPINNING: # Allow exit unless actively spinning
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            # Clear slots specific state if needed (reset does most)
            new_game_state['message'] = ""
            new_game_state['current_state'] = states.STATE_GAME_SELECTION
        else:
            new_game_state['message'] = "Cannot exit while reels are spinning!"
            # Keep current state
        return new_game_state # Return early after handling menu action

    # --- Spin Action ---
    if action == actions_cfg.ACTION_SLOTS_SPIN:
        if current_state_str in [states.STATE_SLOTS_IDLE, states.STATE_SLOTS_SHOWING_RESULT]:
            spin_result_state = process_slots_spin(new_game_state, game_state_manager, sounds)
            new_game_state.update(spin_result_state)

    return new_game_state

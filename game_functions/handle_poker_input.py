# /game_functions/handle_poker_input.py
# NEW FILE
from typing import Dict, Any, Optional, Tuple

import config_states as states
import config_actions as actions_cfg
import config_layout_cards as layout_cards # For NUM_MULTI_HANDS cost check
from game_state import GameState
from .start_draw_poker_round import start_draw_poker_round
from .start_multi_poker_round import start_multi_poker_round
from .process_drawing import process_drawing
from .process_multi_drawing import process_multi_drawing
from .reset_game_variables import reset_game_variables

def handle_poker_action(action: str, payload: Optional[any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """Handles input actions for Draw Poker and Multi-Hand Poker states."""
    new_game_state = current_game_state.copy()
    current_state_str = new_game_state['current_state']

    # --- Return to Menu (Needs Confirmation Check) ---
    if action == actions_cfg.ACTION_RETURN_TO_MENU:
        if current_state_str in [states.STATE_DRAW_POKER_WAITING_FOR_HOLD, states.STATE_MULTI_POKER_WAITING_FOR_HOLD]:
            if sounds.get("button"): sounds["button"].play()
            # Trigger confirmation
            new_game_state['confirm_action_type'] = 'EXIT'
            new_game_state['confirm_exit_destination'] = states.STATE_GAME_SELECTION
            new_game_state['previous_state_before_confirm'] = current_state_str
            new_game_state['current_state'] = states.STATE_CONFIRM_EXIT
        elif current_state_str in [states.STATE_DRAW_POKER_IDLE, states.STATE_DRAW_POKER_SHOWING_RESULT,
                                   states.STATE_MULTI_POKER_IDLE, states.STATE_MULTI_POKER_SHOWING_RESULT]:
            # Allow direct exit from idle/result states
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['message'] = ""
            new_game_state['current_state'] = states.STATE_GAME_SELECTION
        return new_game_state # Return early after handling menu action

    # --- Deal/Draw Actions ---
    if action == actions_cfg.ACTION_DEAL_DRAW:
        if current_state_str == states.STATE_DRAW_POKER_IDLE:
            if sounds.get("button"): sounds["button"].play()
            round_state = start_draw_poker_round(game_state_manager, sounds)
            new_game_state.update(round_state)
        elif current_state_str == states.STATE_MULTI_POKER_IDLE:
            if sounds.get("button"): sounds["button"].play()
            round_state = start_multi_poker_round(game_state_manager, sounds)
            new_game_state.update(round_state)
        elif current_state_str == states.STATE_DRAW_POKER_WAITING_FOR_HOLD:
            if sounds.get("button"): sounds["button"].play()
            draw_results = process_drawing(
                new_game_state['hand'], new_game_state['held_indices'],
                new_game_state['deck'], game_state_manager, sounds
            )
            new_game_state.update(draw_results)
        elif current_state_str == states.STATE_MULTI_POKER_WAITING_FOR_HOLD:
            if sounds.get("button"): sounds["button"].play()
            multi_draw_results = process_multi_drawing(
                new_game_state['hand'], new_game_state['held_indices'],
                game_state_manager, sounds
            )
            new_game_state.update(multi_draw_results)
        elif current_state_str == states.STATE_DRAW_POKER_SHOWING_RESULT:
            if sounds.get("button"): sounds["button"].play()
            if game_state_manager.can_afford_bet(1):
                round_state = start_draw_poker_round(game_state_manager, sounds)
                new_game_state.update(round_state)
            else:
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['message'] = "GAME OVER! Not enough money."
                new_game_state['current_state'] = states.STATE_GAME_OVER
        elif current_state_str == states.STATE_MULTI_POKER_SHOWING_RESULT:
            if sounds.get("button"): sounds["button"].play()
            cost_next_multi = layout_cards.NUM_MULTI_HANDS
            if game_state_manager.can_afford_bet(cost_next_multi):
                round_state = start_multi_poker_round(game_state_manager, sounds)
                new_game_state.update(round_state)
            else:
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['message'] = f"GAME OVER! Need ${cost_next_multi} for Multi Poker."
                new_game_state['current_state'] = states.STATE_GAME_OVER

    # --- Hold Toggle Action ---
    elif action == actions_cfg.ACTION_HOLD_TOGGLE:
        if current_state_str in [states.STATE_DRAW_POKER_WAITING_FOR_HOLD, states.STATE_MULTI_POKER_WAITING_FOR_HOLD]:
            index = payload
            if index is not None and 0 <= index < 5:
                held_indices = new_game_state['held_indices']
                if index in held_indices:
                    held_indices.remove(index)
                    if sounds.get("hold"): sounds["hold"].play()
                else:
                    held_indices.append(index)
                    held_indices.sort()
                    if sounds.get("hold"): sounds["hold"].play()
                new_game_state['held_indices'] = held_indices

    return new_game_state

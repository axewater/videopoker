# /game_functions/update_game.py

from typing import Dict, Any

import constants
from .determine_roulette_result import determine_roulette_result
from game_state import GameState

# *** Add sounds parameter ***
def update_game(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles game logic updates per frame (timers, game over checks).
    Returns a dictionary containing the potentially modified game state variables.
    """
    new_state = current_game_state.copy()

    # Update money animation timer
    if new_state.get('money_animation_active', False):
        timer = new_state.get('money_animation_timer', 0)
        timer -= 1
        if timer <= 0:
            new_state['money_animation_active'] = False
            new_state['money_animation_amount'] = 0
            new_state['money_animation_timer'] = 0
        else:
            new_state['money_animation_timer'] = timer

    # Update result message flashing timer
    if new_state.get('result_message_flash_active', False):
        flash_timer = new_state.get('result_message_flash_timer', 0)
        flash_timer -= 1
        if flash_timer <= 0:
            new_state['result_message_flash_active'] = False
            new_state['result_message_flash_timer'] = 0
            new_state['result_message_flash_visible'] = True # Ensure it's visible when flashing stops
        else:
            new_state['result_message_flash_timer'] = flash_timer
            # Toggle visibility based on interval
            if flash_timer % constants.RESULT_FLASH_INTERVAL == 0:
                new_state['result_message_flash_visible'] = not new_state.get('result_message_flash_visible', True)

    # Update Roulette spin timer
    if new_state['current_state'] == constants.STATE_ROULETTE_SPINNING:
        spin_timer = new_state.get('roulette_spin_timer', 0)
        spin_timer -= 1
        if spin_timer <= 0:
            # Spin finished, determine result and change state
            # *** Pass sounds dictionary to determine_roulette_result ***
            result_state = determine_roulette_result(new_state, game_state_manager, sounds)
            new_state.update(result_state)
            new_state['roulette_spin_timer'] = 0 # Reset timer
        else:
            new_state['roulette_spin_timer'] = spin_timer

    # Check for game over condition (logic remains the same)
    # ... (game over check as before) ...
    current_state_str = new_state['current_state']
    # Simplified check: Is the player in a state where they might need to start a new paid round?
    needs_money_check_states = [
        constants.STATE_DRAW_POKER_SHOWING_RESULT,
        constants.STATE_MULTI_POKER_SHOWING_RESULT,
        constants.STATE_BLACKJACK_SHOWING_RESULT,
        # Roulette doesn't automatically start a new round, so GAME OVER isn't triggered this way
    ]
    if current_state_str in needs_money_check_states:
        is_multi = current_state_str == constants.STATE_MULTI_POKER_SHOWING_RESULT
        cost_next_game = constants.NUM_MULTI_HANDS if is_multi else 1
        if not game_state_manager.can_afford_bet(cost_next_game):
            # Check if already game over to prevent message spam
            if new_state['current_state'] != constants.STATE_GAME_OVER:
                 new_state['message'] = f"GAME OVER! Need ${cost_next_game} for next round."
                 new_state['current_state'] = constants.STATE_GAME_OVER


    return new_state

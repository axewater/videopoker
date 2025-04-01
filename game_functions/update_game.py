from typing import Dict, Any

import constants
from game_state import GameState

def update_game(current_game_state: Dict[str, Any], game_state_manager: GameState) -> Dict[str, Any]:
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

    # Check for game over condition if not already in game over state or main menu
    current_state_str = new_state['current_state']
    if current_state_str not in [constants.STATE_TOP_MENU, constants.STATE_GAME_SELECTION, constants.STATE_SETTINGS, constants.STATE_GAME_OVER, constants.STATE_CONFIRM_EXIT, constants.STATE_DRAW_POKER_IDLE, constants.STATE_MULTI_POKER_IDLE]:
         # Determine cost for the *next* game based on the current mode
         is_multi = current_state_str in [constants.STATE_MULTI_POKER_WAITING_FOR_HOLD, constants.STATE_MULTI_POKER_SHOWING_RESULT, constants.STATE_MULTI_POKER_IDLE]
         cost_next_game = constants.NUM_MULTI_HANDS if is_multi else 1

         # Transition to GAME_OVER if player cannot afford the next game *after* showing results
         if current_state_str in [constants.STATE_DRAW_POKER_SHOWING_RESULT, constants.STATE_MULTI_POKER_SHOWING_RESULT]:
             if game_state_manager.money < cost_next_game:
                 # Don't overwrite existing result message if game just ended
                 if not new_state.get('message', '').startswith("GAME OVER"):
                      new_state['message'] = "GAME OVER! Not enough money."
                 new_state['current_state'] = constants.STATE_GAME_OVER

    return new_state

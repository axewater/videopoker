# /game_functions/update_game.py

from typing import Dict, Any

import config_states as states
import config_animations as anim
import config_layout_cards as layout_cards
from .determine_roulette_result import determine_roulette_result
from .resolve_slots_round import resolve_slots_round
from game_state import GameState

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
            if flash_timer % anim.RESULT_FLASH_INTERVAL == 0:
                new_state['result_message_flash_visible'] = not new_state.get('result_message_flash_visible', True)

    # Update Roulette spin/pause/flash logic
    if new_state['current_state'] == states.STATE_ROULETTE_SPINNING:
        spin_timer = new_state.get('roulette_spin_timer', 0)
        pause_timer = new_state.get('roulette_pause_timer', 0)

        if spin_timer > 0:
            # Still spinning
            spin_timer -= 1
            new_state['roulette_spin_timer'] = spin_timer
            if spin_timer == 0:
                # Spin just finished, start pause and flashing
                new_state['roulette_pause_timer'] = anim.ROULETTE_RESULT_PAUSE_DURATION
                new_state['winning_slot_flash_active'] = True
                new_state['winning_slot_flash_count'] = anim.ROULETTE_FLASH_COUNT * 2 # Total on/off cycles
                new_state['winning_slot_flash_visible'] = True # Start visible

        elif pause_timer > 0:
            # In pause/flash phase
            pause_timer -= 1
            new_state['roulette_pause_timer'] = pause_timer

            # Update flashing state
            flash_count = new_state.get('winning_slot_flash_count', 0)
            if flash_count > 0:
                 # Decrement count every interval
                 if pause_timer % anim.ROULETTE_FLASH_INTERVAL == 0:
                     new_state['winning_slot_flash_visible'] = not new_state.get('winning_slot_flash_visible', True)
                     flash_count -= 1
                     new_state['winning_slot_flash_count'] = flash_count
                 if flash_count == 0: # Flashing finished
                      new_state['winning_slot_flash_active'] = False
                      new_state['winning_slot_flash_visible'] = True # Ensure visible at end

            if pause_timer == 0:
                # Pause finished, determine result and change state
                result_state = determine_roulette_result(new_state, game_state_manager, sounds)
                new_state.update(result_state)
                # Reset flashing flags fully just in case
                new_state['winning_slot_flash_active'] = False
                new_state['winning_slot_flash_visible'] = True
                new_state['winning_slot_flash_count'] = 0

    # Update Slots spin/pause logic
    elif new_state['current_state'] == states.STATE_SLOTS_SPINNING:
        spin_timer = new_state.get('slots_spin_timer', 0)
        spin_timer -= 1
        new_state['slots_spin_timer'] = spin_timer
        if spin_timer <= 0:
            # Spin finished, resolve the round
            resolve_state = resolve_slots_round(new_state, game_state_manager, sounds)
            new_state.update(resolve_state)

    elif new_state['current_state'] == states.STATE_SLOTS_SHOWING_RESULT:
        pause_timer = new_state.get('slots_result_pause_timer', 0)
        pause_timer -= 1
        new_state['slots_result_pause_timer'] = pause_timer
        if pause_timer <= 0:
            # Pause finished, return to idle state
            new_state['current_state'] = states.STATE_SLOTS_IDLE
            new_state['message'] = "Click SPIN to play ($1)" # Reset message

    # Check for game over condition (logic remains the same)
    current_state_str = new_state['current_state']
    needs_money_check_states = [
        states.STATE_DRAW_POKER_SHOWING_RESULT,
        states.STATE_MULTI_POKER_SHOWING_RESULT,
        states.STATE_BLACKJACK_SHOWING_RESULT,
    ]
    if current_state_str in needs_money_check_states:
        is_multi = current_state_str == states.STATE_MULTI_POKER_SHOWING_RESULT
        cost_next_game = layout_cards.NUM_MULTI_HANDS if is_multi else 1
        if not game_state_manager.can_afford_bet(cost_next_game):
            if new_state['current_state'] != states.STATE_GAME_OVER:
                 new_state['message'] = f"GAME OVER! Need ${cost_next_game} for next round."
                 new_state['current_state'] = states.STATE_GAME_OVER

    return new_state

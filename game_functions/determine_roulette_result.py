import random
from typing import Dict, Any

import constants
from game_state import GameState
from .calculate_roulette_winnings import calculate_roulette_winnings

def determine_roulette_result(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determines the winning number, calculates payouts, and updates the game state.
    Called after the spin animation/timer finishes.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()

    # 1. Determine Winning Number
    # Use the actual wheel numbers for potential future animation logic
    winning_number = random.choice(constants.ROULETTE_WHEEL_NUMBERS)
    new_state['roulette_winning_number'] = winning_number

    # 2. Calculate Winnings
    bets = new_state.get('roulette_bets', {})
    net_winnings, result_message = calculate_roulette_winnings(winning_number, bets, game_state_manager)

    new_state['result_message'] = result_message

    # 3. Play Sounds & Trigger Animations
    if net_winnings > 0:
        if sounds.get("win"): sounds["win"].play()
        # Trigger animations (using existing money animation logic)
        # Amount should be the total returned to player (payout + original winning bets)
        total_returned = net_winnings + sum(amount for key, amount in bets.items() if winning_number in get_winning_numbers_for_bet(key))
        new_state['money_animation_active'] = True
        new_state['money_animation_amount'] = total_returned
        new_state['money_animation_timer'] = constants.MONEY_ANIMATION_DURATION
        new_state['result_message_flash_active'] = True
        new_state['result_message_flash_timer'] = constants.RESULT_FLASH_DURATION
        new_state['result_message_flash_visible'] = True
    elif net_winnings < 0:
        if sounds.get("lose"): sounds["lose"].play()
        new_state['money_animation_active'] = False
        new_state['result_message_flash_active'] = False
    else: # Push or no bets won/lost
        # No sound? Or a neutral sound?
        new_state['money_animation_active'] = False
        new_state['result_message_flash_active'] = False


    # 4. Update State
    new_state['current_state'] = constants.STATE_ROULETTE_RESULT
    new_state['message'] = "Click 'Clear Bets' or place new bets." # Next action prompt

    # Bets are kept in the state until explicitly cleared by the player
    # game_state_manager.reset_round_bet() # Reset the internal bet tracker

    return new_state

# Need these for win calculation logic within this file temporarily
from roulette_rules import get_winning_numbers_for_bet

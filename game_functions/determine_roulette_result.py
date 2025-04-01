import random
from typing import Dict, Any

import config_animations as animations
import config_states as states
from game_state import GameState
# No longer need calculate_roulette_winnings here directly
# from .calculate_roulette_winnings import calculate_roulette_winnings
# Need the rules for getting number properties
from roulette_rules import get_winning_numbers_for_bet, RED_NUMBERS, BLACK_NUMBERS, GREEN_NUMBER

# This function is now primarily responsible for calculating winnings and setting messages
# based on a pre-determined winning number.
def determine_roulette_result(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates payouts based on the pre-determined winning number stored in the state,
    updates money, sets messages/animations, and transitions state to RESULT.
    Called after the spin animation/timer finishes.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()

    # 1. Get the pre-determined Winning Number
    winning_number = new_state.get('roulette_winning_number')
    if winning_number is None:
        print("Error: Winning number not found in state for result calculation!")
        # Handle error gracefully - maybe force a loss or re-spin?
        # For now, set to 0 and proceed, logging the error.
        winning_number = 0
        new_state['roulette_winning_number'] = 0 # Ensure it's set

    # 2. Calculate Winnings (using imported rules)
    bets = new_state.get('roulette_bets', {})
    total_payout = 0
    total_bet_amount = sum(bets.values())
    winning_bets_summary = []

    # Re-implement calculation logic here (from calculate_roulette_winnings)
    from roulette_rules import get_payout_for_bet # Local import ok here
    for bet_key, bet_amount in bets.items():
        winning_numbers_for_this_bet = get_winning_numbers_for_bet(bet_key)
        if winning_number in winning_numbers_for_this_bet:
            payout_multiplier = get_payout_for_bet(bet_key)
            # Payout includes the original bet back
            payout = (payout_multiplier * bet_amount) + bet_amount
            total_payout += payout
            # Format bet key nicely for the message
            bet_name = bet_key.replace('_', ' ').title()
            winning_bets_summary.append(f"{bet_name} (+${payout})")

    net_winnings = total_payout - total_bet_amount

    # Update player's money - add the total payout
    if total_payout > 0:
        game_state_manager.add_winnings(total_payout)

    # Construct result message
    number_color = "Green" if winning_number in GREEN_NUMBER else ("Red" if winning_number in RED_NUMBERS else "Black")
    result_message = f"Number {winning_number} ({number_color}) wins! "

    if net_winnings > 0:
        result_message += f"You win ${net_winnings}! "
        if winning_bets_summary:
             result_message += f"({', '.join(winning_bets_summary)})"
    elif net_winnings == 0 and total_payout > 0: # Bets returned, no net gain/loss
         result_message += "Bets returned."
    elif total_bet_amount > 0: # Avoid saying "You lost $0" if no bets were placed
        result_message += f"You lost ${abs(net_winnings)}."
    else:
        result_message += "No bets placed."


    new_state['result_message'] = result_message

    # 3. Play Sounds & Trigger Animations
    if net_winnings > 0:
        if sounds.get("win"): sounds["win"].play()
        # Amount should be the total returned (net winnings + original winning bets)
        original_winning_bets_value = total_payout - net_winnings
        total_returned = net_winnings + original_winning_bets_value
        new_state['money_animation_active'] = True
        new_state['money_animation_amount'] = total_returned
        new_state['money_animation_timer'] = animations.MONEY_ANIMATION_DURATION
        new_state['result_message_flash_active'] = True
        new_state['result_message_flash_timer'] = animations.RESULT_FLASH_DURATION
        new_state['result_message_flash_visible'] = True
    elif net_winnings < 0:
        if sounds.get("lose"): sounds["lose"].play()
        new_state['money_animation_active'] = False
        new_state['result_message_flash_active'] = False
    else: # Push or no bets won/lost
        new_state['money_animation_active'] = False
        new_state['result_message_flash_active'] = False


    # 4. Update State for Result Display
    new_state['current_state'] = states.STATE_ROULETTE_RESULT
    new_state['message'] = "Click 'Clear Bets' or place new bets." # Next action prompt

    # Bets are kept in the state until explicitly cleared by the player
    # game_state_manager.reset_round_bet() # Reset the internal bet tracker for the next round

    return new_state

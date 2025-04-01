from typing import Dict, Any, Tuple

from game_state import GameState
from roulette_rules import get_winning_numbers_for_bet, get_payout_for_bet, RED_NUMBERS

def calculate_roulette_winnings(winning_number: int, bets: Dict[str, int], game_state_manager: GameState) -> Tuple[int, str]:
    """
    Calculates the total winnings for the placed bets based on the winning number.
    Updates the player's money via game_state_manager.
    Returns the total net winnings (positive or negative) and a result summary message.
    """
    total_payout = 0
    total_bet_amount = sum(bets.values())

    winning_bets_summary = []

    for bet_key, bet_amount in bets.items():
        winning_numbers = get_winning_numbers_for_bet(bet_key)
        if winning_number in winning_numbers:
            payout_multiplier = get_payout_for_bet(bet_key)
            payout = (payout_multiplier * bet_amount) + bet_amount # Payout includes original bet back
            total_payout += payout
            winning_bets_summary.append(f"{bet_key.replace('_', ' ').title()} (+${payout})")

    net_winnings = total_payout - total_bet_amount

    # Update player's money - add the total payout (which includes original bets back for winners)
    if total_payout > 0:
        game_state_manager.add_winnings(total_payout)

    # Construct result message
    number_color = "Green" if winning_number == 0 else ("Red" if winning_number in RED_NUMBERS else "Black")
    result_message = f"Number {winning_number} ({number_color}) wins! "

    if net_winnings > 0:
        result_message += f"You win ${net_winnings}! "
        if winning_bets_summary:
             result_message += f"({', '.join(winning_bets_summary)})"
    elif net_winnings == 0 and total_payout > 0: # Bets returned, no net gain/loss
         result_message += "Bets returned."
    else: # Net loss
        result_message += f"You lost ${abs(net_winnings)}."


    return net_winnings, result_message

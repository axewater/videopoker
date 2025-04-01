# /game_functions/place_roulette_bet.py
from typing import Dict, Any

import config_display as display
from game_state import GameState

# Define the amount placed per click
BET_AMOUNT_PER_CLICK = 1

def place_roulette_bet(bet_info: Dict[str, Any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles placing a single chip bet on a specific Roulette spot.
    Updates the 'roulette_bets' dictionary in the game state.
    Does NOT deduct money here; money is deducted when SPIN is pressed.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()
    bets = new_state.get('roulette_bets', {})
    bet_type = bet_info.get('type')
    bet_value = bet_info.get('value')

    if not bet_type:
        print("Error: Bet type missing in bet_info")
        return new_state # No change

    # Construct the bet key (e.g., 'number_5', 'color_red')
    bet_key = f"{bet_type}_{bet_value}" if bet_value is not None else bet_type

    # Check if player can afford *at least* one chip
    # We don't deduct yet, but prevent placing bets if already broke.
    # A better check would be against the total potential bet if SPIN was pressed now.
    if not game_state_manager.can_afford_bet(BET_AMOUNT_PER_CLICK):
        new_state['message'] = "Not enough money to place more bets!"
        # Optionally play a different sound?
        return new_state

    # Add bet amount to the specific bet key
    current_bet_on_spot = bets.get(bet_key, 0)
    bets[bet_key] = current_bet_on_spot + BET_AMOUNT_PER_CLICK

    new_state['roulette_bets'] = bets
    new_state['message'] = f"Bet ${bets[bet_key]} on {bet_key.replace('_', ' ').title()}" # User feedback

    if sounds.get("hold"): # Use 'hold' sound for placing chip? Or add a 'chip' sound?
        sounds["hold"].play()

    # Recalculate total potential bet amount for display/checking later
    total_bet_amount = sum(bets.values())
    new_state['roulette_total_bet'] = total_bet_amount
    # Update message to show total bet
    new_state['message'] += f" (Total Bet: ${total_bet_amount})"


    return new_state

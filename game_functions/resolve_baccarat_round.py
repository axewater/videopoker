"""
Resolves the Baccarat round after all cards are dealt/drawn.
Determines winner, calculates payout, updates state.
"""
from typing import Dict, Any

import config_states as states
import config_animations as anim
from game_state import GameState # Need GameState to update money
from baccarat_rules import (
    determine_baccarat_winner, calculate_baccarat_payout,
    get_baccarat_hand_value
)

def resolve_baccarat_round(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolves the Baccarat round after potential third card draws.
    Determines winner, calculates payout, updates money and game state.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()
    player_hand = new_state.get('baccarat_player_hand', [])
    banker_hand = new_state.get('baccarat_banker_hand', [])
    bet_type = new_state.get('baccarat_bet_type')
    bet_amount = new_state.get('baccarat_total_bet', 0)

    if not player_hand or not banker_hand or not bet_type or bet_amount <= 0:
        print("Error: Invalid state for Baccarat resolution.")
        new_state['message'] = "Error resolving round."
        new_state['current_state'] = states.STATE_BACCARAT_BETTING
        return new_state

    # Determine winner and final values
    winning_hand, player_val, banker_val = determine_baccarat_winner(player_hand, banker_hand)
    total_returned, net_winnings = calculate_baccarat_payout(bet_type, bet_amount, winning_hand)

    new_state['baccarat_player_value'] = player_val
    new_state['baccarat_banker_value'] = banker_val
    new_state['baccarat_winner'] = winning_hand

    # Update money and set messages/animations
    if net_winnings > 0:
        game_state_manager.add_winnings(int(round(total_returned))) # Add total return (bet + win), ensure int
        new_state['result_message'] = f"{winning_hand} wins! +${int(round(total_returned))}"
        if sounds.get("win"): sounds["win"].play()
        new_state['money_animation_active'] = True
        new_state['money_animation_amount'] = int(round(total_returned))
        new_state['money_animation_timer'] = anim.MONEY_ANIMATION_DURATION
        new_state['result_message_flash_active'] = True
        new_state['result_message_flash_timer'] = anim.RESULT_FLASH_DURATION
        new_state['result_message_flash_visible'] = True
    elif net_winnings == 0: # Push (Tie occurred, bet was on Player/Banker)
        game_state_manager.add_winnings(int(round(total_returned))) # Return original bet
        new_state['result_message'] = f"Tie! Bet Returned"
        # No win/lose sound for push
        new_state['money_animation_active'] = False # No animation for push
        new_state['result_message_flash_active'] = False
    else: # Loss
        # Bet was already deducted, no money change needed
        new_state['result_message'] = f"{winning_hand} wins! You lose -${bet_amount}"
        if sounds.get("lose"): sounds["lose"].play()
        new_state['money_animation_active'] = False # No animation for loss
        new_state['result_message_flash_active'] = False

    new_state['message'] = "Place bets or Deal again."
    new_state['current_state'] = states.STATE_BACCARAT_RESULT

    return new_state

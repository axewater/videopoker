# /game_functions/start_baccarat_round.py
"""
Handles the start of a Baccarat round: dealing initial cards and checking for naturals.
"""
from typing import Dict, Any

import config_states as states
import config_animations as anim
from deck import Deck
from game_state import GameState
from baccarat_rules import (
    is_natural, determine_baccarat_winner, calculate_baccarat_payout,
    BET_PLAYER, BET_BANKER, BET_TIE, get_baccarat_hand_value
)
from .reset_game_variables import reset_game_variables # Use to clear previous round state

def start_baccarat_round(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Starts a new round of Baccarat. Deals cards, checks for naturals, and determines immediate outcome or proceeds.
    Assumes bets are already placed and validated in handle_baccarat_action.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()
    bet_amount = new_state.get('baccarat_total_bet', 0)
    bet_type = new_state.get('baccarat_bet_type') # Should be set before calling this

    # Reset previous round variables (hands, results) but keep bets for this round
    reset_vars = reset_game_variables()
    new_state.update(reset_vars)
    # Restore bets for this round
    new_state['baccarat_total_bet'] = bet_amount
    new_state['baccarat_bet_type'] = bet_type

    deck = Deck() # Fresh deck

    # Deal initial hands (Player, Banker, Player, Banker)
    player_hand = [deck.deal(1)[0], deck.deal(1)[0]]
    banker_hand = [deck.deal(1)[0], deck.deal(1)[0]]

    new_state['baccarat_player_hand'] = player_hand
    new_state['baccarat_banker_hand'] = banker_hand
    new_state['deck'] = deck # Store the deck

    if sounds.get("deal"):
        sounds["deal"].play()

    new_state['current_state'] = states.STATE_BACCARAT_DEALING # Indicate dealing phase

    # Check for Naturals
    player_natural = is_natural(player_hand)
    banker_natural = is_natural(banker_hand)

    if player_natural or banker_natural:
        # Natural occurred, round ends immediately. Resolve winner.
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
        elif net_winnings == 0: # Push (Tie occurred, bet was on Player/Banker)
            game_state_manager.add_winnings(int(round(total_returned))) # Return original bet
            new_state['result_message'] = f"Tie! Bet Returned"
            # No win/lose sound for push
        else: # Loss
            # Bet was already deducted, no money change needed
            new_state['result_message'] = f"{winning_hand} wins! You lose -${bet_amount}"
            if sounds.get("lose"): sounds["lose"].play()

        new_state['message'] = "Place bets or Deal again."
        new_state['current_state'] = states.STATE_BACCARAT_RESULT

    else:
        # No Natural, proceed to drawing phase
        # Store initial values for display during drawing phase if needed
        new_state['baccarat_player_value'] = get_baccarat_hand_value(player_hand)
        new_state['baccarat_banker_value'] = get_baccarat_hand_value(banker_hand)
        new_state['message'] = "Checking drawing rules..."
        new_state['current_state'] = states.STATE_BACCARAT_DRAWING # Move to drawing logic state
        # We can add a small delay timer here if we want a pause before drawing starts
        # new_state['baccarat_draw_delay_timer'] = 30 # e.g., 1 second delay

    return new_state

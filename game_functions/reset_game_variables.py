# /game_functions/reset_game_variables.py
from typing import Dict, Any, List, Optional

from poker_rules import HandRank # Import HandRank if needed for type hint

def reset_game_variables() -> Dict[str, Any]:
    """Resets variables needed for starting a new game or returning to menu.
       Returns a dictionary containing the reset state variables.
    """
    return {
        'hand': [],
        'multi_hands': [],
        'multi_results': [],
        'held_indices': [],
        'message': "",
        'result_message': "",
        'final_hand_rank': None,
        'total_winnings': 0,
        'money_animation_active': False,
        'money_animation_timer': 0,
        'money_animation_amount': 0,
        # Result message flashing state
        'result_message_flash_active': False,
        'result_message_flash_timer': 0,
        'result_message_flash_visible': True,
        # Roulette specific state reset
        'roulette_bets': {},
        'roulette_winning_number': None,
        'roulette_spin_timer': 0,
        'roulette_pause_timer': 0, # Reset pause timer
        'winning_slot_flash_active': False, # Reset flash active flag
        'winning_slot_flash_count': 0, # Reset flash count
        'winning_slot_flash_visible': True, # Reset flash visibility
        # Slots specific state reset
        'slots_final_symbols': ["?", "?", "?"], # Use placeholders initially
        'slots_spin_timer': 0,
        'slots_result_pause_timer': 0,
        # Baccarat specific state reset
        'baccarat_bets': {},
        'baccarat_bet_type': None,
        'baccarat_total_bet': 0,
        'baccarat_player_hand': [],
        'baccarat_banker_hand': [],
        'baccarat_player_value': None,
        'baccarat_banker_value': None,
        'baccarat_winner': None,
        # Note: deck and current_state are typically handled by the calling function
        # Note: game_state_manager (money) is NOT reset here
    }

from typing import Dict, Any, List, Optional

import constants
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
        # Note: deck and current_state are typically handled by the calling function
        # Note: game_state_manager (money) is NOT reset here
    }

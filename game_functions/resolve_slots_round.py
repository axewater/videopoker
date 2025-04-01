from typing import Dict, Any

import constants
from game_state import GameState
from slots_rules import calculate_winnings # Import the function to calculate winnings
from .process_slots_spin import SLOTS_COST_PER_SPIN # Import cost per spin

def resolve_slots_round(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates winnings based on the final symbols stored in the state,
    updates money, sets messages/animations, and transitions state to SHOWING_RESULT.
    Called after the spin animation/timer finishes.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()

    # 1. Get the final symbols determined before the spin
    final_symbols = new_state.get('slots_final_symbols')
    if not final_symbols or len(final_symbols) != constants.NUM_REELS:
        print(f"Error: Final symbols not found or invalid in state: {final_symbols}")
        # Handle error gracefully - assume no win
        final_symbols = ["?", "?", "?"] # Placeholder
        winnings = 0
        win_name = ""
        new_state['slots_final_symbols'] = final_symbols # Ensure it's set for display
    else:
        # 2. Calculate Winnings
        winnings, win_name = calculate_winnings(final_symbols, SLOTS_COST_PER_SPIN)

    # 3. Update Money and Set Messages/Sounds/Animations
    if winnings > 0:
        game_state_manager.add_winnings(winnings) # Add net winnings
        new_state['result_message'] = f"WINNER! {win_name}! +${winnings}"
        if sounds.get("win"): sounds["win"].play()
        # Trigger animations
        new_state['money_animation_active'] = True
        new_state['money_animation_amount'] = winnings
        new_state['money_animation_timer'] = constants.MONEY_ANIMATION_DURATION
        new_state['result_message_flash_active'] = True
        new_state['result_message_flash_timer'] = constants.RESULT_FLASH_DURATION
        new_state['result_message_flash_visible'] = True
    else:
        new_state['result_message'] = "No win this spin."
        # Only play lose sound if they actually bet (which they must have to reach here)
        if sounds.get("lose"): sounds["lose"].play()
        # Ensure animations are off
        new_state['money_animation_active'] = False
        new_state['result_message_flash_active'] = False

    # 4. Update State for Result Display
    new_state['current_state'] = constants.STATE_SLOTS_SHOWING_RESULT
    new_state['slots_result_pause_timer'] = constants.SLOTS_RESULT_PAUSE_DURATION # Start pause timer
    new_state['message'] = "Click SPIN to play again." # Next action prompt

    # Reset the round bet tracker in GameState (optional, depends on how it's used)
    # game_state_manager.reset_round_bet()

    return new_state

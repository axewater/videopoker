# /game_functions/process_slots_spin.py
import random # Added missing import
from typing import Dict, Any

import constants
from game_state import GameState
from slots_rules import spin_reels, REEL_STRIPS # Import REEL_STRIPS from slots_rules
# Define the cost per spin
SLOTS_COST_PER_SPIN = 1

def process_slots_spin(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles the player clicking the SPIN button in the Slots game.
    Deducts cost, determines the result, starts the animation timer.
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()

    # 1. Check if player can afford the spin
    if not game_state_manager.can_afford_bet(SLOTS_COST_PER_SPIN):
        new_state['message'] = f"Not enough money! Need ${SLOTS_COST_PER_SPIN} to spin."
        if sounds.get("lose"): sounds["lose"].play()
        return new_state # Return without changing state if cannot afford

    # 2. Deduct cost
    if game_state_manager.deduct_bet(SLOTS_COST_PER_SPIN):
        if sounds.get("button"): sounds["button"].play() # Or a dedicated spin sound

        # 3. Determine the final result of the spin *before* animation starts
        final_symbols = spin_reels()
        new_state['slots_final_symbols'] = final_symbols # Store the result

        # 4. Set state to spinning and start timer
        new_state['current_state'] = constants.STATE_SLOTS_SPINNING
        new_state['slots_spin_timer'] = constants.SLOTS_SPIN_DURATION
        new_state['message'] = "Spinning..."
        new_state['result_message'] = "" # Clear previous result

        # Initialize reel positions for animation (e.g., start at random points)
        # These will be updated during the animation in draw_slots_screen
        # Use the imported REEL_STRIPS
        new_state['slots_reel_positions'] = [random.randint(0, len(strip) - 1) for strip in REEL_STRIPS]

    else:
        # Should not happen if can_afford_bet passed, but as a fallback
        new_state['message'] = "Error deducting bet!"
        if sounds.get("lose"): sounds["lose"].play()

    return new_state

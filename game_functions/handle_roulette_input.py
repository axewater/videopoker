# /game_functions/handle_roulette_input.py
import random
from typing import Dict, Any, Optional, Tuple

import config_states as states
import config_actions as actions_cfg
import config_animations as anim
import config_layout_roulette as layout_roulette # For wheel numbers
from game_state import GameState
from .place_roulette_bet import place_roulette_bet
from .reset_game_variables import reset_game_variables

def handle_roulette_action(action: str, payload: Optional[any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """Handles input actions for Roulette states."""
    new_game_state = current_game_state.copy()
    current_state_str = new_game_state['current_state']

    # --- Return to Menu (Needs Confirmation Check) ---
    if action == actions_cfg.ACTION_RETURN_TO_MENU:
        if current_state_str == states.STATE_ROULETTE_SPINNING:
            # Disallow exit during spin animation
            new_game_state['message'] = "Cannot exit while wheel is spinning!"
            # Don't change state or show confirmation
        elif current_state_str == states.STATE_ROULETTE_BETTING and new_game_state.get('roulette_bets'):
            # Confirm exit if bets are placed but not spun
            if sounds.get("button"): sounds["button"].play()
            new_game_state['confirm_action_type'] = 'EXIT'
            new_game_state['confirm_exit_destination'] = states.STATE_GAME_SELECTION
            new_game_state['previous_state_before_confirm'] = current_state_str
            new_game_state['current_state'] = states.STATE_CONFIRM_EXIT
        else: # Idle (no bets), Result, or Betting with no bets placed
            # Allow direct exit
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['roulette_bets'] = {} # Clear bets
            new_game_state['message'] = ""
            new_game_state['current_state'] = states.STATE_GAME_SELECTION
        return new_game_state # Return early after handling menu action

    # --- Betting Actions ---
    if action == actions_cfg.ACTION_ROULETTE_BET:
        if current_state_str in [states.STATE_ROULETTE_BETTING, states.STATE_ROULETTE_RESULT]:
            # If placing a bet after a result, reset the result state first
            if current_state_str == states.STATE_ROULETTE_RESULT:
                new_game_state['roulette_bets'] = {}
                new_game_state['roulette_winning_number'] = None
                new_game_state['result_message'] = ""
                new_game_state['message'] = "Place your bets!"
                new_game_state['current_state'] = states.STATE_ROULETTE_BETTING
                game_state_manager.reset_round_bet() # Reset internal tracker

            bet_result_state = place_roulette_bet(payload, new_game_state, game_state_manager, sounds)
            new_game_state.update(bet_result_state)

    # --- Spin Action ---
    elif action == actions_cfg.ACTION_ROULETTE_SPIN:
        if current_state_str == states.STATE_ROULETTE_BETTING:
            total_bet = new_game_state.get('roulette_total_bet', 0)
            if total_bet <= 0:
                new_game_state['message'] = "Place a bet before spinning!"
                if sounds.get("lose"): sounds["lose"].play()
            elif game_state_manager.can_afford_bet(total_bet):
                if game_state_manager.deduct_bet(total_bet):
                    if sounds.get("deal"): sounds["deal"].play()
                    # Determine winning number HERE
                    winning_number = random.choice(layout_roulette.ROULETTE_WHEEL_NUMBERS)
                    new_game_state['roulette_winning_number'] = winning_number
                    # Set state and timer for animation
                    new_game_state['current_state'] = states.STATE_ROULETTE_SPINNING
                    new_game_state['roulette_spin_timer'] = anim.ROULETTE_SPIN_DURATION
                    new_game_state['message'] = "Spinning..."
                    new_game_state['result_message'] = ""
                else:
                    new_game_state['message'] = "Error deducting bet!"
                    if sounds.get("lose"): sounds["lose"].play()
            else:
                new_game_state['message'] = f"Not enough money! Need ${total_bet} to spin."
                if sounds.get("lose"): sounds["lose"].play()

    # --- Clear Bets Action ---
    elif action == actions_cfg.ACTION_ROULETTE_CLEAR_BETS:
        if current_state_str in [states.STATE_ROULETTE_BETTING, states.STATE_ROULETTE_RESULT]:
            if new_game_state.get('roulette_bets'):
                if sounds.get("button"): sounds["button"].play()
                new_game_state['roulette_bets'] = {}
                new_game_state['roulette_total_bet'] = 0
                new_game_state['result_message'] = ""
                new_game_state['message'] = "Bets cleared. Place new bets."
                game_state_manager.reset_round_bet()
                if current_state_str == states.STATE_ROULETTE_RESULT:
                    new_game_state['current_state'] = states.STATE_ROULETTE_BETTING
                    new_game_state['roulette_winning_number'] = None

    return new_game_state

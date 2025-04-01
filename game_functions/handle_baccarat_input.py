# /game_functions/handle_baccarat_input.py
"""
Handles input actions specific to the Baccarat game states.
"""
from typing import Dict, Any, Optional

import config_states as states
import config_actions as actions_cfg
from game_state import GameState
from baccarat_rules import BET_PLAYER, BET_BANKER, BET_TIE # Import bet types
from .start_baccarat_round import start_baccarat_round
from .reset_game_variables import reset_game_variables

# Define the amount placed per click for Baccarat bets
BACCARAT_BET_AMOUNT_PER_CLICK = 1

def handle_baccarat_action(action: str, payload: Optional[any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """Handles input actions for Baccarat states."""
    new_game_state = current_game_state.copy()
    current_state_str = new_game_state['current_state']

    # --- Return to Menu (Needs Confirmation Check) ---
    if action == actions_cfg.ACTION_RETURN_TO_MENU:
        # Allow exit from Betting/Result states, confirm if bets placed
        # Disallow exit during Dealing/Drawing phases
        if current_state_str in [states.STATE_BACCARAT_DEALING, states.STATE_BACCARAT_DRAWING]:
            new_game_state['message'] = "Cannot exit during deal/draw!"
        elif current_state_str == states.STATE_BACCARAT_BETTING and new_game_state.get('baccarat_total_bet', 0) > 0:
            # Confirm exit if bets are placed but not dealt
            if sounds.get("button"): sounds["button"].play()
            new_game_state['confirm_action_type'] = 'EXIT'
            new_game_state['confirm_exit_destination'] = states.STATE_GAME_SELECTION
            new_game_state['previous_state_before_confirm'] = current_state_str
            new_game_state['current_state'] = states.STATE_CONFIRM_EXIT
        else: # Betting (no bets) or Result state
            # Allow direct exit
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            # Clear Baccarat specific state
            new_game_state['baccarat_bets'] = {}
            new_game_state['baccarat_bet_type'] = None
            new_game_state['baccarat_total_bet'] = 0
            new_game_state['baccarat_player_hand'] = []
            new_game_state['baccarat_banker_hand'] = []
            new_game_state['message'] = ""
            new_game_state['current_state'] = states.STATE_GAME_SELECTION
        return new_game_state # Return early after handling menu action

    # --- Betting Actions ---
    if action == actions_cfg.ACTION_BACCARAT_BET:
        if current_state_str in [states.STATE_BACCARAT_BETTING, states.STATE_BACCARAT_RESULT]:
            bet_type = payload.get('type') if isinstance(payload, dict) else None

            if not bet_type:
                return new_game_state # Invalid payload

            # If placing a bet after a result, reset the result state first
            if current_state_str == states.STATE_BACCARAT_RESULT:
                new_game_state['baccarat_bets'] = {}
                new_game_state['baccarat_total_bet'] = 0
                new_game_state['baccarat_player_hand'] = []
                new_game_state['baccarat_banker_hand'] = []
                new_game_state['baccarat_player_value'] = None
                new_game_state['baccarat_banker_value'] = None
                new_game_state['baccarat_winner'] = None
                new_game_state['result_message'] = ""
                new_game_state['message'] = "Place your bets!"
                new_game_state['current_state'] = states.STATE_BACCARAT_BETTING
                game_state_manager.reset_round_bet()

            # Check if player can afford the bet increment
            if not game_state_manager.can_afford_bet(BACCARAT_BET_AMOUNT_PER_CLICK):
                new_game_state['message'] = "Not enough money to place more bets!"
                if sounds.get("lose"): sounds["lose"].play()
                return new_game_state

            # Baccarat allows only one bet type per round (Player, Banker, or Tie)
            # If a bet already exists on a different type, clear it first.
            current_bet_type = new_game_state.get('baccarat_bet_type')
            current_bets = new_game_state.get('baccarat_bets', {})
            if current_bet_type and current_bet_type != bet_type:
                current_bets = {} # Clear existing bets if switching type
                new_game_state['baccarat_total_bet'] = 0

            # Add bet amount to the specific bet type
            current_bet_on_spot = current_bets.get(bet_type, 0)
            current_bets[bet_type] = current_bet_on_spot + BACCARAT_BET_AMOUNT_PER_CLICK

            new_game_state['baccarat_bets'] = current_bets
            new_game_state['baccarat_bet_type'] = bet_type # Store the single bet type
            new_game_state['baccarat_total_bet'] = current_bets[bet_type] # Total bet is just the amount on the chosen spot
            new_game_state['message'] = f"Bet ${new_game_state['baccarat_total_bet']} on {bet_type}"

            if sounds.get("hold"): sounds["hold"].play() # Use 'hold' sound for placing chip

    # --- Clear Bets Action ---
    elif action == actions_cfg.ACTION_BACCARAT_CLEAR_BETS:
        if current_state_str in [states.STATE_BACCARAT_BETTING, states.STATE_BACCARAT_RESULT]:
            if new_game_state.get('baccarat_total_bet', 0) > 0:
                if sounds.get("button"): sounds["button"].play()
                new_game_state['baccarat_bets'] = {}
                new_game_state['baccarat_bet_type'] = None
                new_game_state['baccarat_total_bet'] = 0
                new_game_state['result_message'] = ""
                new_game_state['message'] = "Bets cleared. Place new bets."
                game_state_manager.reset_round_bet()
                if current_state_str == states.STATE_BACCARAT_RESULT:
                    new_game_state['current_state'] = states.STATE_BACCARAT_BETTING
                    # Clear results from previous round
                    new_game_state['baccarat_player_hand'] = []
                    new_game_state['baccarat_banker_hand'] = []
                    new_game_state['baccarat_player_value'] = None
                    new_game_state['baccarat_banker_value'] = None
                    new_game_state['baccarat_winner'] = None

    # --- Deal Action ---
    elif action == actions_cfg.ACTION_BACCARAT_DEAL:
        if current_state_str == states.STATE_BACCARAT_BETTING or current_state_str == states.STATE_BACCARAT_RESULT:
            total_bet = new_game_state.get('baccarat_total_bet', 0)
            bet_type = new_game_state.get('baccarat_bet_type')

            if total_bet <= 0 or not bet_type:
                new_game_state['message'] = "Place a bet (Player, Banker, or Tie) before dealing!"
                if sounds.get("lose"): sounds["lose"].play()
            elif game_state_manager.can_afford_bet(total_bet):
                if game_state_manager.deduct_bet(total_bet):
                    # Start the round (deals cards, checks naturals)
                    round_state = start_baccarat_round(new_game_state, game_state_manager, sounds)
                    new_game_state.update(round_state)
                else:
                    new_game_state['message'] = "Error deducting bet!"
                    if sounds.get("lose"): sounds["lose"].play()
            else:
                new_game_state['message'] = f"Not enough money! Need ${total_bet} to deal."
                if sounds.get("lose"): sounds["lose"].play()

    return new_game_state

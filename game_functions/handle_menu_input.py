# /game_functions/handle_menu_input.py
from typing import Dict, Any, Optional, Tuple

import config_states as states
import config_actions as actions_cfg
import config_layout_cards as layout_cards
from game_state import GameState
from .reset_game_variables import reset_game_variables

def handle_menu_action(action: str, payload: Optional[any], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """Handles input actions for Top Menu, Game Selection, and Settings states."""
    new_game_state = current_game_state.copy()
    current_state_str = new_game_state['current_state']

    # --- Top Menu Actions ---
    if current_state_str == states.STATE_TOP_MENU:
        if action == actions_cfg.ACTION_GOTO_PLAY:
            if sounds.get("button"): sounds["button"].play()
            new_game_state['current_state'] = states.STATE_GAME_SELECTION
        elif action == actions_cfg.ACTION_GOTO_SETTINGS:
            if sounds.get("button"): sounds["button"].play()
            new_game_state['current_state'] = states.STATE_SETTINGS
        elif action == actions_cfg.ACTION_QUIT:
             if sounds.get("button"): sounds["button"].play()
             # Trigger confirmation dialog
             new_game_state['confirm_action_type'] = 'QUIT'
             new_game_state['previous_state_before_confirm'] = current_state_str
             new_game_state['current_state'] = states.STATE_CONFIRM_EXIT

    # --- Settings Actions ---
    elif current_state_str == states.STATE_SETTINGS:
        if action == actions_cfg.ACTION_TOGGLE_SOUND:
            new_game_state['sound_enabled'] = not new_game_state['sound_enabled']
            new_game_state['sound_setting_changed'] = True
            if new_game_state['sound_enabled'] and sounds.get("button"): sounds["button"].play()
        elif action == actions_cfg.ACTION_VOLUME_DOWN:
            if new_game_state['sound_enabled']:
                current_volume = new_game_state.get('volume_level', 0.7)
                new_volume = max(0.0, current_volume - 0.1)
                new_game_state['volume_level'] = round(new_volume, 2)
                new_game_state['volume_changed'] = True
                if sounds.get("button"): sounds["button"].play()
        elif action == actions_cfg.ACTION_VOLUME_UP:
            if new_game_state['sound_enabled']:
                current_volume = new_game_state.get('volume_level', 0.7)
                new_volume = min(1.0, current_volume + 0.1)
                new_game_state['volume_level'] = round(new_volume, 2)
                new_game_state['volume_changed'] = True
                if sounds.get("button"): sounds["button"].play()
        elif action == actions_cfg.ACTION_RETURN_TO_TOP_MENU:
            if sounds.get("button"): sounds["button"].play()
            new_game_state['current_state'] = states.STATE_TOP_MENU

    # --- Game Selection Actions ---
    elif current_state_str == states.STATE_GAME_SELECTION:
        if action == actions_cfg.ACTION_CHOOSE_DRAW_POKER:
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['current_state'] = states.STATE_DRAW_POKER_IDLE
            new_game_state['message'] = "Click DEAL to start ($1)"
        elif action == actions_cfg.ACTION_CHOOSE_MULTI_POKER:
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['current_state'] = states.STATE_MULTI_POKER_IDLE
            new_game_state['message'] = f"Click DEAL to start (${layout_cards.NUM_MULTI_HANDS})"
        elif action == actions_cfg.ACTION_CHOOSE_BLACKJACK:
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['current_state'] = states.STATE_BLACKJACK_IDLE
            new_game_state['message'] = "Click DEAL to play Blackjack ($1)"
            new_game_state['player_hand'] = []
            new_game_state['dealer_hand'] = []
        elif action == actions_cfg.ACTION_CHOOSE_ROULETTE:
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['current_state'] = states.STATE_ROULETTE_BETTING
            new_game_state['message'] = "Place your bets!"
            new_game_state['roulette_bets'] = {}
            new_game_state['roulette_winning_number'] = None
            new_game_state['roulette_total_bet'] = 0
        elif action == actions_cfg.ACTION_CHOOSE_SLOTS:
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['current_state'] = states.STATE_SLOTS_IDLE
            new_game_state['message'] = "Click SPIN to play ($1)"
            new_game_state['slots_final_symbols'] = ["?", "?", "?"]
            new_game_state['slots_reel_positions'] = [0, 0, 0]
            new_game_state['slots_spin_timer'] = 0
            new_game_state['slots_result_pause_timer'] = 0
        elif action == actions_cfg.ACTION_CHOOSE_BACCARAT:
            if sounds.get("button"): sounds["button"].play()
            reset_state = reset_game_variables()
            new_game_state.update(reset_state)
            new_game_state['current_state'] = states.STATE_BACCARAT_BETTING
            new_game_state['message'] = "Place your bet (Player, Banker, or Tie)"
            new_game_state['baccarat_bets'] = {}
            new_game_state['baccarat_bet_type'] = None
            new_game_state['baccarat_total_bet'] = 0
        elif action == actions_cfg.ACTION_RESTART_GAME:
            if sounds.get("button"): sounds["button"].play()
            new_game_state['confirm_action_type'] = 'RESTART'
            new_game_state['previous_state_before_confirm'] = states.STATE_GAME_SELECTION
            new_game_state['current_state'] = states.STATE_CONFIRM_EXIT
        elif action == actions_cfg.ACTION_RETURN_TO_TOP_MENU:
            if sounds.get("button"): sounds["button"].play()
            new_game_state['current_state'] = states.STATE_TOP_MENU

    # --- Generic Return to Menu (from a game) ---
    # This action is handled within each game's handler now, as it might need confirmation.

    # --- Game Over Action ---
    # elif current_state_str == states.STATE_GAME_OVER:
    #     if action == actions_cfg.ACTION_PLAY_AGAIN:
    #         if sounds.get("button"): sounds["button"].play()
    #         reset_state = reset_game_variables()
    #         new_game_state.update(reset_state)
    #         new_game_state['current_state'] = states.STATE_TOP_MENU
    #         new_game_state['needs_money_reset'] = True

    return new_game_state

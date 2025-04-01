# /input_handler.py
import pygame
from typing import List, Optional, Tuple, Dict, Any

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_general as layout_general
import config_layout_cards as layout_cards
import config_layout_roulette as layout_roulette
import config_layout_slots as layout_slots
import config_layout_baccarat as layout_baccarat

class InputHandler:
    """Handles user input events."""

    def __init__(self):
        """Initializes the input handler."""
        # No specific state needed here for now, but could hold things
        # like previous mouse state if needed for drag detection etc.
        pass

    def handle_events(self, current_state: str) -> List[Tuple[str, Optional[any]]]:
        """
        Processes Pygame events and returns a list of actions.
        Each action is a tuple: (ACTION_TYPE, payload).
        Payload is None for simple actions, or data like card index for HOLD_TOGGLE.
        """
        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append((actions_cfg.ACTION_QUIT, None))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # --- State-dependent checks ---
                if current_state == states.STATE_TOP_MENU:
                    if layout_general.PLAY_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_GOTO_PLAY, None))
                    elif layout_general.SETTINGS_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_GOTO_SETTINGS, None))
                    elif layout_general.TOP_MENU_QUIT_BUTTON_RECT.collidepoint(mouse_pos):
                         actions.append((actions_cfg.ACTION_QUIT, None))

                elif current_state == states.STATE_GAME_SELECTION:
                    if layout_general.DRAW_POKER_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CHOOSE_DRAW_POKER, None))
                    elif layout_general.MULTI_POKER_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CHOOSE_MULTI_POKER, None))
                    elif layout_general.BLACKJACK_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CHOOSE_BLACKJACK, None))
                    elif layout_general.ROULETTE_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CHOOSE_ROULETTE, None))
                    elif layout_general.SLOTS_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CHOOSE_SLOTS, None))
                    elif layout_general.BACCARAT_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CHOOSE_BACCARAT, None))
                    elif layout_general.SETTINGS_BACK_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RETURN_TO_TOP_MENU, None))
                    elif layout_general.RESTART_GAME_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RESTART_GAME, None))

                elif current_state == states.STATE_BLACKJACK_PLAYER_TURN:
                    if layout_cards.BLACKJACK_HIT_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_BLACKJACK_HIT, None))
                    elif layout_cards.BLACKJACK_STAND_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_BLACKJACK_STAND, None))
                    elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

                elif current_state in [states.STATE_DRAW_POKER_IDLE, states.STATE_MULTI_POKER_IDLE,
                                       states.STATE_DRAW_POKER_WAITING_FOR_HOLD, states.STATE_MULTI_POKER_WAITING_FOR_HOLD,
                                       states.STATE_DRAW_POKER_SHOWING_RESULT, states.STATE_MULTI_POKER_SHOWING_RESULT]:
                    # Check Deal/Draw button first
                    if layout_cards.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_DEAL_DRAW, None))
                    elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))
                    else:
                        # Check card clicks (only if Deal/Draw or Menu wasn't clicked)
                        for i, card_rect in enumerate(layout_cards.CARD_RECTS):
                            if card_rect.collidepoint(mouse_pos):
                                actions.append((actions_cfg.ACTION_HOLD_TOGGLE, i))
                                break # Process only one card click per event

                        # Check hold button clicks (if card wasn't clicked)
                        else:
                            for i, hold_rect in enumerate(layout_cards.HOLD_BUTTON_RECTS):
                                if hold_rect.collidepoint(mouse_pos):
                                    actions.append((actions_cfg.ACTION_HOLD_TOGGLE, i))
                                    break # Process only one hold button click

                elif current_state in [states.STATE_BLACKJACK_IDLE, states.STATE_BLACKJACK_SHOWING_RESULT]:
                     # Check Deal button first
                    if layout_cards.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_DEAL_DRAW, None))
                    elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

                elif current_state == states.STATE_GAME_OVER:
                    if layout_general.PLAY_AGAIN_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_PLAY_AGAIN, None))

                elif current_state == states.STATE_SETTINGS:
                    if layout_general.SOUND_TOGGLE_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_TOGGLE_SOUND, None))
                    elif layout_general.VOLUME_DOWN_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_VOLUME_DOWN, None))
                    elif layout_general.VOLUME_UP_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_VOLUME_UP, None))
                    elif layout_general.SETTINGS_BACK_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RETURN_TO_TOP_MENU, None))

                elif current_state == states.STATE_CONFIRM_EXIT:
                    if layout_general.CONFIRM_YES_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CONFIRM_YES, None))
                    elif layout_general.CONFIRM_NO_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_CONFIRM_NO, None))

                # --- Roulette Specific Input ---
                elif current_state == states.STATE_ROULETTE_BETTING:
                    clicked_on_bet_area = False
                    # Define outside bet areas using string keys
                    outside_bet_definitions: Dict[str, Dict[str, Any]] = {
                        'dozen_1': {'rect': layout_roulette.ROULETTE_BET_DOZEN1_RECT, 'type': 'dozen', 'value': '1'},
                        'dozen_2': {'rect': layout_roulette.ROULETTE_BET_DOZEN2_RECT, 'type': 'dozen', 'value': '2'},
                        'dozen_3': {'rect': layout_roulette.ROULETTE_BET_DOZEN3_RECT, 'type': 'dozen', 'value': '3'},
                        'column_1': {'rect': layout_roulette.ROULETTE_BET_COL1_RECT, 'type': 'column', 'value': '1'},
                        'column_2': {'rect': layout_roulette.ROULETTE_BET_COL2_RECT, 'type': 'column', 'value': '2'},
                        'column_3': {'rect': layout_roulette.ROULETTE_BET_COL3_RECT, 'type': 'column', 'value': '3'},
                        'half_low': {'rect': layout_roulette.ROULETTE_BET_LOW_RECT, 'type': 'half', 'value': 'low'},
                        'parity_even': {'rect': layout_roulette.ROULETTE_BET_EVEN_RECT, 'type': 'parity', 'value': 'even'},
                        'color_red': {'rect': layout_roulette.ROULETTE_BET_RED_RECT, 'type': 'color', 'value': 'red'},
                        'color_black': {'rect': layout_roulette.ROULETTE_BET_BLACK_RECT, 'type': 'color', 'value': 'black'},
                        'parity_odd': {'rect': layout_roulette.ROULETTE_BET_ODD_RECT, 'type': 'parity', 'value': 'odd'},
                        'half_high': {'rect': layout_roulette.ROULETTE_BET_HIGH_RECT, 'type': 'half', 'value': 'high'},
                    }

                    # Check number bets (0-36)
                    for number, rect in layout_roulette.ROULETTE_NUMBER_RECTS.items():
                        if rect and rect.collidepoint(mouse_pos):
                            actions.append((actions_cfg.ACTION_ROULETTE_BET, {'type': 'number', 'value': number}))
                            clicked_on_bet_area = True
                            break # Process only one bet click

                    # Check outside bets if no number was clicked
                    if not clicked_on_bet_area:
                        for bet_key, definition in outside_bet_definitions.items():
                             rect = definition.get('rect')
                             bet_info = {'type': definition.get('type'), 'value': definition.get('value')}
                             if rect and rect.collidepoint(mouse_pos):
                                 actions.append((actions_cfg.ACTION_ROULETTE_BET, bet_info))
                                 clicked_on_bet_area = True
                                 break

                    # Check buttons only if no bet area was clicked
                    if not clicked_on_bet_area:
                        if layout_roulette.ROULETTE_SPIN_BUTTON_RECT.collidepoint(mouse_pos):
                             actions.append((actions_cfg.ACTION_ROULETTE_SPIN, None))
                        elif layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT and layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT.collidepoint(mouse_pos):
                             actions.append((actions_cfg.ACTION_ROULETTE_CLEAR_BETS, None))
                        elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                             actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

                elif current_state == states.STATE_ROULETTE_SPINNING:
                    # Ignore most clicks during spin, except perhaps an emergency exit?
                    # For now, only allow returning to menu (will be handled in process_input)
                    if layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                         actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

                elif current_state == states.STATE_ROULETTE_RESULT:
                     # Allow clearing bets or returning to menu after result
                    if layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT and layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT.collidepoint(mouse_pos):
                         actions.append((actions_cfg.ACTION_ROULETTE_CLEAR_BETS, None))
                    elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                         actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))
                    # Also allow placing new bets immediately (acts like clear + place)
                    else:
                        clicked_on_bet_area = False
                        # Copied betting logic from STATE_ROULETTE_BETTING for convenience
                        # Define outside bet areas using string keys
                        outside_bet_definitions: Dict[str, Dict[str, Any]] = {
                            'dozen_1': {'rect': layout_roulette.ROULETTE_BET_DOZEN1_RECT, 'type': 'dozen', 'value': '1'},
                            'dozen_2': {'rect': layout_roulette.ROULETTE_BET_DOZEN2_RECT, 'type': 'dozen', 'value': '2'},
                            'dozen_3': {'rect': layout_roulette.ROULETTE_BET_DOZEN3_RECT, 'type': 'dozen', 'value': '3'},
                            'column_1': {'rect': layout_roulette.ROULETTE_BET_COL1_RECT, 'type': 'column', 'value': '1'},
                            'column_2': {'rect': layout_roulette.ROULETTE_BET_COL2_RECT, 'type': 'column', 'value': '2'},
                            'column_3': {'rect': layout_roulette.ROULETTE_BET_COL3_RECT, 'type': 'column', 'value': '3'},
                            'half_low': {'rect': layout_roulette.ROULETTE_BET_LOW_RECT, 'type': 'half', 'value': 'low'},
                            'parity_even': {'rect': layout_roulette.ROULETTE_BET_EVEN_RECT, 'type': 'parity', 'value': 'even'},
                            'color_red': {'rect': layout_roulette.ROULETTE_BET_RED_RECT, 'type': 'color', 'value': 'red'},
                            'color_black': {'rect': layout_roulette.ROULETTE_BET_BLACK_RECT, 'type': 'color', 'value': 'black'},
                            'parity_odd': {'rect': layout_roulette.ROULETTE_BET_ODD_RECT, 'type': 'parity', 'value': 'odd'},
                            'half_high': {'rect': layout_roulette.ROULETTE_BET_HIGH_RECT, 'type': 'half', 'value': 'high'},
                        }
                        for number, rect in layout_roulette.ROULETTE_NUMBER_RECTS.items():
                            if rect and rect.collidepoint(mouse_pos):
                                actions.append((actions_cfg.ACTION_ROULETTE_BET, {'type': 'number', 'value': number}))
                                clicked_on_bet_area = True
                                break
                        if not clicked_on_bet_area:
                             for bet_key, definition in outside_bet_definitions.items():
                                 rect = definition.get('rect')
                                 bet_info = {'type': definition.get('type'), 'value': definition.get('value')}
                                 if rect and rect.collidepoint(mouse_pos):
                                     actions.append((actions_cfg.ACTION_ROULETTE_BET, bet_info))
                                     clicked_on_bet_area = True
                                     break

                # --- Slots Specific Input ---
                # Check states where SPIN button is active
                elif current_state == states.STATE_SLOTS_IDLE or current_state == states.STATE_SLOTS_SHOWING_RESULT:
                    if layout_slots.SLOTS_SPIN_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_SLOTS_SPIN, None))
                    elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

                # Check state where SPIN button is inactive
                elif current_state == states.STATE_SLOTS_SPINNING:
                    # Allow returning to menu (will trigger confirmation via process_input)
                    if layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))


        return actions # Return the list of processed actions
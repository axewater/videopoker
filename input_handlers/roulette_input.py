import pygame
from typing import List, Optional, Tuple, Dict, Any

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_roulette as layout_roulette # Import layout which now contains definitions
import config_layout_general as layout_general

def handle_roulette_event(event: pygame.event.Event, current_state: str) -> List[Tuple[str, Optional[any]]]:
    """Handles input events for Roulette states."""
    actions = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

        # --- Betting State ---
        if current_state == states.STATE_ROULETTE_BETTING:
            clicked_on_bet_area = False
            # Check number bets (0-36)
            for number, rect in layout_roulette.ROULETTE_NUMBER_RECTS.items():
                if rect and rect.collidepoint(mouse_pos):
                    actions.append((actions_cfg.ACTION_ROULETTE_BET, {'type': 'number', 'value': number}))
                    clicked_on_bet_area = True
                    break # Process only one bet click

            # Check outside bets if no number was clicked
            if not clicked_on_bet_area:
                # Use the definitions from config_layout_roulette
                for bet_key, definition in layout_roulette.ROULETTE_OUTSIDE_BET_DEFINITIONS.items():
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

        # --- Spinning State ---
        elif current_state == states.STATE_ROULETTE_SPINNING:
            # Only allow returning to menu (will be handled in process_input)
            if layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                 actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

        # --- Result State ---
        elif current_state == states.STATE_ROULETTE_RESULT:
             # Allow clearing bets or returning to menu first
            if layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT and layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT.collidepoint(mouse_pos):
                 actions.append((actions_cfg.ACTION_ROULETTE_CLEAR_BETS, None))
            elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                 actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))
            # Also allow placing new bets immediately (acts like clear + place)
            else:
                clicked_on_bet_area = False
                # Check number bets
                for number, rect in layout_roulette.ROULETTE_NUMBER_RECTS.items():
                    if rect and rect.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_ROULETTE_BET, {'type': 'number', 'value': number}))
                        clicked_on_bet_area = True
                        break
                # Check outside bets
                if not clicked_on_bet_area:
                     # Use the definitions from config_layout_roulette
                     for bet_key, definition in layout_roulette.ROULETTE_OUTSIDE_BET_DEFINITIONS.items():
                         rect = definition.get('rect')
                         bet_info = {'type': definition.get('type'), 'value': definition.get('value')}
                         if rect and rect.collidepoint(mouse_pos):
                             actions.append((actions_cfg.ACTION_ROULETTE_BET, bet_info))
                             clicked_on_bet_area = True
                             break

    return actions

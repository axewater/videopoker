import pygame
from typing import List, Optional, Tuple

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_baccarat as layout_baccarat
import config_layout_general as layout_general
from baccarat_rules import BET_PLAYER, BET_BANKER, BET_TIE # Import bet types

def handle_baccarat_event(event: pygame.event.Event, current_state: str) -> List[Tuple[str, Optional[any]]]:
    """Handles input events for Baccarat states."""
    actions = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

        # Check betting areas and buttons only if in Betting or Result state
        if current_state in [states.STATE_BACCARAT_BETTING, states.STATE_BACCARAT_RESULT]:
            clicked_action_button = False
            # Check Action Buttons first (Deal, Clear, Menu)
            if layout_baccarat.BACCARAT_DEAL_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_BACCARAT_DEAL, None))
                clicked_action_button = True
            elif layout_baccarat.BACCARAT_CLEAR_BETS_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_BACCARAT_CLEAR_BETS, None))
                clicked_action_button = True
            elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))
                clicked_action_button = True

            # Check Betting Areas only if no action button was clicked
            if not clicked_action_button:
                if layout_baccarat.BACCARAT_BET_PLAYER_RECT.collidepoint(mouse_pos):
                    actions.append((actions_cfg.ACTION_BACCARAT_BET, {'type': BET_PLAYER}))
                elif layout_baccarat.BACCARAT_BET_BANKER_RECT.collidepoint(mouse_pos):
                    actions.append((actions_cfg.ACTION_BACCARAT_BET, {'type': BET_BANKER}))
                elif layout_baccarat.BACCARAT_BET_TIE_RECT.collidepoint(mouse_pos):
                    actions.append((actions_cfg.ACTION_BACCARAT_BET, {'type': BET_TIE}))

        # Allow Return to Menu from Dealing/Drawing states (handled by process_input)
        elif current_state in [states.STATE_BACCARAT_DEALING, states.STATE_BACCARAT_DRAWING]:
             if layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))


    return actions

import pygame
from typing import List, Optional, Tuple

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_cards as layout_cards
import config_layout_general as layout_general

def handle_poker_event(event: pygame.event.Event, current_state: str) -> List[Tuple[str, Optional[any]]]:
    """Handles input events for Draw Poker and Multi-Hand Poker states."""
    actions = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

        # Check Deal/Draw button first
        if layout_cards.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos):
            actions.append((actions_cfg.ACTION_DEAL_DRAW, None))
        # Check Return to Menu button next
        elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
            actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))
        # Only check cards/hold buttons if other buttons weren't clicked
        # and we are in a state where holding is allowed
        elif current_state in [states.STATE_DRAW_POKER_WAITING_FOR_HOLD, states.STATE_MULTI_POKER_WAITING_FOR_HOLD]:
            # Check card clicks
            card_clicked = False
            for i, card_rect in enumerate(layout_cards.CARD_RECTS):
                if card_rect.collidepoint(mouse_pos):
                    actions.append((actions_cfg.ACTION_HOLD_TOGGLE, i))
                    card_clicked = True
                    break # Process only one card click per event

            # Check hold button clicks (if card wasn't clicked)
            if not card_clicked:
                for i, hold_rect in enumerate(layout_cards.HOLD_BUTTON_RECTS):
                    if hold_rect.collidepoint(mouse_pos):
                        actions.append((actions_cfg.ACTION_HOLD_TOGGLE, i))
                        break # Process only one hold button click

    return actions

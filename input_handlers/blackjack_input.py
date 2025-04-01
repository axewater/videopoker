import pygame
from typing import List, Optional, Tuple

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_cards as layout_cards
import config_layout_general as layout_general

def handle_blackjack_event(event: pygame.event.Event, current_state: str) -> List[Tuple[str, Optional[any]]]:
    """Handles input events for Blackjack states."""
    actions = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

        # Player's Turn Actions
        if current_state == states.STATE_BLACKJACK_PLAYER_TURN:
            if layout_cards.BLACKJACK_HIT_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_BLACKJACK_HIT, None))
            elif layout_cards.BLACKJACK_STAND_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_BLACKJACK_STAND, None))
            elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

        # Idle or Result State Actions (Deal or Return)
        elif current_state in [states.STATE_BLACKJACK_IDLE, states.STATE_BLACKJACK_SHOWING_RESULT]:
            if layout_cards.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos): # Reuse Deal/Draw button layout
                actions.append((actions_cfg.ACTION_DEAL_DRAW, None)) # Use DEAL_DRAW action for consistency
            elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

    return actions

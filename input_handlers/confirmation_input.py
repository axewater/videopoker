import pygame
from typing import List, Optional, Tuple

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_general as layout_general

def handle_confirmation_event(event: pygame.event.Event, current_state: str) -> List[Tuple[str, Optional[any]]]:
    """Handles input events for the Confirmation Dialog state."""
    actions = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if current_state == states.STATE_CONFIRM_EXIT:
            if layout_general.CONFIRM_YES_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_CONFIRM_YES, None))
            elif layout_general.CONFIRM_NO_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_CONFIRM_NO, None))
    return actions

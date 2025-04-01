# /input_handlers/slots_input.py
import pygame
from typing import List, Optional, Tuple

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_slots as layout_slots
import config_layout_general as layout_general

def handle_slots_event(event: pygame.event.Event, current_state: str) -> List[Tuple[str, Optional[any]]]:
    """Handles input events for Slots states."""
    actions = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

        # Check states where SPIN button is active
        if current_state == states.STATE_SLOTS_IDLE or current_state == states.STATE_SLOTS_SHOWING_RESULT:
            if layout_slots.SLOTS_SPIN_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_SLOTS_SPIN, None))
            elif layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

        # Check state where SPIN button is inactive
        elif current_state == states.STATE_SLOTS_SPINNING:
            # Allow returning to menu (will trigger confirmation via process_input)
            if layout_general.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RETURN_TO_MENU, None))

    return actions

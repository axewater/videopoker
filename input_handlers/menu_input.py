import pygame
from typing import List, Optional, Tuple

# Config Imports
import config_states as states
import config_actions as actions_cfg
import config_layout_general as layout_general

def handle_menu_event(event: pygame.event.Event, current_state: str) -> List[Tuple[str, Optional[any]]]:
    """Handles input events for Top Menu, Game Selection, Settings, and Game Over states."""
    actions = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

        # --- Top Menu ---
        if current_state == states.STATE_TOP_MENU:
            if layout_general.PLAY_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_GOTO_PLAY, None))
            elif layout_general.SETTINGS_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_GOTO_SETTINGS, None))
            elif layout_general.TOP_MENU_QUIT_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_QUIT, None)) # Quit action handled directly here or triggers confirmation

        # --- Game Selection ---
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
            elif layout_general.SETTINGS_BACK_BUTTON_RECT.collidepoint(mouse_pos): # Back button
                actions.append((actions_cfg.ACTION_RETURN_TO_TOP_MENU, None))
            elif layout_general.RESTART_GAME_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RESTART_GAME, None))

        # --- Settings ---
        elif current_state == states.STATE_SETTINGS:
            if layout_general.SOUND_TOGGLE_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_TOGGLE_SOUND, None))
            elif layout_general.VOLUME_DOWN_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_VOLUME_DOWN, None))
            elif layout_general.VOLUME_UP_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_VOLUME_UP, None))
            elif layout_general.SETTINGS_BACK_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_RETURN_TO_TOP_MENU, None))

        # --- Game Over ---
        elif current_state == states.STATE_GAME_OVER:
            if layout_general.PLAY_AGAIN_BUTTON_RECT.collidepoint(mouse_pos):
                actions.append((actions_cfg.ACTION_PLAY_AGAIN, None)) # This action needs to be handled in process_input

    return actions

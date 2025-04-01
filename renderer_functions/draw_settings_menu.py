import pygame
from typing import Dict

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_settings_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], sound_enabled: bool):
    """Draws the settings menu screen."""
    surface.fill(constants.DARK_GREEN)

    # Title
    draw_text(surface, "Settings", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, 150, constants.GOLD, center=True)

    # Sound Toggle Button/Text
    sound_status = "ON" if sound_enabled else "OFF"
    sound_text = f"Sound Effects: {sound_status}"
    # Draw the text centered within the toggle rect
    draw_text(surface, sound_text, fonts['button'], constants.SOUND_TOGGLE_RECT.centerx, constants.SOUND_TOGGLE_RECT.centery, constants.WHITE, center=True)
    # Draw a border around the text to indicate it's clickable
    pygame.draw.rect(surface, constants.WHITE, constants.SOUND_TOGGLE_RECT, 2, border_radius=5)

    # Back Button
    draw_button(surface, fonts, "Back", constants.SETTINGS_BACK_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)

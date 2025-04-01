import pygame
from typing import Dict

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_top_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font]):
    """Draws the top-level main menu screen."""
    surface.fill(constants.DARK_GREEN)

    # Use draw_text with specific fonts
    draw_text(surface, "VIDEO POKER", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, 150, constants.GOLD, center=True)

    # Draw Buttons using draw_button
    draw_button(surface, fonts, "Play", constants.PLAY_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Settings", constants.SETTINGS_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Quit", constants.TOP_MENU_QUIT_BUTTON_RECT, constants.RED, constants.WHITE)

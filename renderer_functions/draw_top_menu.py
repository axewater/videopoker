# /renderer_functions/draw_top_menu.py
import pygame
from typing import Dict, Optional

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_top_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], backdrop_image: Optional[pygame.Surface] = None):
    """Draws the top-level main menu screen."""
    if backdrop_image:
        surface.blit(backdrop_image, (0, 0))
    else:
        surface.fill(constants.DARK_GREEN) # Fallback fill

    # Use draw_text with specific fonts and add outline
    draw_text(surface, "AceHigh Casino", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, 150, constants.GOLD, center=True, outline_color=constants.BLACK, outline_width=2) # Added outline parameters

    # Draw Buttons using draw_button
    draw_button(surface, fonts, "Play", constants.PLAY_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Settings", constants.SETTINGS_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Quit", constants.TOP_MENU_QUIT_BUTTON_RECT, constants.RED, constants.WHITE)


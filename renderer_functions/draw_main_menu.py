import pygame
from typing import Dict

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_main_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font]):
    """Draws the main menu screen."""
    surface.fill(constants.DARK_GREEN)

    # Use draw_text with specific fonts
    draw_text(surface, "VIDEO POKER", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, 100, constants.GOLD, center=True)
    draw_text(surface, "Choose your game:", fonts['message'], constants.SCREEN_WIDTH // 2, constants.MENU_BUTTON_Y_START - 50, constants.WHITE, center=True)

    # Draw Buttons using draw_button
    draw_button(surface, fonts, "Draw Poker", constants.DRAW_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Multi Poker", constants.MULTI_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "QUIT", constants.QUIT_BUTTON_RECT, constants.RED, constants.WHITE)

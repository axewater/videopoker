import pygame
from typing import Dict

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_game_selection_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font]):
    """Draws the game selection menu screen."""
    surface.fill(constants.DARK_GREEN)

    # Use draw_text with specific fonts
    # Title removed, assuming it's on the top menu
    draw_text(surface, "Choose your game:", fonts['message'], constants.SCREEN_WIDTH // 2, constants.GAME_SELECT_BUTTON_Y_START - 50, constants.WHITE, center=True)

    # Draw Buttons using draw_button
    draw_button(surface, fonts, "Draw Poker", constants.DRAW_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Multi Poker", constants.MULTI_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    # Quit button removed from here, use Return to Menu instead
    # Return to Top Menu Button
    draw_button(surface, fonts, "Back", constants.RETURN_TO_MENU_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)

# /renderer_functions/draw_game_selection_menu.py
import pygame
from typing import Dict, Optional

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_game_selection_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], current_money: int, backdrop_image: Optional[pygame.Surface] = None):
    """Draws the game selection menu screen."""
    if backdrop_image:
        surface.blit(backdrop_image, (0, 0))
    else:
        surface.fill(constants.DARK_GREEN) # Fallback fill

    # Title
    draw_text(surface, "Select Game", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, 80, constants.GOLD, center=True) # Adjusted Title Y

    # Display Current Money (Bank Account) - Top Right
    money_text = f"Bank: ${current_money}"
    draw_text(surface, money_text, fonts['money'], constants.SCREEN_WIDTH - 150, 20, constants.GOLD)

    # Draw Buttons - All use GREEN now
    draw_button(surface, fonts, "Draw Poker", constants.DRAW_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Multi Poker", constants.MULTI_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Blackjack", constants.BLACKJACK_BUTTON_RECT, constants.GREEN, constants.WHITE) # Changed color
    draw_button(surface, fonts, "Roulette", constants.ROULETTE_BUTTON_RECT, constants.GREEN, constants.WHITE) # Changed color
    draw_button(surface, fonts, "Slots", constants.SLOTS_BUTTON_RECT, constants.GREEN, constants.WHITE) # Added Slots button

    # Restart Game Button (use a distinct color like RED)
    draw_button(surface, fonts, "Restart", constants.RESTART_GAME_BUTTON_RECT, constants.RED, constants.WHITE)

    # Back Button (reuse settings back button rect/position)
    draw_button(surface, fonts, "Back", constants.SETTINGS_BACK_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE) # Keep Back button grey

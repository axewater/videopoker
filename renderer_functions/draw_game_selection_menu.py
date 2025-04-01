import pygame
from typing import Dict

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_game_selection_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], current_money: int):
    """Draws the game selection menu screen."""
    surface.fill(constants.DARK_GREEN)

    # Title
    draw_text(surface, "Select Game", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, 150, constants.GOLD, center=True)

    # Display Current Money (Bank Account) - Top Right
    money_text = f"Bank: ${current_money}"
    draw_text(surface, money_text, fonts['money'], constants.SCREEN_WIDTH - 150, 20, constants.GOLD)

    # Draw Buttons
    draw_button(surface, fonts, "Draw Poker", constants.DRAW_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    draw_button(surface, fonts, "Multi Poker", constants.MULTI_POKER_BUTTON_RECT, constants.GREEN, constants.WHITE)
    # Draw new game buttons (initially inactive/greyed out)
    draw_button(surface, fonts, "Blackjack", constants.BLACKJACK_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)
    draw_button(surface, fonts, "Roulette", constants.ROULETTE_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)

    # Back Button (reuse settings back button rect/position)
    draw_button(surface, fonts, "Back", constants.SETTINGS_BACK_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)

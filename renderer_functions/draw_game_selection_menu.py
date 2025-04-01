# /renderer_functions/draw_game_selection_menu.py
import pygame
from typing import Dict, Optional

import config_display as display
import config_colors as colors
import config_layout_general as layout_general
from .draw_text import draw_text
from .draw_button import draw_button

def draw_game_selection_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], current_money: int, backdrop_image: Optional[pygame.Surface] = None):
    """Draws the game selection menu screen."""
    if backdrop_image:
        surface.blit(backdrop_image, (0, 0))
    else:
        surface.fill(colors.DARK_GREEN) # Fallback fill

    # Title
    draw_text(surface, "Select Game", fonts['game_over_large'], display.SCREEN_WIDTH // 2, 80, colors.GOLD, center=True) # Adjusted Title Y

    # Display Current Money (Bank Account) - Top Right
    money_text = f"Bank: ${current_money}"
    draw_text(surface, money_text, fonts['money'], display.SCREEN_WIDTH - 150, 20, colors.GOLD)

    # Draw Buttons - All use GREEN now
    draw_button(surface, fonts, "Draw Poker", layout_general.DRAW_POKER_BUTTON_RECT, colors.GREEN, colors.WHITE)
    draw_button(surface, fonts, "Multi Poker", layout_general.MULTI_POKER_BUTTON_RECT, colors.GREEN, colors.WHITE)
    draw_button(surface, fonts, "Blackjack", layout_general.BLACKJACK_BUTTON_RECT, colors.GREEN, colors.WHITE) # Changed color
    draw_button(surface, fonts, "Roulette", layout_general.ROULETTE_BUTTON_RECT, colors.GREEN, colors.WHITE) # Changed color
    draw_button(surface, fonts, "Slots", layout_general.SLOTS_BUTTON_RECT, colors.GREEN, colors.WHITE) # Added Slots button
    draw_button(surface, fonts, "Baccarat", layout_general.BACCARAT_BUTTON_RECT, colors.GREEN, colors.WHITE) # Added Baccarat button

    # Restart Game Button (use a distinct color like RED)
    draw_button(surface, fonts, "Restart", layout_general.RESTART_GAME_BUTTON_RECT, colors.RED, colors.WHITE)

    # Back Button (reuse settings back button rect/position)
    draw_button(surface, fonts, "Back", layout_general.SETTINGS_BACK_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE) # Keep Back button grey

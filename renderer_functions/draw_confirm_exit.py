import pygame
from typing import Dict, Any

import config_display as display
import config_colors as colors
import config_layout_general as layout

from .draw_text import draw_text
from .draw_button import draw_button

def draw_confirm_exit(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], game_state: Dict[str, Any]):
    """Draws the confirmation dialog for exiting a hand."""
    # Draw a semi-transparent overlay (optional)
    overlay = pygame.Surface((display.SCREEN_WIDTH, display.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Black with alpha
    surface.blit(overlay, (0, 0))

    # Draw the confirmation box background
    pygame.draw.rect(surface, colors.DARK_GREEN, layout.CONFIRM_BOX_RECT, border_radius=10)
    pygame.draw.rect(surface, colors.WHITE, layout.CONFIRM_BOX_RECT, 2, border_radius=10) # Border

    # Draw the message based on the action type stored in game_state
    action_type = game_state.get('confirm_action_type')
    if action_type == 'RESTART':
        message = "Restart Game?"
        message2 = "Your current money will be lost."
    else: # Default to 'EXIT' or unknown
        message = "Abandon current game?"
        message2 = "(Hand will be lost)"

    draw_text(surface, message, fonts['message'], layout.CONFIRM_BOX_RECT.centerx, layout.CONFIRM_BOX_RECT.centery - 30, colors.WHITE, center=True)
    draw_text(surface, message2, fonts['pay_table'], layout.CONFIRM_BOX_RECT.centerx, layout.CONFIRM_BOX_RECT.centery, colors.YELLOW, center=True)

    # Draw Yes/No buttons
    draw_button(surface, fonts, "Yes", layout.CONFIRM_YES_BUTTON_RECT, colors.RED, colors.WHITE)
    draw_button(surface, fonts, "No", layout.CONFIRM_NO_BUTTON_RECT, colors.GREEN, colors.WHITE)

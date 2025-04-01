import pygame
from typing import Dict, Any

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_confirm_exit(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], game_state: Dict[str, Any]):
    """Draws the confirmation dialog for exiting a hand."""
    # Draw a semi-transparent overlay (optional)
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Black with alpha
    surface.blit(overlay, (0, 0))

    # Draw the confirmation box background
    pygame.draw.rect(surface, constants.DARK_GREEN, constants.CONFIRM_BOX_RECT, border_radius=10)
    pygame.draw.rect(surface, constants.WHITE, constants.CONFIRM_BOX_RECT, 2, border_radius=10) # Border

    # Draw the message based on the action type stored in game_state
    action_type = game_state.get('confirm_action_type')
    if action_type == 'RESTART':
        message = "Restart Game?"
        message2 = "Your current money will be lost."
    else: # Default to 'EXIT' or unknown
        message = "Abandon current game?"
        message2 = "(Hand will be lost)"

    draw_text(surface, message, fonts['message'], constants.CONFIRM_BOX_RECT.centerx, constants.CONFIRM_BOX_RECT.centery - 30, constants.WHITE, center=True)
    draw_text(surface, message2, fonts['pay_table'], constants.CONFIRM_BOX_RECT.centerx, constants.CONFIRM_BOX_RECT.centery, constants.YELLOW, center=True)

    # Draw Yes/No buttons
    draw_button(surface, fonts, "Yes", constants.CONFIRM_YES_BUTTON_RECT, constants.RED, constants.WHITE)
    draw_button(surface, fonts, "No", constants.CONFIRM_NO_BUTTON_RECT, constants.GREEN, constants.WHITE)

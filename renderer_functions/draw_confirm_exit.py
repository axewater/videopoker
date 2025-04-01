import pygame
from typing import Dict

import constants
from .draw_text import draw_text
from .draw_button import draw_button

def draw_confirm_exit(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font]):
    """Draws the confirmation dialog for exiting a hand."""
    # Draw a semi-transparent overlay (optional)
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Black with alpha
    surface.blit(overlay, (0, 0))

    # Draw the confirmation box background
    pygame.draw.rect(surface, constants.DARK_GREEN, constants.CONFIRM_BOX_RECT, border_radius=10)
    pygame.draw.rect(surface, constants.WHITE, constants.CONFIRM_BOX_RECT, 2, border_radius=10) # Border

    # Draw the message
    message = "Abandon current hand?"
    draw_text(surface, message, fonts['message'], constants.CONFIRM_BOX_RECT.centerx, constants.CONFIRM_BOX_RECT.centery - 30, constants.WHITE, center=True)
    message2 = "(Hand will be lost)"
    draw_text(surface, message2, fonts['pay_table'], constants.CONFIRM_BOX_RECT.centerx, constants.CONFIRM_BOX_RECT.centery, constants.YELLOW, center=True)


    # Draw Yes/No buttons
    draw_button(surface, fonts, "Yes", constants.CONFIRM_YES_BUTTON_RECT, constants.RED, constants.WHITE)
    draw_button(surface, fonts, "No", constants.CONFIRM_NO_BUTTON_RECT, constants.GREEN, constants.WHITE)

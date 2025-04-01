import pygame
from typing import List, Dict

import constants
from card import Card
from .get_card_image import get_card_image # Relative import

def draw_hand(surface: pygame.Surface, hand: List[Card], held_indices: List[int], card_images: Dict[str, pygame.Surface], fonts: Dict[str, pygame.font.Font]):
    """Draws the player's hand and the HOLD buttons below them."""
    hold_font = fonts['hold']
    for i, card in enumerate(hand):
        img = get_card_image(card, card_images)
        card_rect = constants.CARD_RECTS[i]
        surface.blit(img, card_rect)

        # Draw HOLD button below card
        hold_rect = constants.HOLD_BUTTON_RECTS[i]
        button_color = constants.BUTTON_ON if i in held_indices else constants.BUTTON_OFF
        pygame.draw.rect(surface, button_color, hold_rect, border_radius=5)

        # Draw HOLD text on the button
        hold_text_surface = hold_font.render("HOLD", True, constants.WHITE)
        text_rect = hold_text_surface.get_rect(center=hold_rect.center)
        surface.blit(hold_text_surface, text_rect)

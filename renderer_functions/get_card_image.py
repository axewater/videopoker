import pygame
from typing import Dict

import config_colors as colors
import config_layout_cards as layout_cards
from card import Card

def get_card_image(card: Card, card_images: Dict[str, pygame.Surface]) -> pygame.Surface:
    """Gets the pre-loaded image surface for a specific card."""
    suit_map = {"♠": "S", "♥": "H", "♦": "D", "♣": "C"}
    suit_short = suit_map.get(card.suit, '?')
    key = f"{card.rank}{suit_short}"

    if key not in card_images:
        print(f"Error: Image not found for card key: {key}")
        # Return a blank surface or a default 'back' image if available
        # Create a simple black rectangle as a fallback
        fallback_surface = pygame.Surface((layout_cards.CARD_WIDTH, layout_cards.CARD_HEIGHT))
        fallback_surface.fill(colors.BLACK)
        pygame.draw.rect(fallback_surface, colors.WHITE, fallback_surface.get_rect(), 1) # Add border
        return fallback_surface
    return card_images[key]

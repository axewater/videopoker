import pygame
from typing import Dict

import constants
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
        fallback_surface = pygame.Surface((constants.CARD_WIDTH, constants.CARD_HEIGHT))
        fallback_surface.fill(constants.BLACK)
        pygame.draw.rect(fallback_surface, constants.WHITE, fallback_surface.get_rect(), 1) # Add border
        return fallback_surface
    return card_images[key]

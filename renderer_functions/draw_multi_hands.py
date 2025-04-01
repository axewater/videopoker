import pygame
from typing import List, Tuple, Dict

import constants
from card import Card
from poker_rules import HandRank
from .get_card_image import get_card_image
from .draw_text import draw_text

def draw_multi_hands(surface: pygame.Surface, multi_hands: List[List[Card]], multi_results: List[Tuple[HandRank, str, int]], card_images: Dict[str, pygame.Surface], fonts: Dict[str, pygame.font.Font]):
    """Draws the multiple smaller hands above the main hand area."""
    card_width = constants.MULTI_CARD_WIDTH
    card_height = constants.MULTI_CARD_HEIGHT
    x_start = constants.MULTI_HAND_X_START
    card_spacing = constants.CARD_SPACING * constants.MULTI_HAND_CARD_SCALE

    result_font = fonts['multi_result']
    for hand_index, hand in enumerate(multi_hands):
        y_pos = constants.MULTI_HAND_Y_START + hand_index * constants.MULTI_HAND_Y_SPACING
        for card_index, card in enumerate(hand):
            img = get_card_image(card, card_images)
            scaled_img = pygame.transform.scale(img, (card_width, card_height))
            x = x_start + card_index * (card_width + card_spacing)
            surface.blit(scaled_img, (x, y_pos))

        # Draw individual hand results next to each hand with a background
        rank, name, payout = multi_results[hand_index]
        result_text = f"{name} ({payout}x)"
        text_x = x_start + 5 * (card_width + card_spacing) + 10 # Position to the right of the hand
        text_y = y_pos + card_height // 2 # Vertically centered with the cards
        padding = 3 # Padding around the text

        # Render text to get its size
        text_surface = result_font.render(result_text, True, constants.YELLOW)
        text_rect = text_surface.get_rect(midleft=(text_x, text_y)) # Align left edge vertically centered

        # Draw background rectangle
        bg_rect = text_rect.inflate(padding * 2, padding * 2) # Add padding
        pygame.draw.rect(surface, constants.BLACK, bg_rect, border_radius=3)

        # Draw text on top of the background
        surface.blit(text_surface, text_rect)

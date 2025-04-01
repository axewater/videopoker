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

    for hand_index, hand in enumerate(multi_hands):
        y_pos = constants.MULTI_HAND_Y_START + hand_index * constants.MULTI_HAND_Y_SPACING
        for card_index, card in enumerate(hand):
            img = get_card_image(card, card_images)
            scaled_img = pygame.transform.scale(img, (card_width, card_height))
            x = x_start + card_index * (card_width + card_spacing)
            surface.blit(scaled_img, (x, y_pos))
        # Optionally draw individual hand results next to each hand
        rank, name, payout = multi_results[hand_index]
        draw_text(surface, f"{name} ({payout}x)", fonts['multi_result'], x_start + 5 * (card_width + card_spacing) + 10, y_pos + card_height // 2, constants.YELLOW, center=False)

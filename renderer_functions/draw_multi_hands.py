# /renderer_functions/draw_multi_hands.py
import pygame
from typing import List, Tuple, Dict

# Removed: import constants
import config_layout_cards as layout_cards # Added
import config_colors as colors # Added
from card import Card
from poker_rules import HandRank
from .get_card_image import get_card_image
from .draw_text import draw_text

def draw_multi_hands(surface: pygame.Surface, multi_hands: List[List[Card]], multi_results: List[Tuple[HandRank, str, int]], card_images: Dict[str, pygame.Surface], fonts: Dict[str, pygame.font.Font]):
    """Draws the multiple smaller hands above the main hand area."""
    # Updated constants references
    card_width = layout_cards.MULTI_CARD_WIDTH
    card_height = layout_cards.MULTI_CARD_HEIGHT
    x_start = layout_cards.MULTI_HAND_X_START
    card_spacing = layout_cards.CARD_SPACING * layout_cards.MULTI_HAND_CARD_SCALE

    result_font = fonts['multi_result']
    for hand_index, hand in enumerate(multi_hands):
        # Updated constants references
        y_pos = layout_cards.MULTI_HAND_Y_START + hand_index * layout_cards.MULTI_HAND_Y_SPACING
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
        # Updated constants references
        text_surface = result_font.render(result_text, True, colors.YELLOW)
        text_rect = text_surface.get_rect(midleft=(text_x, text_y)) # Align left edge vertically centered

        # Draw background rectangle
        bg_rect = text_rect.inflate(padding * 2, padding * 2) # Add padding
        # Updated constants references
        pygame.draw.rect(surface, colors.BLACK, bg_rect, border_radius=3)

        # Draw text on top of the background
        surface.blit(text_surface, text_rect)


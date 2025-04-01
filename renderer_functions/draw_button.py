import pygame
from typing import Tuple, Dict

from .draw_text import draw_text # Relative import

def draw_button(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], text: str, rect: pygame.Rect, color: Tuple[int, int, int], text_color: Tuple[int, int, int]):
    """Draws a button with text."""
    pygame.draw.rect(surface, color, rect, border_radius=5)
    # Use the specific font for buttons
    button_font = fonts.get('button')
    if not button_font:
        print("Warning: Button font not found, using fallback.")
        button_font = fonts['message'] # Fallback

    draw_text(surface, text, button_font, rect.centerx, rect.centery, text_color, center=True)

import pygame
from typing import Tuple, Dict

def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font, x: int, y: int, color: Tuple[int, int, int], center: bool = False):
    """Draws text using a pre-loaded font."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

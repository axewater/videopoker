# /renderer_functions/draw_text.py
import pygame
from typing import Tuple, Dict, Optional

def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font, x: int, y: int, color: Tuple[int, int, int], center: bool = False, outline_color: Optional[Tuple[int, int, int]] = None, outline_width: int = 1):
    """Draws text using a pre-loaded font, with an optional outline."""
    
    # Render the main text surface
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    # Set position based on center flag
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    # Draw outline if specified
    if outline_color and outline_width > 0:
        # Render the outline text surface
        outline_surface = font.render(text, True, outline_color)
        # Draw the outline by blitting the outline surface multiple times offset slightly
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0: # Don't draw outline in the exact center
                    continue
                outline_rect = outline_surface.get_rect()
                if center:
                    outline_rect.center = (x + dx, y + dy)
                else:
                    outline_rect.topleft = (x + dx, y + dy)
                surface.blit(outline_surface, outline_rect)

    # Draw the main text on top
    surface.blit(text_surface, text_rect)


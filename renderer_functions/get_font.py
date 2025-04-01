import pygame
from typing import Optional

def get_font(size: int, font_name: Optional[str] = None) -> pygame.font.Font:
    """Helper to load fonts."""
    # Initialize font module if not already done (safe to call multiple times)
    if not pygame.font.get_init():
        pygame.font.init()
    return pygame.font.Font(pygame.font.match_font(font_name) if font_name else None, size)

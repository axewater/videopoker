# /renderer_functions/draw_settings_menu.py
import pygame
from typing import Dict, Optional

# Removed: import constants
import config_colors as colors # Added
import config_display as display # Added
import config_layout_general as layout # Added
from .draw_text import draw_text
from .draw_button import draw_button

def draw_settings_menu(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], sound_enabled: bool, volume_level: float, backdrop_image: Optional[pygame.Surface] = None):
    """Draws the settings menu screen."""
    if backdrop_image:
        surface.blit(backdrop_image, (0, 0))
    else:
        # Updated constants reference
        surface.fill(colors.DARK_GREEN) # Fallback fill

    # Title
    # Updated constants references
    draw_text(surface, "Settings", fonts['game_over_large'], display.SCREEN_WIDTH // 2, 150, colors.GOLD, center=True)

    # Sound Toggle Button/Text
    sound_status = "ON" if sound_enabled else "OFF"
    sound_text = f"Sound: {sound_status}"
    # Draw the text centered within the toggle rect
    # Updated constants references
    draw_text(surface, sound_text, fonts['button'], layout.SOUND_TOGGLE_RECT.centerx, layout.SOUND_TOGGLE_RECT.centery, colors.WHITE, center=True)
    # Draw a border around the text to indicate it's clickable
    # Updated constants references
    pygame.draw.rect(surface, colors.WHITE, layout.SOUND_TOGGLE_RECT, 2, border_radius=5)

    # Volume Controls (only if sound is enabled)
    if sound_enabled:
        # Updated constants references
        button_color = colors.GREEN
        text_color = colors.WHITE
        # Draw Volume Down Button
        # Updated constants references
        draw_button(surface, fonts, "-", layout.VOLUME_DOWN_BUTTON_RECT, button_color, text_color)
        # Draw Volume Up Button
        # Updated constants references
        draw_button(surface, fonts, "+", layout.VOLUME_UP_BUTTON_RECT, button_color, text_color)
        # Draw Volume Level Display (e.g., "Volume: 70%")
        volume_percent = int(volume_level * 100)
        volume_text = f"Volume: {volume_percent}%"
        # Position volume text below the Sound toggle
        # Updated constants references
        text_y = layout.SOUND_TOGGLE_RECT.bottom + 30
        draw_text(surface, volume_text, fonts['message'], display.SCREEN_WIDTH // 2, text_y, colors.WHITE, center=True)

    # Back Button
    # Updated constants references
    draw_button(surface, fonts, "Back", layout.SETTINGS_BACK_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE)


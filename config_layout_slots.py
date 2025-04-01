# /config_layout_slots.py
"""
Configuration constants for Slots game layout and elements.
Requires pygame for Rect definition.
Imports other config modules for dependencies.
"""
import pygame
import config_display as display
import config_layout_general as layout_general

# --- Slots Constants ---
NUM_REELS = 3 # Number of reels
SLOT_SYMBOL_WIDTH = 90 # Width of each symbol image (was 120)
SLOT_SYMBOL_HEIGHT = 75 # Height of each symbol image (was 100)

# Spin Button Position (Positioned like Deal/Draw)
SLOTS_SPIN_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - layout_general.BUTTON_WIDTH // 2 + 60, # Adjusted for centering
    display.SCREEN_HEIGHT - layout_general.BUTTON_HEIGHT - 50, # Position near bottom center
    layout_general.BUTTON_WIDTH,
    layout_general.BUTTON_HEIGHT
)

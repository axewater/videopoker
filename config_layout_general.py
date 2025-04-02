# /config_layout_general.py
"""
Configuration constants for general UI layout elements (buttons, dialogs).
Requires pygame for Rect definition.
"""
import pygame
import config_display as display

# Button Dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

# Top Menu Button Rectangles
TOP_MENU_BUTTON_Y_START = display.SCREEN_HEIGHT // 2 - 80
TOP_MENU_BUTTON_SPACING = 20
PLAY_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    TOP_MENU_BUTTON_Y_START,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
SETTINGS_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    TOP_MENU_BUTTON_Y_START + BUTTON_HEIGHT + TOP_MENU_BUTTON_SPACING,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
TOP_MENU_QUIT_BUTTON_RECT = pygame.Rect( # Separate Quit for Top Menu positioning
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    TOP_MENU_BUTTON_Y_START + 2 * (BUTTON_HEIGHT + TOP_MENU_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Game Selection Menu Button Rectangles (Previously Main Menu)
GAME_SELECT_BUTTON_Y_START = display.SCREEN_HEIGHT // 2 - 150 # Adjusted start position higher
GAME_SELECT_BUTTON_SPACING = 15 # Reduced spacing slightly
DRAW_POKER_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
MULTI_POKER_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 1 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
BLACKJACK_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 2 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
ROULETTE_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 3 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
SLOTS_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 4 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
BACCARAT_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 5 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Restart Game Button Rectangle (Position bottom-right on Game Select, mirroring Back button)
RESTART_GAME_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH - BUTTON_WIDTH - 20, # Position from right edge
    display.SCREEN_HEIGHT - BUTTON_HEIGHT - 20, # Position from bottom edge
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Quit Button Rectangle (Not used on Top Menu, maybe elsewhere?)
QUIT_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH - BUTTON_WIDTH - 20,
    display.SCREEN_HEIGHT - BUTTON_HEIGHT - 20,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Settings Menu Rectangles
SETTINGS_BACK_BUTTON_RECT = pygame.Rect(
    20, display.SCREEN_HEIGHT - BUTTON_HEIGHT - 20, # Bottom-left
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
SOUND_TOGGLE_RECT = pygame.Rect( # Area for sound toggle text/button
    display.SCREEN_WIDTH // 2 - 100, display.SCREEN_HEIGHT // 2 - 25, 200, 50
)
# Volume Control Rectangles (relative to SOUND_TOGGLE_RECT)
VOLUME_BUTTON_WIDTH = 40
VOLUME_BUTTON_HEIGHT = 40
VOLUME_DOWN_BUTTON_RECT = pygame.Rect(
    SOUND_TOGGLE_RECT.left - VOLUME_BUTTON_WIDTH - 10, SOUND_TOGGLE_RECT.centery - VOLUME_BUTTON_HEIGHT // 2, VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_HEIGHT
)
VOLUME_UP_BUTTON_RECT = pygame.Rect(
    SOUND_TOGGLE_RECT.right + 10, SOUND_TOGGLE_RECT.centery - VOLUME_BUTTON_HEIGHT // 2, VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_HEIGHT
)

# Confirmation Dialog Rectangles
CONFIRM_BOX_RECT = pygame.Rect(display.SCREEN_WIDTH // 4, display.SCREEN_HEIGHT // 3, display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 3)
CONFIRM_YES_BUTTON_RECT = pygame.Rect(
    CONFIRM_BOX_RECT.centerx - BUTTON_WIDTH - 10, CONFIRM_BOX_RECT.bottom - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT
)
CONFIRM_NO_BUTTON_RECT = pygame.Rect(
    CONFIRM_BOX_RECT.centerx + 10, CONFIRM_BOX_RECT.bottom - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT
)

# Play Again Button Rectangle (for Game Over state)
PLAY_AGAIN_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    display.SCREEN_HEIGHT // 2 + 50,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Return to Menu Button (Used in multiple game screens)
# Positioned bottom left, slightly wider
RETURN_TO_MENU_BUTTON_RECT = pygame.Rect(
    20, display.SCREEN_HEIGHT - BUTTON_HEIGHT - 50, # Align Y with Spin/Clear/Deal buttons approx
    BUTTON_WIDTH + 30, # Slightly wider for text
    BUTTON_HEIGHT
)

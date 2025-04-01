# /config_layout_cards.py
"""
Configuration constants for Poker and Blackjack card/button layouts.
Requires pygame for Rect definition.
Imports other config modules for dependencies.
"""
import pygame
import config_display as display
import config_layout_general as layout_general

# Card and spacing dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 145
CARD_SPACING = 10
HOLD_BUTTON_HEIGHT = 40
HOLD_BUTTON_SPACING = 5

# Calculate single hand positioning
HAND_Y_POS = 250
HAND_X_START = (display.SCREEN_WIDTH - 5 * (CARD_WIDTH + CARD_SPACING)) // 2

# Multi-Hand Constants
NUM_MULTI_HANDS = 3
MULTI_HAND_CARD_SCALE = 0.8 # Scale factor for multi-hand cards (optional)
MULTI_CARD_WIDTH = int(CARD_WIDTH * MULTI_HAND_CARD_SCALE)
MULTI_CARD_HEIGHT = int(CARD_HEIGHT * MULTI_HAND_CARD_SCALE)
MULTI_HAND_Y_START = 50 # Y position for the top multi-hand
MULTI_HAND_Y_SPACING = MULTI_CARD_HEIGHT + 15 # Vertical space between multi-hands
MULTI_HAND_X_START = (display.SCREEN_WIDTH - 5 * (MULTI_CARD_WIDTH + CARD_SPACING * MULTI_HAND_CARD_SCALE)) // 2

# Card Rectangles (calculated here for potential use in multiple modules)
CARD_RECTS = []
for i in range(5):
    x = HAND_X_START + i * (CARD_WIDTH + CARD_SPACING)
    rect = pygame.Rect(x, HAND_Y_POS, CARD_WIDTH, CARD_HEIGHT)
    CARD_RECTS.append(rect)

# Pay Table Position
PAY_TABLE_X = 20
PAY_TABLE_Y = 20
PAY_TABLE_MULTI_X = display.SCREEN_WIDTH - 250 # Position pay table to the right in multi-mode

# Hold Button Rectangles (derived from CARD_RECTS)
HOLD_BUTTON_RECTS = []
for card_rect in CARD_RECTS:
     hold_rect = pygame.Rect(
         card_rect.x,
         card_rect.bottom + HOLD_BUTTON_SPACING,
         CARD_WIDTH,
         HOLD_BUTTON_HEIGHT
     )
     HOLD_BUTTON_RECTS.append(hold_rect)

# Deal/Draw Button Rectangle (Poker)
DEAL_DRAW_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - layout_general.BUTTON_WIDTH // 2,
    HAND_Y_POS + CARD_HEIGHT + HOLD_BUTTON_HEIGHT + 40,
    layout_general.BUTTON_WIDTH,
    layout_general.BUTTON_HEIGHT
)

# Blackjack Button Rectangles (Positioned near Deal/Draw)
BLACKJACK_BUTTON_Y = DEAL_DRAW_BUTTON_RECT.y
BLACKJACK_HIT_BUTTON_RECT = pygame.Rect(
    DEAL_DRAW_BUTTON_RECT.left - layout_general.BUTTON_WIDTH - 20, # Left of Deal/Draw
    BLACKJACK_BUTTON_Y,
    layout_general.BUTTON_WIDTH,
    layout_general.BUTTON_HEIGHT
)
BLACKJACK_STAND_BUTTON_RECT = pygame.Rect(
    DEAL_DRAW_BUTTON_RECT.right + 20, # Right of Deal/Draw
    BLACKJACK_BUTTON_Y,
    layout_general.BUTTON_WIDTH,
    layout_general.BUTTON_HEIGHT
)

# /config_layout_baccarat.py
"""
Configuration constants for Baccarat game layout and elements.
Requires pygame for Rect definition.
Imports other config modules for dependencies.
"""
import pygame
import config_display as display
import config_layout_general as layout_general
import config_layout_cards as layout_cards # For card dimensions

# --- Card Positions ---
# Player Hand
PLAYER_HAND_Y = display.SCREEN_HEIGHT // 2 + 30
PLAYER_HAND_X_START = display.SCREEN_WIDTH // 2 - layout_cards.CARD_WIDTH * 1.5 - layout_cards.CARD_SPACING * 1.0 # Centered-ish left
PLAYER_CARD_RECTS = [
    pygame.Rect(PLAYER_HAND_X_START + i * (layout_cards.CARD_WIDTH + layout_cards.CARD_SPACING), PLAYER_HAND_Y, layout_cards.CARD_WIDTH, layout_cards.CARD_HEIGHT)
    for i in range(3) # Max 3 cards
]

# Banker Hand
BANKER_HAND_Y = PLAYER_HAND_Y
BANKER_HAND_X_START = display.SCREEN_WIDTH // 2 + layout_cards.CARD_WIDTH * 0.5 + layout_cards.CARD_SPACING * 1.0 # Centered-ish right
BANKER_CARD_RECTS = [
    pygame.Rect(BANKER_HAND_X_START + i * (layout_cards.CARD_WIDTH + layout_cards.CARD_SPACING), BANKER_HAND_Y, layout_cards.CARD_WIDTH, layout_cards.CARD_HEIGHT)
    for i in range(3) # Max 3 cards
]

# --- Betting Areas ---
BET_AREA_WIDTH = 180
BET_AREA_HEIGHT = 80
BET_AREA_Y = PLAYER_HAND_Y - BET_AREA_HEIGHT - 40 # Above hands
BET_AREA_SPACING = 30

# Calculate total width needed for 3 betting areas + spacing
total_bet_area_width = 3 * BET_AREA_WIDTH + 2 * BET_AREA_SPACING
bet_area_x_start = (display.SCREEN_WIDTH - total_bet_area_width) // 2

BACCARAT_BET_PLAYER_RECT = pygame.Rect(
    bet_area_x_start,
    BET_AREA_Y,
    BET_AREA_WIDTH,
    BET_AREA_HEIGHT
)
BACCARAT_BET_TIE_RECT = pygame.Rect(
    bet_area_x_start + BET_AREA_WIDTH + BET_AREA_SPACING,
    BET_AREA_Y,
    BET_AREA_WIDTH,
    BET_AREA_HEIGHT
)
BACCARAT_BET_BANKER_RECT = pygame.Rect(
    bet_area_x_start + 2 * (BET_AREA_WIDTH + BET_AREA_SPACING),
    BET_AREA_Y,
    BET_AREA_WIDTH,
    BET_AREA_HEIGHT
)

# --- Chip Position within Bet Area ---
CHIP_OFFSET_Y = 15 # Offset from top of bet area
CHIP_RADIUS = 15

# --- Action Buttons ---
# Use positions similar to Blackjack/Poker
BACCARAT_DEAL_BUTTON_RECT = pygame.Rect(
    display.SCREEN_WIDTH // 2 - layout_general.BUTTON_WIDTH // 2,
    display.SCREEN_HEIGHT - layout_general.BUTTON_HEIGHT - 50, # Same Y as other deal buttons
    layout_general.BUTTON_WIDTH,
    layout_general.BUTTON_HEIGHT
)
BACCARAT_CLEAR_BETS_BUTTON_RECT = pygame.Rect(
    BACCARAT_DEAL_BUTTON_RECT.left - layout_general.BUTTON_WIDTH - 20, # Left of Deal
    BACCARAT_DEAL_BUTTON_RECT.y,
    layout_general.BUTTON_WIDTH,
    layout_general.BUTTON_HEIGHT
)

# --- Text Positions ---
PLAYER_VALUE_TEXT_Y = PLAYER_HAND_Y + layout_cards.CARD_HEIGHT + 20
BANKER_VALUE_TEXT_Y = BANKER_HAND_Y + layout_cards.CARD_HEIGHT + 20
RESULT_TEXT_Y = BET_AREA_Y - 50 # Above betting areas
MESSAGE_TEXT_Y = display.SCREEN_HEIGHT - 150 # Near bottom, above buttons

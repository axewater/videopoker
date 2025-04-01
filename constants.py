import pygame

# Display dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Card and spacing dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 145
CARD_SPACING = 10
HOLD_BUTTON_HEIGHT = 40
HOLD_BUTTON_SPACING = 5

# Calculate single hand positioning
HAND_Y_POS = 250
HAND_X_START = (SCREEN_WIDTH - 5 * (CARD_WIDTH + CARD_SPACING)) // 2

# Multi-Hand Constants
NUM_MULTI_HANDS = 3
MULTI_HAND_CARD_SCALE = 0.8 # Scale factor for multi-hand cards (optional)
MULTI_CARD_WIDTH = int(CARD_WIDTH * MULTI_HAND_CARD_SCALE)
MULTI_CARD_HEIGHT = int(CARD_HEIGHT * MULTI_HAND_CARD_SCALE)
MULTI_HAND_Y_START = 50 # Y position for the top multi-hand
MULTI_HAND_Y_SPACING = MULTI_CARD_HEIGHT + 15 # Vertical space between multi-hands

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
GOLD = (218, 165, 32)
YELLOW = (255, 255, 0) # For highlighting
DARK_GREEN = (0, 100, 0)
BUTTON_OFF = (100, 100, 100)
BUTTON_ON = (255, 215, 0) # Goldish color for held button

# Game States
STATE_MAIN_MENU = "MAIN_MENU"
STATE_DRAW_POKER_DEALING = "DRAW_POKER_DEALING" # Optional: Could add animation later
STATE_DRAW_POKER_WAITING_FOR_HOLD = "DRAW_POKER_WAITING_FOR_HOLD"
STATE_DRAW_POKER_DRAWING = "DRAW_POKER_DRAWING" # Optional: Could add animation later
STATE_DRAW_POKER_SHOWING_RESULT = "DRAW_POKER_SHOWING_RESULT"
# Multi Poker States
STATE_MULTI_POKER_WAITING_FOR_HOLD = "MULTI_POKER_WAITING_FOR_HOLD"
STATE_MULTI_POKER_DRAWING = "MULTI_POKER_DRAWING" # Optional animation state
STATE_MULTI_POKER_SHOWING_RESULT = "MULTI_POKER_SHOWING_RESULT"
STATE_GAME_OVER = "GAME_OVER"

# Font Sizes
MONEY_FONT_SIZE = 30
MESSAGE_FONT_SIZE = 28
PAY_TABLE_FONT_SIZE = 20
BUTTON_FONT_SIZE = 30
RESULT_FONT_SIZE = 36
MULTI_RESULT_FONT_SIZE = 20 # Smaller font for individual hand results
HOLD_FONT_SIZE = 24

# Animation Constants
MONEY_ANIMATION_DURATION = 60 # Frames (e.g., 2 seconds at 30 FPS)
MONEY_ANIMATION_OFFSET_Y = 30 # Pixels below the main money display

# Button Dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

# Asset Paths
CARD_ASSET_PATH = "assets/cards"

# Sound Asset Paths
SOUND_ASSET_PATH = "assets/sounds"
SOUND_FILES = {
    "deal": "deal.mp3", "draw": "draw.mp3", "hold": "hold.mp3",
    "win": "win.mp3", "lose": "lose.mp3", "button": "button.mp3"
}

# Card Rectangles (calculated here for potential use in multiple modules)
CARD_RECTS = []
for i in range(5):
    x = HAND_X_START + i * (CARD_WIDTH + CARD_SPACING)
    rect = pygame.Rect(x, HAND_Y_POS, CARD_WIDTH, CARD_HEIGHT)
    CARD_RECTS.append(rect)

# Multi-Hand Card Rectangles (calculated dynamically in Renderer based on hand index)
# We define the starting position and spacing here.
MULTI_HAND_X_START = (SCREEN_WIDTH - 5 * (MULTI_CARD_WIDTH + CARD_SPACING * MULTI_HAND_CARD_SCALE)) // 2

# Pay Table Position (might need adjustment for multi-hand)
PAY_TABLE_X = 20
PAY_TABLE_Y = 20
PAY_TABLE_MULTI_X = SCREEN_WIDTH - 250 # Position pay table to the right in multi-mode

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

# Deal/Draw Button Rectangle
DEAL_DRAW_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    HAND_Y_POS + CARD_HEIGHT + HOLD_BUTTON_HEIGHT + 40,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Main Menu Button Rectangles
MENU_BUTTON_Y_START = SCREEN_HEIGHT // 2 - 50
MENU_BUTTON_SPACING = 20
DRAW_POKER_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    MENU_BUTTON_Y_START,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
MULTI_POKER_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    MENU_BUTTON_Y_START + BUTTON_HEIGHT + MENU_BUTTON_SPACING,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Quit Button Rectangle
QUIT_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH - BUTTON_WIDTH - 20,
    SCREEN_HEIGHT - BUTTON_HEIGHT - 20,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
# Return to Menu Button Rectangle (Position top-left or similar)
RETURN_TO_MENU_BUTTON_RECT = pygame.Rect(
    20, SCREEN_HEIGHT - BUTTON_HEIGHT - 20, # Bottom-left
    BUTTON_WIDTH + 30, # Slightly wider for text
    BUTTON_HEIGHT
)

# Play Again Button Rectangle (for Game Over state)
PLAY_AGAIN_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    SCREEN_HEIGHT // 2 + 50,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Input Actions (returned by InputHandler)
ACTION_QUIT = "QUIT"
ACTION_DEAL_DRAW = "DEAL_DRAW"
ACTION_PLAY_AGAIN = "PLAY_AGAIN"
ACTION_CHOOSE_DRAW_POKER = "CHOOSE_DRAW_POKER"
ACTION_CHOOSE_MULTI_POKER = "CHOOSE_MULTI_POKER"
ACTION_RETURN_TO_MENU = "RETURN_TO_MENU"
ACTION_HOLD_TOGGLE = "HOLD_TOGGLE" # Payload will be the index (0-4)

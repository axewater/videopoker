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

# Calculate hand positioning
HAND_Y_POS = 250
HAND_X_START = (SCREEN_WIDTH - 5 * (CARD_WIDTH + CARD_SPACING)) // 2

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
GOLD = (218, 165, 32)
DARK_GREEN = (0, 100, 0)
BUTTON_OFF = (100, 100, 100)
BUTTON_ON = (255, 215, 0) # Goldish color for held button

# Game States
STATE_START_MENU = "START_MENU"
STATE_DEALING = "DEALING" # Optional: Could add animation later
STATE_WAITING_FOR_HOLD = "WAITING_FOR_HOLD"
STATE_DRAWING = "DRAWING" # Optional: Could add animation later
STATE_SHOWING_RESULT = "SHOWING_RESULT"
STATE_GAME_OVER = "GAME_OVER"

# Font Sizes
MONEY_FONT_SIZE = 30
MESSAGE_FONT_SIZE = 28
PAY_TABLE_FONT_SIZE = 20
BUTTON_FONT_SIZE = 30
RESULT_FONT_SIZE = 36
HOLD_FONT_SIZE = 24

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

# Quit Button Rectangle
QUIT_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH - BUTTON_WIDTH - 20,
    SCREEN_HEIGHT - BUTTON_HEIGHT - 20,
    BUTTON_WIDTH,
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
ACTION_HOLD_TOGGLE = "HOLD_TOGGLE" # Payload will be the index (0-4)

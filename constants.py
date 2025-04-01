# /constants.py
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
GREY = (128, 128, 128) # Added for wheel drawing

# Game States
STATE_TOP_MENU = "TOP_MENU" # New top-level menu
STATE_GAME_SELECTION = "GAME_SELECTION" # Renamed from STATE_MAIN_MENU
STATE_SETTINGS = "SETTINGS" # New settings screen
STATE_DRAW_POKER_IDLE = "DRAW_POKER_IDLE" # Before first deal
STATE_DRAW_POKER_DEALING = "DRAW_POKER_DEALING" # Optional: Could add animation later
STATE_DRAW_POKER_WAITING_FOR_HOLD = "DRAW_POKER_WAITING_FOR_HOLD"
STATE_DRAW_POKER_DRAWING = "DRAW_POKER_DRAWING" # Optional: Could add animation later
STATE_DRAW_POKER_SHOWING_RESULT = "DRAW_POKER_SHOWING_RESULT"
# Multi Poker States
STATE_MULTI_POKER_IDLE = "MULTI_POKER_IDLE" # Before first deal
STATE_MULTI_POKER_WAITING_FOR_HOLD = "MULTI_POKER_WAITING_FOR_HOLD"
STATE_MULTI_POKER_DRAWING = "MULTI_POKER_DRAWING" # Optional animation state
STATE_MULTI_POKER_SHOWING_RESULT = "MULTI_POKER_SHOWING_RESULT"
STATE_GAME_OVER = "GAME_OVER"
STATE_CONFIRM_EXIT = "CONFIRM_EXIT" # New state for exit confirmation
STATE_BLACKJACK_IDLE = "BLACKJACK_IDLE" # Before bet/deal
STATE_BLACKJACK_PLAYER_TURN = "BLACKJACK_PLAYER_TURN"
STATE_BLACKJACK_DEALER_TURN = "BLACKJACK_DEALER_TURN" # Dealer plays out
STATE_BLACKJACK_SHOWING_RESULT = "BLACKJACK_SHOWING_RESULT"
# Roulette States
STATE_ROULETTE_BETTING = "ROULETTE_BETTING"
STATE_ROULETTE_SPINNING = "ROULETTE_SPINNING" # Includes pause phase now
STATE_ROULETTE_RESULT = "ROULETTE_RESULT"
STATE_SLOTS_IDLE = "SLOTS_IDLE" # Placeholder for slots

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
# ROULETTE_SPIN_DURATION = 90 # Frames (e.g., 3 seconds at 30 FPS) for spin animation
ROULETTE_SPIN_DURATION = 180 # Increased duration (e.g., 6 seconds at 30 FPS)
ROULETTE_RESULT_PAUSE_DURATION = 30 # Frames to pause after spin (e.g., 1 second at 30 FPS)
ROULETTE_FLASH_COUNT = 3 # Number of times the winning slot flashes
ROULETTE_FLASH_INTERVAL = 10 # Frames for one flash state (on/off) - Total flash cycle = 2*INTERVAL
MONEY_ANIMATION_OFFSET_Y = 30 # Pixels below the main money display
RESULT_FLASH_DURATION = 45 # Frames (e.g., 1.5 seconds at 30 FPS)
RESULT_FLASH_INTERVAL = 5 # Frames between toggling visibility

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

# Roulette Constants (Initial Setup)
ROULETTE_WHEEL_NUMBERS = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
ROULETTE_RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
ROULETTE_BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
ROULETTE_GREEN_NUMBER = {0}

# Roulette Colors
ROULETTE_COLOR_RED = (200, 0, 0)
ROULETTE_COLOR_BLACK = (50, 50, 50) # Dark grey for black numbers
ROULETTE_COLOR_GREEN = (0, 150, 0)
ROULETTE_TABLE_COLOR = (0, 100, 0) # Dark green table
ROULETTE_CHIP_COLOR = (255, 255, 0) # Yellow chips for now
ROULETTE_CHIP_RADIUS = 10
ROULETTE_CHIP_TEXT_COLOR = BLACK
ROULETTE_FLASH_COLOR = YELLOW # Color for flashing winning slot

# Roulette Layout Constants
ROULETTE_GRID_X_START = 50 # Adjusted for more space
ROULETTE_GRID_Y_START = 100 # Adjusted for more space
ROULETTE_NUM_BOX_WIDTH = 45 # Slightly wider boxes
ROULETTE_NUM_BOX_HEIGHT = 45 # Slightly taller boxes
ROULETTE_GRID_SPACING = 4
ROULETTE_NUM_COLS = 12
ROULETTE_NUM_ROWS = 3

# --- Calculate Roulette Rects ---
ROULETTE_NUMBER_RECTS = {}
# Zero (Aligned with top of grid, spans 3 rows)
zero_x = ROULETTE_GRID_X_START
zero_y = ROULETTE_GRID_Y_START # Align top with number grid
zero_width = ROULETTE_NUM_BOX_WIDTH # Same width as number boxes
zero_height = ROULETTE_NUM_BOX_HEIGHT * ROULETTE_NUM_ROWS + ROULETTE_GRID_SPACING * (ROULETTE_NUM_ROWS - 1)
ROULETTE_NUMBER_RECTS[0] = pygame.Rect(zero_x, zero_y, zero_width, zero_height)

# Numbers 1-36 (3 rows, 12 columns)
number = 1
for col in range(ROULETTE_NUM_COLS):
    for row in range(ROULETTE_NUM_ROWS):
        # Numbers go 3, 2, 1 vertically in each column
        current_number = (col * ROULETTE_NUM_ROWS) + (ROULETTE_NUM_ROWS - row)
        if current_number > 36: continue

        rect_x = ROULETTE_GRID_X_START + zero_width + ROULETTE_GRID_SPACING + col * (ROULETTE_NUM_BOX_WIDTH + ROULETTE_GRID_SPACING)
        rect_y = ROULETTE_GRID_Y_START + row * (ROULETTE_NUM_BOX_HEIGHT + ROULETTE_GRID_SPACING)
        ROULETTE_NUMBER_RECTS[current_number] = pygame.Rect(rect_x, rect_y, ROULETTE_NUM_BOX_WIDTH, ROULETTE_NUM_BOX_HEIGHT)

# Outside Bets
outside_bet_height = BUTTON_HEIGHT # Standard height for outside bets

# --- Outside Bet Rects ---
# Dozen Bets (Below numbers, spanning 4 number boxes each)
dozen_width = 4 * (ROULETTE_NUM_BOX_WIDTH + ROULETTE_GRID_SPACING) - ROULETTE_GRID_SPACING
dozen_y = ROULETTE_GRID_Y_START + ROULETTE_NUM_ROWS * (ROULETTE_NUM_BOX_HEIGHT + ROULETTE_GRID_SPACING) + ROULETTE_GRID_SPACING
ROULETTE_BET_DOZEN1_RECT = pygame.Rect(ROULETTE_NUMBER_RECTS[1].left, dozen_y, dozen_width, outside_bet_height)
ROULETTE_BET_DOZEN2_RECT = pygame.Rect(ROULETTE_NUMBER_RECTS[13].left, dozen_y, dozen_width, outside_bet_height)
ROULETTE_BET_DOZEN3_RECT = pygame.Rect(ROULETTE_NUMBER_RECTS[25].left, dozen_y, dozen_width, outside_bet_height)

# Column Bets (Right of numbers, spanning 1 number box vertically each)
col_width = ROULETTE_NUM_BOX_WIDTH # Make width same as number box
col_height = ROULETTE_NUM_BOX_HEIGHT # Height for one row
col_x = ROULETTE_NUMBER_RECTS[36].right + ROULETTE_GRID_SPACING
# Align each column bet with its corresponding row
ROULETTE_BET_COL1_RECT = pygame.Rect(col_x, ROULETTE_NUMBER_RECTS[3].top, col_width, col_height) # Aligns with row containing 3, 6, ... 36
ROULETTE_BET_COL2_RECT = pygame.Rect(col_x, ROULETTE_NUMBER_RECTS[2].top, col_width, col_height) # Aligns with row containing 2, 5, ... 35
ROULETTE_BET_COL3_RECT = pygame.Rect(col_x, ROULETTE_NUMBER_RECTS[1].top, col_width, col_height) # Aligns with row containing 1, 4, ... 34

# Even Money Bets (Below Dozens, spanning 2 number boxes each)
even_money_y = dozen_y + outside_bet_height + ROULETTE_GRID_SPACING
# Total width of the number grid part (12 cols)
total_number_grid_width = 12 * (ROULETTE_NUM_BOX_WIDTH + ROULETTE_GRID_SPACING) - ROULETTE_GRID_SPACING
# Divide total width by 6 for the six even money bets
even_money_width = total_number_grid_width // 6

# Calculate starting x based on the first dozen bet's left edge
even_money_x_start = ROULETTE_BET_DOZEN1_RECT.left

ROULETTE_BET_LOW_RECT = pygame.Rect(even_money_x_start, even_money_y, even_money_width, outside_bet_height)
ROULETTE_BET_EVEN_RECT = pygame.Rect(even_money_x_start + even_money_width, even_money_y, even_money_width, outside_bet_height)
ROULETTE_BET_RED_RECT = pygame.Rect(even_money_x_start + 2 * even_money_width, even_money_y, even_money_width, outside_bet_height)
ROULETTE_BET_BLACK_RECT = pygame.Rect(even_money_x_start + 3 * even_money_width, even_money_y, even_money_width, outside_bet_height)
ROULETTE_BET_ODD_RECT = pygame.Rect(even_money_x_start + 4 * even_money_width, even_money_y, even_money_width, outside_bet_height)
ROULETTE_BET_HIGH_RECT = pygame.Rect(even_money_x_start + 5 * even_money_width, even_money_y, even_money_width, outside_bet_height)


# Spin Button Position (Example - Bottom Right)
spin_button_x = SCREEN_WIDTH - BUTTON_WIDTH - 50
spin_button_y = SCREEN_HEIGHT - BUTTON_HEIGHT - 50
ROULETTE_SPIN_BUTTON_RECT = pygame.Rect(spin_button_x, spin_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

# Clear Bets Button
ROULETTE_CLEAR_BETS_BUTTON_RECT = pygame.Rect(spin_button_x - BUTTON_WIDTH - 20, spin_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

# Return to Menu Button (Moved up slightly to avoid overlap)
RETURN_TO_MENU_BUTTON_RECT = pygame.Rect(
    20, spin_button_y, # Align Y with Spin/Clear buttons
    BUTTON_WIDTH + 30, # Slightly wider for text
    BUTTON_HEIGHT
)

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

# Blackjack Button Rectangles (Positioned near Deal/Draw)
BLACKJACK_BUTTON_Y = DEAL_DRAW_BUTTON_RECT.y
BLACKJACK_HIT_BUTTON_RECT = pygame.Rect(
    DEAL_DRAW_BUTTON_RECT.left - BUTTON_WIDTH - 20, # Left of Deal/Draw
    BLACKJACK_BUTTON_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
BLACKJACK_STAND_BUTTON_RECT = pygame.Rect(
    DEAL_DRAW_BUTTON_RECT.right + 20, # Right of Deal/Draw
    BLACKJACK_BUTTON_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Top Menu Button Rectangles
TOP_MENU_BUTTON_Y_START = SCREEN_HEIGHT // 2 - 80
TOP_MENU_BUTTON_SPACING = 20
PLAY_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    TOP_MENU_BUTTON_Y_START,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
SETTINGS_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    TOP_MENU_BUTTON_Y_START + BUTTON_HEIGHT + TOP_MENU_BUTTON_SPACING,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
TOP_MENU_QUIT_BUTTON_RECT = pygame.Rect( # Separate Quit for Top Menu positioning
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    TOP_MENU_BUTTON_Y_START + 2 * (BUTTON_HEIGHT + TOP_MENU_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Game Selection Menu Button Rectangles (Previously Main Menu)
GAME_SELECT_BUTTON_Y_START = SCREEN_HEIGHT // 2 - 150 # Adjusted start position higher
GAME_SELECT_BUTTON_SPACING = 15 # Reduced spacing slightly
DRAW_POKER_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
MULTI_POKER_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 1 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
# New Game Buttons
BLACKJACK_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 2 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
ROULETTE_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 3 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
SLOTS_BUTTON_RECT = pygame.Rect( # New Slots Button
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    GAME_SELECT_BUTTON_Y_START + 4 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING),
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)


# Restart Game Button Rectangle (Position bottom-center on Game Select)
RESTART_GAME_BUTTON_RECT = pygame.Rect(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, # Centered horizontally
    GAME_SELECT_BUTTON_Y_START + 5 * (BUTTON_HEIGHT + GAME_SELECT_BUTTON_SPACING) + 20, # Below Slots button
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

# Settings Menu Rectangles
SETTINGS_BACK_BUTTON_RECT = pygame.Rect(
    20, SCREEN_HEIGHT - BUTTON_HEIGHT - 20, # Bottom-left
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
SOUND_TOGGLE_RECT = pygame.Rect( # Area for sound toggle text/button
    SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50
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
CONFIRM_BOX_RECT = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
CONFIRM_YES_BUTTON_RECT = pygame.Rect(
    CONFIRM_BOX_RECT.centerx - BUTTON_WIDTH - 10, CONFIRM_BOX_RECT.bottom - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT
)
CONFIRM_NO_BUTTON_RECT = pygame.Rect(
    CONFIRM_BOX_RECT.centerx + 10, CONFIRM_BOX_RECT.bottom - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT
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
# Top Menu Actions
ACTION_GOTO_PLAY = "GOTO_PLAY"
ACTION_GOTO_SETTINGS = "GOTO_SETTINGS"
# Game Selection Actions
ACTION_CHOOSE_DRAW_POKER = "CHOOSE_DRAW_POKER"
ACTION_CHOOSE_MULTI_POKER = "CHOOSE_MULTI_POKER"
ACTION_CHOOSE_BLACKJACK = "CHOOSE_BLACKJACK" # New action
ACTION_CHOOSE_ROULETTE = "CHOOSE_ROULETTE" # New action
ACTION_CHOOSE_SLOTS = "CHOOSE_SLOTS" # New action for slots
ACTION_RESTART_GAME = "RESTART_GAME" # New action for restarting money
ACTION_RETURN_TO_MENU = "RETURN_TO_MENU"
ACTION_HOLD_TOGGLE = "HOLD_TOGGLE" # Payload will be the index (0-4)
# Settings Actions
ACTION_TOGGLE_SOUND = "TOGGLE_SOUND"
ACTION_RETURN_TO_TOP_MENU = "RETURN_TO_TOP_MENU" # From Settings
ACTION_VOLUME_UP = "VOLUME_UP"
ACTION_VOLUME_DOWN = "VOLUME_DOWN"
# Confirmation Actions
ACTION_CONFIRM_YES = "CONFIRM_YES"
ACTION_CONFIRM_NO = "CONFIRM_NO"
# Blackjack Actions
ACTION_BLACKJACK_HIT = "BLACKJACK_HIT"
ACTION_BLACKJACK_STAND = "BLACKJACK_STAND"
# Roulette Actions
ACTION_ROULETTE_BET = "ROULETTE_BET" # Payload will be bet details dict
ACTION_ROULETTE_SPIN = "ROULETTE_SPIN"
ACTION_ROULETTE_CLEAR_BETS = "ROULETTE_CLEAR_BETS" # Added action constant

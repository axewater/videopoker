# /config_layout_roulette.py
"""
Configuration constants for Roulette game layout and elements.
Requires pygame for Rect definition.
Imports other config modules for dependencies.
"""
import pygame
import config_display as display
import config_layout_general as layout_general
import config_colors as colors
from typing import Dict, Any

# Roulette Constants (Initial Setup)
ROULETTE_WHEEL_NUMBERS = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
ROULETTE_RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
ROULETTE_BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
ROULETTE_GREEN_NUMBER = {0}

# Roulette Layout Constants
ROULETTE_CHIP_RADIUS = 10
ROULETTE_GRID_X_START = 50 # Adjusted for more space
ROULETTE_GRID_Y_START = 100 # Adjusted for more space
ROULETTE_NUM_BOX_WIDTH = 45 # Slightly wider boxes
ROULETTE_NUM_BOX_HEIGHT = 45 # Slightly taller boxes
ROULETTE_GRID_SPACING = 4
ROULETTE_NUM_COLS = 12
ROULETTE_NUM_ROWS = 3

# --- Wheel and Ball Animation Constants ---
WHEEL_CENTER_X = display.SCREEN_WIDTH // 2
WHEEL_CENTER_Y = display.SCREEN_HEIGHT // 2
WHEEL_PERSPECTIVE_RATIO = 0.6 # How much shorter the vertical radius is for ellipse effect

# Radii for drawing (Horizontal - Vertical will be calculated using perspective ratio)
RIM_OUTER_RADIUS = min(WHEEL_CENTER_X, WHEEL_CENTER_Y) - 50 # Absolute outer edge
RIM_THICKNESS = 15
RIM_INNER_RADIUS = RIM_OUTER_RADIUS - RIM_THICKNESS
TRACK_OUTER_RADIUS = RIM_INNER_RADIUS # Ball track starts inside the rim
TRACK_INNER_RADIUS = TRACK_OUTER_RADIUS - 40 # Inner edge of the ball track area
NUMBER_AREA_OUTER_RADIUS = TRACK_INNER_RADIUS # Numbers start inside the track
NUMBER_AREA_INNER_RADIUS = NUMBER_AREA_OUTER_RADIUS - 60 # Inner edge of the number pockets, near the hub
HUB_RADIUS = NUMBER_AREA_INNER_RADIUS - 10 # Radius of the central hub structure

BALL_START_TRACK_RADIUS = TRACK_OUTER_RADIUS - 5 # Ball starts near outer edge of track
BALL_END_TRACK_RADIUS = TRACK_INNER_RADIUS + 5 # Ball settles near inner edge of track
BALL_RADIUS = 6
BALL_COLOR = colors.WHITE
BALL_SHADOW_COLOR = (50, 50, 50, 150) # Semi-transparent shadow
BALL_SHADOW_OFFSET = 2

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
outside_bet_height = layout_general.BUTTON_HEIGHT # Standard height for outside bets

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

# --- Outside Bet Definitions (for input handling) ---
# Dictionary mapping bet keys to their properties (rect, type, value)
ROULETTE_OUTSIDE_BET_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    'dozen_1': {'rect': ROULETTE_BET_DOZEN1_RECT, 'type': 'dozen', 'value': '1'},
    'dozen_2': {'rect': ROULETTE_BET_DOZEN2_RECT, 'type': 'dozen', 'value': '2'},
    'dozen_3': {'rect': ROULETTE_BET_DOZEN3_RECT, 'type': 'dozen', 'value': '3'},
    'column_1': {'rect': ROULETTE_BET_COL1_RECT, 'type': 'column', 'value': '1'},
    'column_2': {'rect': ROULETTE_BET_COL2_RECT, 'type': 'column', 'value': '2'},
    'column_3': {'rect': ROULETTE_BET_COL3_RECT, 'type': 'column', 'value': '3'},
    'half_low': {'rect': ROULETTE_BET_LOW_RECT, 'type': 'half', 'value': 'low'},
    'parity_even': {'rect': ROULETTE_BET_EVEN_RECT, 'type': 'parity', 'value': 'even'},
    'color_red': {'rect': ROULETTE_BET_RED_RECT, 'type': 'color', 'value': 'red'},
    'color_black': {'rect': ROULETTE_BET_BLACK_RECT, 'type': 'color', 'value': 'black'},
    'parity_odd': {'rect': ROULETTE_BET_ODD_RECT, 'type': 'parity', 'value': 'odd'},
    'half_high': {'rect': ROULETTE_BET_HIGH_RECT, 'type': 'half', 'value': 'high'},
}

# Spin Button Position (Example - Bottom Right)
spin_button_x = display.SCREEN_WIDTH - layout_general.BUTTON_WIDTH - 50
spin_button_y = display.SCREEN_HEIGHT - layout_general.BUTTON_HEIGHT - 50
ROULETTE_SPIN_BUTTON_RECT = pygame.Rect(spin_button_x, spin_button_y, layout_general.BUTTON_WIDTH, layout_general.BUTTON_HEIGHT)

# Clear Bets Button
ROULETTE_CLEAR_BETS_BUTTON_RECT = pygame.Rect(spin_button_x - layout_general.BUTTON_WIDTH - 20, spin_button_y, layout_general.BUTTON_WIDTH, layout_general.BUTTON_HEIGHT)

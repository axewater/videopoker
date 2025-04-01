# /renderer_functions/draw_roulette_screen.py
import pygame
from typing import Dict, List, Optional, Tuple, Any

import constants
from game_state import GameState
from .draw_text import draw_text
from .draw_button import draw_button

# --- Helper function to get number color ---
def get_number_color(number: int) -> Tuple[int, int, int]:
    """Returns the Pygame color for a given roulette number."""
    if number == 0:
        return constants.ROULETTE_COLOR_GREEN
    elif number in constants.ROULETTE_RED_NUMBERS:
        return constants.ROULETTE_COLOR_RED
    elif number in constants.ROULETTE_BLACK_NUMBERS:
        return constants.ROULETTE_COLOR_BLACK
    else:
        return constants.WHITE # Should not happen for 0-36

def draw_roulette_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], game_state: Dict, game_state_manager: GameState):
    """Draws the Roulette game screen."""
    surface.fill(constants.ROULETTE_TABLE_COLOR)

    bets: Dict[str, int] = game_state.get('roulette_bets', {})
    current_state = game_state.get('current_state')
    message = game_state.get('message', '')
    result_message = game_state.get('result_message', '')
    winning_number = game_state.get('roulette_winning_number', None) # Get winning number if available

    chip_font = fonts['pay_table'] # Use a smaller font for chip text
    number_font = fonts['button'] # Font for numbers in boxes

    # --- Draw Money ---
    money_text = f"Money: ${game_state_manager.money}"
    draw_text(surface, money_text, fonts['money'], constants.SCREEN_WIDTH - 150, 20, constants.GOLD) # Top right

    # --- Draw Betting Grid ---

    # Draw 0
    zero_rect = constants.ROULETTE_NUMBER_RECTS.get(0)
    if zero_rect:
        pygame.draw.rect(surface, constants.ROULETTE_COLOR_GREEN, zero_rect)
        pygame.draw.rect(surface, constants.WHITE, zero_rect, 1) # Border
        draw_text(surface, "0", number_font, zero_rect.centerx, zero_rect.centery, constants.WHITE, center=True)
        # Draw chip if bet exists
        bet_key = "number_0"
        if bet_key in bets:
            pygame.draw.circle(surface, constants.ROULETTE_CHIP_COLOR, zero_rect.center, constants.ROULETTE_CHIP_RADIUS)
            draw_text(surface, str(bets[bet_key]), chip_font, zero_rect.centerx, zero_rect.centery, constants.ROULETTE_CHIP_TEXT_COLOR, center=True)
        # Highlight winning number 0
        if winning_number == 0:
            pygame.draw.rect(surface, constants.YELLOW, zero_rect, 3) # Draw yellow border

    # Draw numbers 1-36
    for number in range(1, 37):
        rect = constants.ROULETTE_NUMBER_RECTS.get(number)
        if rect:
            color = get_number_color(number)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, constants.WHITE, rect, 1) # Border
            # Use white text for red/black, black text for green/yellow background
            text_color = constants.BLACK if color in [constants.ROULETTE_COLOR_GREEN, constants.YELLOW] else constants.WHITE

            bet_key = f"number_{number}"
            if bet_key in bets:
                 pygame.draw.circle(surface, constants.ROULETTE_CHIP_COLOR, rect.center, constants.ROULETTE_CHIP_RADIUS)
                 draw_text(surface, str(bets[bet_key]), chip_font, rect.centerx, rect.centery, constants.ROULETTE_CHIP_TEXT_COLOR, center=True)
            else:
                 draw_text(surface, str(number), number_font, rect.centerx, rect.centery, text_color, center=True)

            # Highlight winning number
            if number == winning_number and winning_number is not None:
                 pygame.draw.rect(surface, constants.YELLOW, rect, 3) # Draw yellow border

    # --- Draw Outside Bets ---
    # Helper to draw outside bet areas and chips
    def draw_outside_bet(bet_key: str, rect: Optional[pygame.Rect], text: str, color: Tuple[int, int, int]):
        if rect:
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, constants.WHITE, rect, 1) # Border
            draw_text(surface, text, fonts['pay_table'], rect.centerx, rect.centery, constants.WHITE, center=True)
            if bet_key in bets:
                # Slightly offset chip position to avoid covering text completely, if needed
                chip_pos = rect.center
                pygame.draw.circle(surface, constants.ROULETTE_CHIP_COLOR, chip_pos, constants.ROULETTE_CHIP_RADIUS)
                draw_text(surface, str(bets[bet_key]), chip_font, chip_pos[0], chip_pos[1], constants.ROULETTE_CHIP_TEXT_COLOR, center=True)

    # Draw Dozens
    draw_outside_bet("dozen_1", constants.ROULETTE_BET_DOZEN1_RECT, "1st 12", constants.ROULETTE_COLOR_GREEN)
    draw_outside_bet("dozen_2", constants.ROULETTE_BET_DOZEN2_RECT, "2nd 12", constants.ROULETTE_COLOR_GREEN)
    draw_outside_bet("dozen_3", constants.ROULETTE_BET_DOZEN3_RECT, "3rd 12", constants.ROULETTE_COLOR_GREEN)

    # Draw Columns (Using "2:1" text as requested, centered)
    draw_outside_bet("column_3", constants.ROULETTE_BET_COL3_RECT, "2:1", constants.ROULETTE_COLOR_GREEN) # Corresponds to top row numbers (1, 4, ...)
    draw_outside_bet("column_2", constants.ROULETTE_BET_COL2_RECT, "2:1", constants.ROULETTE_COLOR_GREEN) # Corresponds to middle row numbers (2, 5, ...)
    draw_outside_bet("column_1", constants.ROULETTE_BET_COL1_RECT, "2:1", constants.ROULETTE_COLOR_GREEN) # Corresponds to bottom row numbers (3, 6, ...)

    # Draw Even Money Bets
    draw_outside_bet("half_low", constants.ROULETTE_BET_LOW_RECT, "1-18", constants.ROULETTE_COLOR_GREEN)
    draw_outside_bet("parity_even", constants.ROULETTE_BET_EVEN_RECT, "EVEN", constants.ROULETTE_COLOR_GREEN)
    draw_outside_bet("color_red", constants.ROULETTE_BET_RED_RECT, "RED", constants.ROULETTE_COLOR_RED)
    draw_outside_bet("color_black", constants.ROULETTE_BET_BLACK_RECT, "BLACK", constants.ROULETTE_COLOR_BLACK)
    draw_outside_bet("parity_odd", constants.ROULETTE_BET_ODD_RECT, "ODD", constants.ROULETTE_COLOR_GREEN)
    draw_outside_bet("half_high", constants.ROULETTE_BET_HIGH_RECT, "19-36", constants.ROULETTE_COLOR_GREEN)

    # --- Draw Buttons ---
    can_spin = len(bets) > 0 # Can spin if any bet is placed (affordability checked in process_input)
    spin_button_color = constants.GREEN if can_spin else constants.BUTTON_OFF

    if current_state == constants.STATE_ROULETTE_BETTING:
        draw_button(surface, fonts, "SPIN", constants.ROULETTE_SPIN_BUTTON_RECT, spin_button_color, constants.WHITE)
        clear_button_color = constants.RED if len(bets) > 0 else constants.BUTTON_OFF
        draw_button(surface, fonts, "Clear Bets", constants.ROULETTE_CLEAR_BETS_BUTTON_RECT, clear_button_color, constants.WHITE)
    elif current_state == constants.STATE_ROULETTE_SPINNING:
        draw_button(surface, fonts, "Spinning...", constants.ROULETTE_SPIN_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)
        # Hide Clear Bets during spin
    elif current_state == constants.STATE_ROULETTE_RESULT:
        # Show SPIN as disabled, allow Clear Bets or placing new bets (handled by input)
        draw_button(surface, fonts, "SPIN", constants.ROULETTE_SPIN_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)
        clear_button_color = constants.RED # Always allow clear after result if bets were placed
        draw_button(surface, fonts, "Clear Bets", constants.ROULETTE_CLEAR_BETS_BUTTON_RECT, clear_button_color, constants.WHITE)

    # --- Draw Messages ---
    if message:
        draw_text(surface, message, fonts['message'], constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 100, constants.WHITE, center=True)
    if result_message:
        # Position result message near the top-center
        draw_text(surface, result_message, fonts['result'], constants.SCREEN_WIDTH // 2, 60, constants.GOLD, center=True)

    # --- Draw Return to Menu Button ---
    draw_button(surface, fonts, "Game Menu", constants.RETURN_TO_MENU_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)


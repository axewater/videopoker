# /renderer_functions/draw_roulette_screen.py
import pygame
from typing import Dict, List, Optional, Tuple, Any

import config_display as display
import config_animations as animations
import config_layout_roulette as layout_roulette
import config_colors as colors
import config_states as states
import config_layout_general as layout_general
from game_state import GameState
from .draw_text import draw_text
from .draw_button import draw_button
from .draw_spinning_wheel import draw_spinning_wheel, get_number_color

def draw_roulette_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], game_state: Dict, game_state_manager: GameState):
    """Draws the Roulette game screen."""
    surface.fill(colors.ROULETTE_TABLE_COLOR)

    bets: Dict[str, int] = game_state.get('roulette_bets', {})
    current_state = game_state.get('current_state')
    message = game_state.get('message', '')
    result_message = game_state.get('result_message', '')
    winning_number = game_state.get('roulette_winning_number', None)
    spin_timer = game_state.get('roulette_spin_timer', 0)
    pause_timer = game_state.get('roulette_pause_timer', 0)

    chip_font = fonts['pay_table']
    number_font = fonts['button']

    # --- Draw Money ---
    money_text = f"Money: ${game_state_manager.money}"
    draw_text(surface, money_text, fonts['money'], display.SCREEN_WIDTH - 150, 20, colors.GOLD)

    # --- Draw Spinning Wheel OR Betting Grid ---
    if current_state == states.STATE_ROULETTE_SPINNING:
        draw_spinning_wheel(surface, fonts, game_state)
    else:
        # Draw Betting Grid
        # Draw 0
        zero_rect = layout_roulette.ROULETTE_NUMBER_RECTS.get(0)
        if zero_rect:
            pygame.draw.rect(surface, colors.ROULETTE_COLOR_GREEN, zero_rect)
            pygame.draw.rect(surface, colors.WHITE, zero_rect, 1)
            draw_text(surface, "0", number_font, zero_rect.centerx, zero_rect.centery, colors.WHITE, center=True)
            # Draw chip if bet exists
            bet_key = "number_0"
            if bet_key in bets:
                pygame.draw.circle(surface, colors.ROULETTE_CHIP_COLOR, zero_rect.center, layout_roulette.ROULETTE_CHIP_RADIUS)
                draw_text(surface, str(bets[bet_key]), chip_font, zero_rect.centerx, zero_rect.centery, colors.ROULETTE_CHIP_TEXT_COLOR, center=True)
            # Highlight winning number 0 (Only in RESULT state)
            if current_state == states.STATE_ROULETTE_RESULT and winning_number == 0:
                pygame.draw.rect(surface, colors.YELLOW, zero_rect, 3)

        # Draw numbers 1-36
        for number in range(1, 37):
            rect = layout_roulette.ROULETTE_NUMBER_RECTS.get(number)
            if rect:
                color = get_number_color(number)
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, colors.WHITE, rect, 1)
                text_color = colors.WHITE

                bet_key = f"number_{number}"
                if bet_key in bets:
                     pygame.draw.circle(surface, colors.ROULETTE_CHIP_COLOR, rect.center, layout_roulette.ROULETTE_CHIP_RADIUS)
                     draw_text(surface, str(bets[bet_key]), chip_font, rect.centerx, rect.centery, colors.ROULETTE_CHIP_TEXT_COLOR, center=True)
                else:
                     draw_text(surface, str(number), number_font, rect.centerx, rect.centery, text_color, center=True)

                # Highlight winning number (Only in RESULT state)
                if current_state == states.STATE_ROULETTE_RESULT and number == winning_number:
                     pygame.draw.rect(surface, colors.YELLOW, rect, 3)

        # --- Draw Outside Bets ---
        def draw_outside_bet(bet_key: str, rect: Optional[pygame.Rect], text: str, color: Tuple[int, int, int]):
            if rect:
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, colors.WHITE, rect, 1)
                draw_text(surface, text, fonts['pay_table'], rect.centerx, rect.centery, colors.WHITE, center=True)
                if bet_key in bets:
                    chip_pos = rect.center
                    pygame.draw.circle(surface, colors.ROULETTE_CHIP_COLOR, chip_pos, layout_roulette.ROULETTE_CHIP_RADIUS)
                    draw_text(surface, str(bets[bet_key]), chip_font, chip_pos[0], chip_pos[1], colors.ROULETTE_CHIP_TEXT_COLOR, center=True)

        draw_outside_bet("dozen_1", layout_roulette.ROULETTE_BET_DOZEN1_RECT, "1st 12", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("dozen_2", layout_roulette.ROULETTE_BET_DOZEN2_RECT, "2nd 12", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("dozen_3", layout_roulette.ROULETTE_BET_DOZEN3_RECT, "3rd 12", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("column_3", layout_roulette.ROULETTE_BET_COL3_RECT, "2:1", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("column_2", layout_roulette.ROULETTE_BET_COL2_RECT, "2:1", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("column_1", layout_roulette.ROULETTE_BET_COL1_RECT, "2:1", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("half_low", layout_roulette.ROULETTE_BET_LOW_RECT, "1-18", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("parity_even", layout_roulette.ROULETTE_BET_EVEN_RECT, "EVEN", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("color_red", layout_roulette.ROULETTE_BET_RED_RECT, "RED", colors.ROULETTE_COLOR_RED)
        draw_outside_bet("color_black", layout_roulette.ROULETTE_BET_BLACK_RECT, "BLACK", colors.ROULETTE_COLOR_BLACK)
        draw_outside_bet("parity_odd", layout_roulette.ROULETTE_BET_ODD_RECT, "ODD", colors.ROULETTE_COLOR_GREEN)
        draw_outside_bet("half_high", layout_roulette.ROULETTE_BET_HIGH_RECT, "19-36", colors.ROULETTE_COLOR_GREEN)

    # --- Draw Buttons (Logic depends on state) ---
    can_spin = len(bets) > 0
    spin_button_color = colors.GREEN if can_spin else colors.BUTTON_OFF

    if current_state == states.STATE_ROULETTE_BETTING:
        draw_button(surface, fonts, "SPIN", layout_roulette.ROULETTE_SPIN_BUTTON_RECT, spin_button_color, colors.WHITE)
        clear_button_color = colors.RED if len(bets) > 0 else colors.BUTTON_OFF
        draw_button(surface, fonts, "Clear Bets", layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT, clear_button_color, colors.WHITE)
    elif current_state == states.STATE_ROULETTE_SPINNING:
        # Hide buttons during spin and pause phases
        pass
    elif current_state == states.STATE_ROULETTE_RESULT:
        # Show SPIN as disabled, allow Clear Bets or placing new bets
        draw_button(surface, fonts, "SPIN", layout_roulette.ROULETTE_SPIN_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE)
        clear_button_color = colors.RED
        draw_button(surface, fonts, "Clear Bets", layout_roulette.ROULETTE_CLEAR_BETS_BUTTON_RECT, clear_button_color, colors.WHITE)

    # --- Draw Messages ---
    if current_state != states.STATE_ROULETTE_SPINNING:
        if message:
            draw_text(surface, message, fonts['message'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT - 100, colors.WHITE, center=True)
        if result_message:
            draw_text(surface, result_message, fonts['result'], display.SCREEN_WIDTH // 2, 60, colors.GOLD, center=True)

    # --- Draw Return to Menu Button (Visible except during spin/pause) ---
    if current_state != states.STATE_ROULETTE_SPINNING:
         draw_button(surface, fonts, "Game Menu", layout_general.RETURN_TO_MENU_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE)

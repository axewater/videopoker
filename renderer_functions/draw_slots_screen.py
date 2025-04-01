# /renderer_functions/draw_slots_screen.py
import pygame
import random
from typing import Dict, List, Optional, Any

import constants
from game_state import GameState
from slots_rules import REEL_STRIPS, SLOTS_PAYOUTS, BAR_SYMBOLS # Need rules for display
from .draw_text import draw_text
from .draw_button import draw_button

# --- Constants for Slots Layout ---
SLOT_SYMBOL_WIDTH = 120 # Width of each symbol image
SLOT_SYMBOL_HEIGHT = 100 # Height of each symbol image
REEL_X_START = (constants.SCREEN_WIDTH - constants.NUM_REELS * SLOT_SYMBOL_WIDTH) // 2
REEL_Y_POS = 150 # Y position for the payline (center of symbols)
REEL_SPACING = 10 # Horizontal space between reels (if needed, currently adjacent)
VISIBLE_ROWS = 3 # How many symbols are visible vertically per reel
PAYLINE_Y_OFFSET = (VISIBLE_ROWS // 2) * SLOT_SYMBOL_HEIGHT # Offset to draw the central payline symbol

# --- Paytable Display Constants ---
PAYTABLE_X = 20  # Adjusted X position further left
PAYTABLE_Y = 20  # Adjusted Y position further up
PAYTABLE_LINE_HEIGHT = 25
PAYTABLE_COL_WIDTH = 150

def draw_slots_paytable(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font]):
    """Draws a simplified payout table for the slots game."""
    font = fonts['pay_table']
    x = PAYTABLE_X
    y = PAYTABLE_Y
    line_height = PAYTABLE_LINE_HEIGHT

    draw_text(surface, "--- Payouts (Bet: 1) ---", font, x, y, constants.GOLD)
    y += line_height * 1.5

    # Define payouts to display (can be selective)
    payouts_to_show = [
        (("7", "7", "7"), "Triple 7s"),
        (("bell", "bell", "bell"), "Triple Bells"),
        (("3bar", "3bar", "3bar"), "Triple 3-Bar"),
        (("2bar", "2bar", "2bar"), "Triple 2-Bar"),
        (("1bar", "1bar", "1bar"), "Triple 1-Bar"),
        (("bar", "bar", "bar"), "Any 3 Bars"), # Special case text
        (("cherry", "cherry", "cherry"), "Triple Cherries"),
        (("cherry", "cherry", None), "Two Cherries (1st 2)"),
        (("cherry", None, None), "One Cherry (1st Reel)"),
    ]

    # Get actual payout values from rules
    payout_values = {
        "Triple 7s": SLOTS_PAYOUTS.get(("7", "7", "7"), 0),
        "Triple Bells": SLOTS_PAYOUTS.get(("bell", "bell", "bell"), 0),
        "Triple 3-Bar": SLOTS_PAYOUTS.get(("3bar", "3bar", "3bar"), 0),
        "Triple 2-Bar": SLOTS_PAYOUTS.get(("2bar", "2bar", "2bar"), 0),
        "Triple 1-Bar": SLOTS_PAYOUTS.get(("1bar", "1bar", "1bar"), 0),
        "Any 3 Bars": 15, # Hardcoded based on rules logic for now
        "Triple Cherries": SLOTS_PAYOUTS.get(("cherry", "cherry", "cherry"), 0),
        "Two Cherries (1st 2)": SLOTS_PAYOUTS.get(("cherry", "cherry", None), 0),
        "One Cherry (1st Reel)": SLOTS_PAYOUTS.get(("cherry", None, None), 0),
    }


    for _, text in payouts_to_show:
        payout = payout_values.get(text, 0)
        if payout > 0:
            draw_text(surface, f"{text}:", font, x, y, constants.WHITE)
            draw_text(surface, f"{payout}x", font, x + PAYTABLE_COL_WIDTH, y, constants.YELLOW)
            y += line_height


def draw_slots_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], slot_images: Dict[str, pygame.Surface], game_state: Dict[str, Any], game_state_manager: GameState):
    """Draws the Slots game screen."""
    surface.fill(constants.DARK_GREEN)

    current_state = game_state.get('current_state')
    message = game_state.get('message', '')
    result_message = game_state.get('result_message', '')
    spin_timer = game_state.get('slots_spin_timer', 0)
    final_symbols = game_state.get('slots_final_symbols', ["?", "?", "?"]) # Default if not set

    # --- Draw Reels and Symbols ---
    reel_positions = game_state.get('slots_reel_positions', [0] * constants.NUM_REELS)

    for reel_index in range(constants.NUM_REELS):
        reel_strip = REEL_STRIPS[reel_index]
        strip_len = len(reel_strip)
        current_pos_index = reel_positions[reel_index]

        reel_x = REEL_X_START + reel_index * (SLOT_SYMBOL_WIDTH + REEL_SPACING)

        # Determine symbols to show based on state
        symbols_to_draw = []
        if current_state == constants.STATE_SLOTS_SPINNING:
            # Show rapidly changing symbols based on timer/position
            # Simple approach: advance position quickly
            reel_positions[reel_index] = (current_pos_index + random.randint(1, 3)) % strip_len # Faster spin visual
            current_pos_index = reel_positions[reel_index] # Update for drawing

            # Get symbols around the current position for the visible rows
            for i in range(VISIBLE_ROWS):
                 # Calculate index on the strip, wrapping around
                 symbol_index = (current_pos_index + i - (VISIBLE_ROWS // 2) + strip_len) % strip_len
                 symbols_to_draw.append(reel_strip[symbol_index])

        else: # IDLE or SHOWING_RESULT - show the final symbols
            # Need to know the index of the final symbol on the strip to show context
            # For simplicity, just show the final symbols centered for now
            final_symbol = final_symbols[reel_index]
            # Try to find the final symbol on the strip to get context (optional)
            try:
                final_symbol_index = reel_strip.index(final_symbol) # Find first occurrence
            except ValueError:
                final_symbol_index = 0 # Fallback

            for i in range(VISIBLE_ROWS):
                 symbol_index = (final_symbol_index + i - (VISIBLE_ROWS // 2) + strip_len) % strip_len
                 symbols_to_draw.append(reel_strip[symbol_index])


        # Draw the visible symbols for this reel
        for row_index, symbol_name in enumerate(symbols_to_draw):
            symbol_img = slot_images.get(symbol_name)
            if symbol_img:
                symbol_y = REEL_Y_POS + (row_index - (VISIBLE_ROWS // 2)) * SLOT_SYMBOL_HEIGHT
                surface.blit(symbol_img, (reel_x, symbol_y))
            else:
                # Draw placeholder if image missing
                pygame.draw.rect(surface, constants.RED, (reel_x, symbol_y, SLOT_SYMBOL_WIDTH, SLOT_SYMBOL_HEIGHT))
                draw_text(surface, "?", fonts['button'], reel_x + SLOT_SYMBOL_WIDTH//2, symbol_y + SLOT_SYMBOL_HEIGHT//2, constants.WHITE, center=True)

    # Update reel positions in game state if they were changed during spinning draw
    if current_state == constants.STATE_SLOTS_SPINNING:
        game_state['slots_reel_positions'] = reel_positions

    # --- Draw Payline Marker (optional) ---
    payline_y = REEL_Y_POS + SLOT_SYMBOL_HEIGHT // 2
    pygame.draw.line(surface, constants.YELLOW, (REEL_X_START - 10, payline_y), (REEL_X_START + constants.NUM_REELS * SLOT_SYMBOL_WIDTH + 10, payline_y), 3)

    # --- Draw Paytable ---
    draw_slots_paytable(surface, fonts)

    # --- Draw Money ---
    money_text = f"Money: ${game_state_manager.money}"
    draw_text(surface, money_text, fonts['money'], constants.SCREEN_WIDTH - 150, 20, constants.GOLD) # Top right
    # Draw money animation if active
    if game_state.get('money_animation_active', False):
        amount = game_state.get('money_animation_amount', 0)
        anim_text = f"+${amount}" if amount >=0 else f"${amount}"
        draw_text(surface, anim_text, fonts['money'], constants.SCREEN_WIDTH - 150, 20 + constants.MONEY_ANIMATION_OFFSET_Y, constants.YELLOW)

    # --- Draw Messages ---
    if message:
        draw_text(surface, message, fonts['message'], constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 150, constants.WHITE, center=True)
    if result_message:
        # Check flashing state
        is_flashing = game_state.get('result_message_flash_active', False)
        is_visible = game_state.get('result_message_flash_visible', True)
        if not is_flashing or (is_flashing and is_visible):
            result_font = fonts['result']
            color = constants.GOLD
            text_x = constants.SCREEN_WIDTH // 2
            text_y = REEL_Y_POS - 50 # Position above reels
            padding = 8
            # Calculate text size
            text_surf = result_font.render(result_message, True, color)
            text_rect = text_surf.get_rect(center=(text_x, text_y))
            # Draw background rectangle
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(surface, constants.BLACK, bg_rect, border_radius=5)
            # Draw text on top
            surface.blit(text_surf, text_rect)

    # --- Draw Buttons ---
    # Return to Game Selection Button
    draw_button(surface, fonts, "Game Menu", constants.RETURN_TO_MENU_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)

    # Spin Button (active only when idle or showing result)
    can_play_next = game_state_manager.money >= 1 # Check if can afford next $1 spin
    button_color = constants.BUTTON_OFF
    button_text = "SPIN"

    if current_state == constants.STATE_SLOTS_IDLE or current_state == constants.STATE_SLOTS_SHOWING_RESULT:
        button_color = constants.GREEN if can_play_next else constants.RED
    # Else (spinning): keep color as BUTTON_OFF (disabled look)

    draw_button(surface, fonts, button_text, constants.SLOTS_SPIN_BUTTON_RECT, button_color, constants.WHITE)

    # Game Over Screen elements (handled by draw_game_screen, but could be drawn here too if needed)
    if current_state == constants.STATE_GAME_OVER:
        # This state might be triggered from process_input if money runs out
        draw_text(surface, "GAME OVER", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 50, constants.RED, center=True)
        final_money = game_state_manager.money
        draw_text(surface, f"Final Money: ${final_money}", fonts['game_over_medium'], constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2, constants.WHITE, center=True)
        draw_button(surface, fonts, "Play Again", constants.PLAY_AGAIN_BUTTON_RECT, constants.GREEN, constants.WHITE)


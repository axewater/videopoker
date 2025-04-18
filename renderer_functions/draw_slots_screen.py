# /renderer_functions/draw_slots_screen.py
import pygame
import random
from typing import Dict, List, Optional, Any

import config_display as display
import config_colors as colors
import config_assets as assets
import config_states as states
import config_animations as anim
import config_layout_slots as layout_slots
import config_layout_general as layout_general
from game_state import GameState
from slots_rules import REEL_STRIPS, SLOTS_PAYOUTS, BAR_SYMBOLS # Need rules for display
from .draw_text import draw_text
from .draw_button import draw_button

# --- Constants for Slots Layout ---
REEL_X_START = ((display.SCREEN_WIDTH - layout_slots.NUM_REELS * layout_slots.SLOT_SYMBOL_WIDTH) // 2) + 50 # Added + 50
REEL_Y_POS = 150 + 50 # Y position for the payline (center of symbols) # Added + 50
REEL_SPACING = 10 # Horizontal space between reels (if needed, currently adjacent)
VISIBLE_ROWS = 3 # How many symbols are visible vertically per reel
PAYLINE_Y_OFFSET = (VISIBLE_ROWS // 2) * layout_slots.SLOT_SYMBOL_HEIGHT # Offset to draw the central payline symbol
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

    draw_text(surface, "--- Payouts (Bet: 1) ---", font, x, y, colors.GOLD)
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
            draw_text(surface, f"{text}:", font, x, y, colors.WHITE)
            draw_text(surface, f"{payout}x", font, x + PAYTABLE_COL_WIDTH, y, colors.YELLOW)
            y += line_height


def draw_slots_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], slot_images: Dict[str, pygame.Surface], game_state: Dict[str, Any], game_state_manager: GameState, slot_machine_overlay_image: Optional[pygame.Surface] = None): # Added overlay parameter
    """Draws the Slots game screen."""
    surface.fill(colors.DARK_GREEN)

    current_state = game_state.get('current_state')
    message = game_state.get('message', '')
    result_message = game_state.get('result_message', '')
    spin_timer = game_state.get('slots_spin_timer', 0)
    final_symbols = game_state.get('slots_final_symbols', ["?", "?", "?"]) # Default if not set

    # --- Draw Reels and Symbols ---
    reel_positions = game_state.get('slots_reel_positions', [0] * layout_slots.NUM_REELS)

    for reel_index in range(layout_slots.NUM_REELS):
        reel_strip = REEL_STRIPS[reel_index]
        strip_len = len(reel_strip)
        current_pos_index = reel_positions[reel_index]

        reel_x = REEL_X_START + reel_index * (layout_slots.SLOT_SYMBOL_WIDTH + REEL_SPACING)

        # Determine symbols to draw based on state
        symbols_to_draw = []
        if current_state == states.STATE_SLOTS_SPINNING:
            # Show rapidly changing symbols based on timer/position
            reel_positions[reel_index] = (current_pos_index + random.randint(1, 3)) % strip_len # Faster spin visual
            current_pos_index = reel_positions[reel_index] # Update for drawing

            for i in range(VISIBLE_ROWS):
                 symbol_index = (current_pos_index + i - (VISIBLE_ROWS // 2) + strip_len) % strip_len
                 symbols_to_draw.append(reel_strip[symbol_index])

        else: # IDLE or SHOWING_RESULT - show the final symbols
            final_symbol = final_symbols[reel_index]
            try:
                final_symbol_index = reel_strip.index(final_symbol)
            except ValueError:
                final_symbol_index = 0 # Fallback

            for i in range(VISIBLE_ROWS):
                 symbol_index = (final_symbol_index + i - (VISIBLE_ROWS // 2) + strip_len) % strip_len
                 symbols_to_draw.append(reel_strip[symbol_index])


        # Draw the visible symbols for this reel
        for row_index, symbol_name in enumerate(symbols_to_draw):
            symbol_img = slot_images.get(symbol_name)
            if symbol_img:
                symbol_y = REEL_Y_POS + (row_index - (VISIBLE_ROWS // 2)) * layout_slots.SLOT_SYMBOL_HEIGHT
                surface.blit(symbol_img, (reel_x, symbol_y))
            else:
                pygame.draw.rect(surface, colors.RED, (reel_x, symbol_y, layout_slots.SLOT_SYMBOL_WIDTH, layout_slots.SLOT_SYMBOL_HEIGHT))
                draw_text(surface, "?", fonts['button'], reel_x + layout_slots.SLOT_SYMBOL_WIDTH//2, symbol_y + layout_slots.SLOT_SYMBOL_HEIGHT//2, colors.WHITE, center=True)

    # Update reel positions in game state if they were changed during spinning draw
    if current_state == states.STATE_SLOTS_SPINNING:
        game_state['slots_reel_positions'] = reel_positions

    # --- Draw Payline Marker (optional) ---
    payline_y = REEL_Y_POS + layout_slots.SLOT_SYMBOL_HEIGHT // 2
    pygame.draw.line(surface, colors.YELLOW, (REEL_X_START - 10, payline_y), (REEL_X_START + layout_slots.NUM_REELS * layout_slots.SLOT_SYMBOL_WIDTH + 10, payline_y), 3)

    # --- Draw Slot Machine Overlay ---
    if slot_machine_overlay_image:
        # Get the rect of the already resized image
        overlay_rect = slot_machine_overlay_image.get_rect()
        # Start by centering it on the screen
        overlay_rect.centerx = display.SCREEN_WIDTH // 2
        # Adjust vertical position: center and then move up 50px
        overlay_rect.centery = (display.SCREEN_HEIGHT // 2) - 30
        surface.blit(slot_machine_overlay_image, overlay_rect)


    # --- Draw Paytable ---
    draw_slots_paytable(surface, fonts)

    # --- Draw Money ---
    money_text = f"Money: ${game_state_manager.money}"
    draw_text(surface, money_text, fonts['money'], display.SCREEN_WIDTH - 150, 20, colors.GOLD) # Top right
    # Draw money animation if active
    if game_state.get('money_animation_active', False):
        amount = game_state.get('money_animation_amount', 0)
        anim_text = f"+${amount}" if amount >=0 else f"${amount}"
        draw_text(surface, anim_text, fonts['money'], display.SCREEN_WIDTH - 150, 20 + anim.MONEY_ANIMATION_OFFSET_Y, colors.YELLOW)

    # --- Draw Messages ---
    if message:
        draw_text(surface, message, fonts['message'], display.SCREEN_WIDTH // 2 + 50, display.SCREEN_HEIGHT - 150, colors.WHITE, center=True)
    if result_message:
        is_flashing = game_state.get('result_message_flash_active', False)
        is_visible = game_state.get('result_message_flash_visible', True)
        if not is_flashing or (is_flashing and is_visible):
            result_font = fonts['result']
            color = colors.GOLD
            # Position result message maybe below the overlay or above reels, avoiding overlap
            text_x = display.SCREEN_WIDTH // 2
            text_y = REEL_Y_POS - 50 # Position above reels (or adjust if overlay is there)
            padding = 8
            text_surf = result_font.render(result_message, True, color)
            text_rect = text_surf.get_rect(center=(text_x, text_y))
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(surface, colors.BLACK, bg_rect, border_radius=5)
            surface.blit(text_surf, text_rect)

    # --- Draw Buttons ---
    draw_button(surface, fonts, "Game Menu", layout_general.RETURN_TO_MENU_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE)

    can_play_next = game_state_manager.money >= 1
    button_color = colors.BUTTON_OFF
    button_text = "SPIN"

    if current_state == states.STATE_SLOTS_IDLE or current_state == states.STATE_SLOTS_SHOWING_RESULT:
        button_color = colors.GREEN if can_play_next else colors.RED

    draw_button(surface, fonts, button_text, layout_slots.SLOTS_SPIN_BUTTON_RECT, button_color, colors.WHITE)

    # Game Over Screen elements
    if current_state == states.STATE_GAME_OVER:
        draw_text(surface, "GAME OVER", fonts['game_over_large'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2 - 50, colors.RED, center=True)
        final_money = game_state_manager.money
        draw_text(surface, f"Final Money: ${final_money}", fonts['game_over_medium'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2, colors.WHITE, center=True)
        draw_button(surface, fonts, "Play Again", layout_general.PLAY_AGAIN_BUTTON_RECT, colors.GREEN, colors.WHITE)

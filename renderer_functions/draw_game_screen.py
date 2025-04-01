# /renderer_functions/draw_game_screen.py
import pygame
from typing import Dict, List, Optional, Tuple

# --- Config Imports ---
import config_colors as colors
import config_display as display
import config_states as states
import config_layout_cards as layout_cards
import config_layout_general as layout_general
import config_animations as anim
# --- End Config Imports ---

from card import Card
from poker_rules import HandRank
from .draw_pay_table import draw_pay_table
from .draw_text import draw_text
from .draw_hand import draw_hand
from .draw_multi_hands import draw_multi_hands
from .draw_button import draw_button

def draw_game_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], card_images: Dict[str, pygame.Surface], render_data: dict, game_state: dict):
    """Draws the entire game screen based on the provided game data."""
    surface.fill(colors.DARK_GREEN)

    # Use full game_state for more context if needed, render_data for basic display items
    current_state = game_state.get('current_state')
    winning_rank = render_data.get('winning_rank')
    is_multi_poker = current_state in [states.STATE_MULTI_POKER_WAITING_FOR_HOLD, states.STATE_MULTI_POKER_SHOWING_RESULT]

    # Draw Pay Table - Always position top-left
    pay_table_x = layout_cards.PAY_TABLE_X # Always use the standard X position
    pay_table_y = layout_cards.PAY_TABLE_Y
    # Highlight only works well for single hand mode, disable for multi (already handled by passing None)
    draw_pay_table(surface, fonts, x=pay_table_x, y=pay_table_y, winning_rank=winning_rank if not is_multi_poker else None)

    # Draw Money
    money_text = f"Money: ${render_data.get('money', 0)}"
    # Draw money animation if active
    if render_data.get('money_animation_active', False):
        amount = render_data.get('money_animation_amount', 0)
        anim_text = f"+${amount}"
        # Position slightly below the main money text
        draw_text(surface, anim_text, fonts['money'], display.SCREEN_WIDTH - 150, 20 + anim.MONEY_ANIMATION_OFFSET_Y, colors.YELLOW)

    draw_text(surface, money_text, fonts['money'], display.SCREEN_WIDTH - 150, 20, colors.GOLD) # Top right

    # Draw Hand (if available)
    hand = render_data.get('hand')
    held_indices = render_data.get('held_indices', [])

    # Draw hand if it exists and we are in a game state (not menus)
    # Also, don't draw the base hand/hold buttons when showing multi-poker results
    if hand and current_state not in [states.STATE_TOP_MENU, states.STATE_GAME_SELECTION, states.STATE_SETTINGS, states.STATE_CONFIRM_EXIT, states.STATE_MULTI_POKER_SHOWING_RESULT]:
         draw_hand(surface, hand, held_indices, card_images, fonts)

    # Draw Multi Hands (if available and in multi-poker mode showing results)
    multi_hands = render_data.get('multi_hands')
    multi_results = render_data.get('multi_results')
    if is_multi_poker and current_state == states.STATE_MULTI_POKER_SHOWING_RESULT and multi_hands and multi_results:
        # Draw the multiple result hands (usually above the main hand area)
        # Need to pass layout constants correctly here from layout_cards and colors
        draw_multi_hands(surface, multi_hands, multi_results, card_images, fonts) # draw_multi_hands needs updating to use config too

    # Draw Messages
    message = render_data.get('message', '')
    result_message = render_data.get('result_message', '')

    if message:
        draw_text(surface, message, fonts['message'], display.SCREEN_WIDTH // 2, layout_cards.HAND_Y_POS - 60, colors.WHITE, center=True)
    if result_message:
        # Check flashing state
        is_flashing = render_data.get('result_message_flash_active', False)
        is_visible = render_data.get('result_message_flash_visible', True)

        # Only draw if not flashing, or if flashing and currently visible
        if not is_flashing or (is_flashing and is_visible):
            result_font = fonts['result']
            color = colors.GOLD if "WINNER" in result_message else colors.WHITE
            text_x = display.SCREEN_WIDTH // 2
            text_y = layout_cards.HAND_Y_POS - 100 # Position above hand
            padding = 8

            # Calculate text size
            text_surf = result_font.render(result_message, True, color)
            text_rect = text_surf.get_rect(center=(text_x, text_y))

            # Draw background rectangle
            bg_rect = text_rect.inflate(padding * 2, padding * 2) # Add padding
            pygame.draw.rect(surface, colors.BLACK, bg_rect, border_radius=5)

            # Draw text on top
            surface.blit(text_surf, text_rect)

    # Draw Buttons
    # Return to Game Selection Button (visible during gameplay)
    if current_state not in [states.STATE_TOP_MENU, states.STATE_GAME_SELECTION, states.STATE_SETTINGS, states.STATE_GAME_OVER, states.STATE_CONFIRM_EXIT]:
        draw_button(surface, fonts, "Game Menu", layout_general.RETURN_TO_MENU_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE)

    # Contextual Deal/Draw Button
    can_play = render_data.get('can_play', False) # Can afford cost=1
    # Determine button text and state based on current_state
    if current_state == states.STATE_DRAW_POKER_IDLE:
        button_color = colors.GREEN if can_play else colors.RED
        draw_button(surface, fonts, "DEAL", layout_cards.DEAL_DRAW_BUTTON_RECT, button_color, colors.WHITE)
    elif current_state == states.STATE_DRAW_POKER_WAITING_FOR_HOLD:
        draw_button(surface, fonts, "DRAW", layout_cards.DEAL_DRAW_BUTTON_RECT, colors.GREEN, colors.WHITE)
    elif current_state == states.STATE_DRAW_POKER_SHOWING_RESULT:
         button_color = colors.GREEN if can_play else colors.RED
         draw_button(surface, fonts, "DEAL", layout_cards.DEAL_DRAW_BUTTON_RECT, button_color, colors.WHITE)
    elif current_state == states.STATE_MULTI_POKER_IDLE:
         cost_next_game = layout_cards.NUM_MULTI_HANDS
         can_play_multi = render_data.get('money', 0) >= cost_next_game
         button_color = colors.GREEN if can_play_multi else colors.RED
         draw_button(surface, fonts, "DEAL", layout_cards.DEAL_DRAW_BUTTON_RECT, button_color, colors.WHITE)
    elif current_state == states.STATE_MULTI_POKER_WAITING_FOR_HOLD: # Added for multi-poker draw
        draw_button(surface, fonts, "DRAW", layout_cards.DEAL_DRAW_BUTTON_RECT, colors.GREEN, colors.WHITE)
    elif current_state == states.STATE_MULTI_POKER_SHOWING_RESULT: # Added for multi-poker next deal
         cost_next_game = layout_cards.NUM_MULTI_HANDS
         can_play_multi = render_data.get('money', 0) >= cost_next_game
         button_color = colors.GREEN if can_play_multi else colors.RED
         draw_button(surface, fonts, "DEAL", layout_cards.DEAL_DRAW_BUTTON_RECT, button_color, colors.WHITE)


    # Game Over Screen elements
    if current_state == states.STATE_GAME_OVER:
        draw_text(surface, "GAME OVER", fonts['game_over_large'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2 - 50, colors.RED, center=True)
        final_money = render_data.get('money', 0)
        draw_text(surface, f"Final Money: ${final_money}", fonts['game_over_medium'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2, colors.WHITE, center=True)
        draw_button(surface, fonts, "Play Again", layout_general.PLAY_AGAIN_BUTTON_RECT, colors.GREEN, colors.WHITE)


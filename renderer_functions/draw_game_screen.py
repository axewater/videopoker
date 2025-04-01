import pygame
from typing import Dict, List, Optional, Tuple

import constants
from card import Card
from poker_rules import HandRank
from .draw_pay_table import draw_pay_table
from .draw_text import draw_text
from .draw_hand import draw_hand
from .draw_multi_hands import draw_multi_hands
from .draw_button import draw_button

def draw_game_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], card_images: Dict[str, pygame.Surface], game_data: dict):
    """Draws the entire game screen based on the provided game data."""
    surface.fill(constants.DARK_GREEN)

    current_state = game_data.get('current_state')
    winning_rank = game_data.get('winning_rank')
    is_multi_poker = current_state in [constants.STATE_MULTI_POKER_WAITING_FOR_HOLD, constants.STATE_MULTI_POKER_SHOWING_RESULT]

    # Draw Pay Table - position depends on game mode
    pay_table_x = constants.PAY_TABLE_MULTI_X if is_multi_poker else constants.PAY_TABLE_X
    pay_table_y = constants.PAY_TABLE_Y
    # Highlight only works well for single hand mode, disable for multi
    draw_pay_table(surface, fonts, x=pay_table_x, y=pay_table_y, winning_rank=winning_rank if not is_multi_poker else None)

    # Draw Money
    money_text = f"Money: ${game_data.get('money', 0)}"
    # Draw money animation if active
    if game_data.get('money_animation_active', False):
        amount = game_data.get('money_animation_amount', 0)
        anim_text = f"+${amount}"
        # Position slightly below the main money text
        draw_text(surface, anim_text, fonts['money'], constants.SCREEN_WIDTH - 150, 20 + constants.MONEY_ANIMATION_OFFSET_Y, constants.YELLOW)

    draw_text(surface, money_text, fonts['money'], constants.SCREEN_WIDTH - 150, 20, constants.GOLD) # Top right

    # Draw Hand (if available)
    hand = game_data.get('hand')
    held_indices = game_data.get('held_indices', [])

    # Only draw hand if not in main menu or if game over but hand exists (showing final hand)
    if hand and (current_state != constants.STATE_MAIN_MENU or (current_state == constants.STATE_GAME_OVER and hand)):
         draw_hand(surface, hand, held_indices, card_images, fonts)

    # Draw Multi Hands (if available and in multi-poker mode showing results)
    multi_hands = game_data.get('multi_hands')
    multi_results = game_data.get('multi_results')
    if is_multi_poker and current_state == constants.STATE_MULTI_POKER_SHOWING_RESULT and multi_hands and multi_results:
        # Draw the multiple result hands (usually above the main hand area)
        draw_multi_hands(surface, multi_hands, multi_results, card_images, fonts)

    # Draw Messages
    message = game_data.get('message', '')
    result_message = game_data.get('result_message', '')

    if message:
        draw_text(surface, message, fonts['message'], constants.SCREEN_WIDTH // 2, constants.HAND_Y_POS - 60, constants.WHITE, center=True)
    if result_message:
         color = constants.GOLD if "WINNER" in result_message else constants.WHITE
         draw_text(surface, result_message, fonts['result'], constants.SCREEN_WIDTH // 2, constants.HAND_Y_POS - 100, color, center=True) # Position above hand

    # Draw Buttons
    # Quit Button (always visible)
    draw_button(surface, fonts, "QUIT", constants.QUIT_BUTTON_RECT, constants.RED, constants.WHITE)

    # Return to Menu Button (visible during gameplay)
    if current_state not in [constants.STATE_MAIN_MENU, constants.STATE_GAME_OVER]:
        draw_button(surface, fonts, "Return to Menu", constants.RETURN_TO_MENU_BUTTON_RECT, constants.BUTTON_OFF, constants.WHITE)

    # Contextual Deal/Draw Button
    can_play = game_data.get('can_play', False)
    # No Deal button on main menu anymore
    if current_state == constants.STATE_DRAW_POKER_WAITING_FOR_HOLD:
        draw_button(surface, fonts, "DRAW", constants.DEAL_DRAW_BUTTON_RECT, constants.GREEN, constants.WHITE)
    elif current_state == constants.STATE_DRAW_POKER_SHOWING_RESULT:
         button_color = constants.GREEN if can_play else constants.RED
         draw_button(surface, fonts, "DEAL", constants.DEAL_DRAW_BUTTON_RECT, button_color, constants.WHITE)
    elif current_state == constants.STATE_MULTI_POKER_WAITING_FOR_HOLD: # Added for multi-poker draw
        draw_button(surface, fonts, "DRAW", constants.DEAL_DRAW_BUTTON_RECT, constants.GREEN, constants.WHITE)
    elif current_state == constants.STATE_MULTI_POKER_SHOWING_RESULT: # Added for multi-poker next deal
         cost_next_game = constants.NUM_MULTI_HANDS
         can_play_multi = game_data.get('money', 0) >= cost_next_game
         button_color = constants.GREEN if can_play_multi else constants.RED
         draw_button(surface, fonts, "DEAL", constants.DEAL_DRAW_BUTTON_RECT, button_color, constants.WHITE)


    # Game Over Screen elements
    if current_state == constants.STATE_GAME_OVER:
        draw_text(surface, "GAME OVER", fonts['game_over_large'], constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 50, constants.RED, center=True)
        final_money = game_data.get('money', 0)
        draw_text(surface, f"Final Money: ${final_money}", fonts['game_over_medium'], constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2, constants.WHITE, center=True)
        draw_button(surface, fonts, "Play Again", constants.PLAY_AGAIN_BUTTON_RECT, constants.GREEN, constants.WHITE)

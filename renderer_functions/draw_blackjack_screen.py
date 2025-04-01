import pygame
from typing import Dict, List, Optional

import config_colors as colors
import config_display as display
import config_layout_cards as layout_cards
import config_layout_general as layout_general
import config_animations as animations
import config_states as states
from card import Card
from game_state import GameState
from blackjack_rules import get_hand_value, BLACKJACK_PAYOUT, WIN_PAYOUT, BLACKJACK_VALUES
from .draw_text import draw_text
from .draw_button import draw_button
from .get_card_image import get_card_image

def draw_blackjack_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], card_images: Dict[str, pygame.Surface], game_state: Dict, game_state_manager: GameState):
    """Draws the Blackjack game screen."""
    surface.fill(colors.DARK_GREEN)

    player_hand = game_state.get('player_hand', [])
    dealer_hand = game_state.get('dealer_hand', [])
    dealer_shows_one_card = game_state.get('dealer_shows_one_card', False)
    current_state = game_state.get('current_state')
    message = game_state.get('message', '')
    result_message = game_state.get('result_message', '')

    # --- Draw Dealer's Hand ---
    dealer_y = 50
    dealer_x_start = (display.SCREEN_WIDTH - len(dealer_hand) * (layout_cards.CARD_WIDTH + layout_cards.CARD_SPACING)) // 2
    dealer_value_text = ""
    if dealer_hand:
        for i, card in enumerate(dealer_hand):
            x = dealer_x_start + i * (layout_cards.CARD_WIDTH + layout_cards.CARD_SPACING)
            if i == 0 and dealer_shows_one_card:
                # Draw card back (need a card back image, or just a placeholder)
                # Placeholder: Green rectangle
                pygame.draw.rect(surface, colors.GREEN, (x, dealer_y, layout_cards.CARD_WIDTH, layout_cards.CARD_HEIGHT), border_radius=5)
                pygame.draw.rect(surface, colors.WHITE, (x, dealer_y, layout_cards.CARD_WIDTH, layout_cards.CARD_HEIGHT), 1, border_radius=5)
                dealer_value_text = f"Dealer Shows: {BLACKJACK_VALUES.get(dealer_hand[1].rank, '?')}" # Show value of upcard
            else:
                img = get_card_image(card, card_images)
                surface.blit(img, (x, dealer_y))

        if not dealer_shows_one_card:
            dealer_value = get_hand_value(dealer_hand)
            dealer_value_text = f"Dealer Hand: {dealer_value}"
            if dealer_value > 21:
                dealer_value_text += " (Bust!)"

        # Draw dealer value text above hand
        draw_text(surface, dealer_value_text, fonts['message'], display.SCREEN_WIDTH // 2, dealer_y - 30, colors.WHITE, center=True)

    # --- Draw Player's Hand ---
    player_y = layout_cards.HAND_Y_POS # Reuse poker hand Y position
    player_x_start = (display.SCREEN_WIDTH - len(player_hand) * (layout_cards.CARD_WIDTH + layout_cards.CARD_SPACING)) // 2
    player_value_text = ""
    if player_hand:
        for i, card in enumerate(player_hand):
            x = player_x_start + i * (layout_cards.CARD_WIDTH + layout_cards.CARD_SPACING)
            img = get_card_image(card, card_images)
            surface.blit(img, (x, player_y))

        player_value = get_hand_value(player_hand)
        player_value_text = f"Player Hand: {player_value}"
        if player_value > 21:
            player_value_text += " (Bust!)"

        # Draw player value text below hand
        draw_text(surface, player_value_text, fonts['message'], display.SCREEN_WIDTH // 2, player_y + layout_cards.CARD_HEIGHT + 20, colors.WHITE, center=True)

    # --- Draw Money ---
    money_text = f"Money: ${game_state_manager.money}"
    draw_text(surface, money_text, fonts['money'], display.SCREEN_WIDTH - 150, 20, colors.GOLD) # Top right
    # Draw money animation if active
    if game_state.get('money_animation_active', False):
        amount = game_state.get('money_animation_amount', 0)
        anim_text = f"+${amount}" if amount >=0 else f"${amount}" # Show sign correctly
        draw_text(surface, anim_text, fonts['money'], display.SCREEN_WIDTH - 150, 20 + animations.MONEY_ANIMATION_OFFSET_Y, colors.YELLOW)


    # --- Draw Messages ---
    if message:
        draw_text(surface, message, fonts['message'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT - 150, colors.WHITE, center=True)
    if result_message:
        # Check flashing state
        is_flashing = game_state.get('result_message_flash_active', False)
        is_visible = game_state.get('result_message_flash_visible', True)
        if not is_flashing or (is_flashing and is_visible):
            result_font = fonts['result']
            color = colors.GOLD # Always gold for result? Or based on win/loss? Let's use gold.
            text_x = display.SCREEN_WIDTH // 2
            text_y = display.SCREEN_HEIGHT // 2 # Center screen
            padding = 8
            # Calculate text size
            text_surf = result_font.render(result_message, True, color)
            text_rect = text_surf.get_rect(center=(text_x, text_y))
            # Draw background rectangle
            bg_rect = text_rect.inflate(padding * 2, padding * 2) # Add padding
            pygame.draw.rect(surface, colors.BLACK, bg_rect, border_radius=5)
            # Draw text on top
            surface.blit(text_surf, text_rect)

    # --- Draw Payout Table (Simple Text) ---
    payout_y_start = layout_cards.PAY_TABLE_Y
    payout_font = fonts['pay_table']
    line_height = payout_font.get_linesize()
    draw_text(surface, "--- Blackjack Pays ---", payout_font, layout_cards.PAY_TABLE_X, payout_y_start, colors.GOLD)
    draw_text(surface, f"Blackjack: {BLACKJACK_PAYOUT * 2:.1f} to {WIN_PAYOUT * 2:.1f}", payout_font, layout_cards.PAY_TABLE_X, payout_y_start + line_height, colors.WHITE)
    draw_text(surface, f"Win: {WIN_PAYOUT * 2:.1f} to {WIN_PAYOUT * 2:.1f}", payout_font, layout_cards.PAY_TABLE_X, payout_y_start + 2 * line_height, colors.WHITE)
    draw_text(surface, "Dealer stands on 17+", payout_font, layout_cards.PAY_TABLE_X, payout_y_start + 3 * line_height, colors.WHITE)

    # --- Draw Buttons ---
    # Return to Game Selection Button
    draw_button(surface, fonts, "Game Menu", layout_general.RETURN_TO_MENU_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE)

    # Action Buttons (Hit/Stand or Deal)
    can_play_next = game_state_manager.money >= 1 # Check if can afford next $1 bet

    if current_state == states.STATE_BLACKJACK_PLAYER_TURN:
        draw_button(surface, fonts, "Hit", layout_cards.BLACKJACK_HIT_BUTTON_RECT, colors.GREEN, colors.WHITE)
        draw_button(surface, fonts, "Stand", layout_cards.BLACKJACK_STAND_BUTTON_RECT, colors.GREEN, colors.WHITE)
    elif current_state == states.STATE_BLACKJACK_IDLE or current_state == states.STATE_BLACKJACK_SHOWING_RESULT:
        button_color = colors.GREEN if can_play_next else colors.RED
        draw_button(surface, fonts, "DEAL", layout_cards.DEAL_DRAW_BUTTON_RECT, button_color, colors.WHITE)

    # Game Over Screen elements (handled by draw_game_screen, but could be drawn here too if needed)
    if current_state == states.STATE_GAME_OVER:
        draw_text(surface, "GAME OVER", fonts['game_over_large'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2 - 50, colors.RED, center=True)
        final_money = game_state_manager.money
        draw_text(surface, f"Final Money: ${final_money}", fonts['game_over_medium'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2, colors.WHITE, center=True)
        draw_button(surface, fonts, "Play Again", layout_general.PLAY_AGAIN_BUTTON_RECT, colors.GREEN, colors.WHITE)

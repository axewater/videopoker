# /renderer_functions/draw_baccarat_screen.py
"""
Draws the Baccarat game screen, including hands, betting areas, and messages.
"""
import pygame
from typing import Dict, List, Optional, Any

import config_colors as colors
import config_display as display
import config_layout_baccarat as layout_baccarat
import config_layout_general as layout_general
import config_animations as anim
import config_states as states
import config_layout_cards as layout_cards # Added import for CARD_WIDTH
from card import Card
from game_state import GameState
from baccarat_rules import BET_PLAYER, BET_BANKER, BET_TIE # Import bet types
from .draw_text import draw_text
from .draw_button import draw_button
from .get_card_image import get_card_image

def draw_baccarat_screen(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], card_images: Dict[str, pygame.Surface], game_state: Dict[str, Any], game_state_manager: GameState):
    """Draws the Baccarat game screen."""
    surface.fill(colors.DARK_GREEN) # Baccarat often uses green

    player_hand = game_state.get('baccarat_player_hand', [])
    banker_hand = game_state.get('baccarat_banker_hand', [])
    player_value = game_state.get('baccarat_player_value') # Final value after resolution
    banker_value = game_state.get('baccarat_banker_value')
    bets = game_state.get('baccarat_bets', {})
    bet_type = game_state.get('baccarat_bet_type')
    total_bet = game_state.get('baccarat_total_bet', 0)
    current_state = game_state.get('current_state')
    message = game_state.get('message', '')
    result_message = game_state.get('result_message', '')
    winner = game_state.get('baccarat_winner') # Winning hand name

    # --- Draw Money ---
    money_text = f"Money: ${game_state_manager.money}"
    draw_text(surface, money_text, fonts['money'], display.SCREEN_WIDTH - 150, 20, colors.GOLD) # Top right
    # Draw money animation if active
    if game_state.get('money_animation_active', False):
        amount = game_state.get('money_animation_amount', 0)
        anim_text = f"+${amount}" if amount >=0 else f"${amount}"
        draw_text(surface, anim_text, fonts['money'], display.SCREEN_WIDTH - 150, 20 + anim.MONEY_ANIMATION_OFFSET_Y, colors.YELLOW)

    # --- Draw Betting Areas ---
    bet_area_font = fonts['button']
    chip_font = fonts['pay_table']

    # Player Bet Area
    pygame.draw.rect(surface, colors.BLUE, layout_baccarat.BACCARAT_BET_PLAYER_RECT, border_radius=10) # Blue for Player
    pygame.draw.rect(surface, colors.WHITE, layout_baccarat.BACCARAT_BET_PLAYER_RECT, 2, border_radius=10)
    draw_text(surface, "PLAYER", bet_area_font, layout_baccarat.BACCARAT_BET_PLAYER_RECT.centerx, layout_baccarat.BACCARAT_BET_PLAYER_RECT.top + 20, colors.WHITE, center=True)
    draw_text(surface, "Pays 1:1", fonts['pay_table'], layout_baccarat.BACCARAT_BET_PLAYER_RECT.centerx, layout_baccarat.BACCARAT_BET_PLAYER_RECT.bottom - 20, colors.WHITE, center=True)
    if bets.get(BET_PLAYER, 0) > 0:
        chip_pos = (layout_baccarat.BACCARAT_BET_PLAYER_RECT.centerx, layout_baccarat.BACCARAT_BET_PLAYER_RECT.centery + layout_baccarat.CHIP_OFFSET_Y)
        pygame.draw.circle(surface, colors.ROULETTE_CHIP_COLOR, chip_pos, layout_baccarat.CHIP_RADIUS)
        draw_text(surface, str(bets[BET_PLAYER]), chip_font, chip_pos[0], chip_pos[1], colors.BLACK, center=True)

    # Tie Bet Area
    pygame.draw.rect(surface, colors.GREEN, layout_baccarat.BACCARAT_BET_TIE_RECT, border_radius=10) # Green for Tie
    pygame.draw.rect(surface, colors.WHITE, layout_baccarat.BACCARAT_BET_TIE_RECT, 2, border_radius=10)
    draw_text(surface, "TIE", bet_area_font, layout_baccarat.BACCARAT_BET_TIE_RECT.centerx, layout_baccarat.BACCARAT_BET_TIE_RECT.top + 20, colors.WHITE, center=True)
    draw_text(surface, "Pays 8:1", fonts['pay_table'], layout_baccarat.BACCARAT_BET_TIE_RECT.centerx, layout_baccarat.BACCARAT_BET_TIE_RECT.bottom - 20, colors.WHITE, center=True)
    if bets.get(BET_TIE, 0) > 0:
        chip_pos = (layout_baccarat.BACCARAT_BET_TIE_RECT.centerx, layout_baccarat.BACCARAT_BET_TIE_RECT.centery + layout_baccarat.CHIP_OFFSET_Y)
        pygame.draw.circle(surface, colors.ROULETTE_CHIP_COLOR, chip_pos, layout_baccarat.CHIP_RADIUS)
        draw_text(surface, str(bets[BET_TIE]), chip_font, chip_pos[0], chip_pos[1], colors.BLACK, center=True)

    # Banker Bet Area
    pygame.draw.rect(surface, colors.RED, layout_baccarat.BACCARAT_BET_BANKER_RECT, border_radius=10) # Red for Banker
    pygame.draw.rect(surface, colors.WHITE, layout_baccarat.BACCARAT_BET_BANKER_RECT, 2, border_radius=10)
    draw_text(surface, "BANKER", bet_area_font, layout_baccarat.BACCARAT_BET_BANKER_RECT.centerx, layout_baccarat.BACCARAT_BET_BANKER_RECT.top + 20, colors.WHITE, center=True)
    draw_text(surface, "Pays 0.95:1", fonts['pay_table'], layout_baccarat.BACCARAT_BET_BANKER_RECT.centerx, layout_baccarat.BACCARAT_BET_BANKER_RECT.bottom - 20, colors.WHITE, center=True)
    if bets.get(BET_BANKER, 0) > 0:
        chip_pos = (layout_baccarat.BACCARAT_BET_BANKER_RECT.centerx, layout_baccarat.BACCARAT_BET_BANKER_RECT.centery + layout_baccarat.CHIP_OFFSET_Y)
        pygame.draw.circle(surface, colors.ROULETTE_CHIP_COLOR, chip_pos, layout_baccarat.CHIP_RADIUS)
        draw_text(surface, str(bets[BET_BANKER]), chip_font, chip_pos[0], chip_pos[1], colors.BLACK, center=True)

    # --- Draw Hands ---
    # Player Hand
    # --- MODIFICATION START: Use layout_cards.CARD_WIDTH ---
    draw_text(surface, "PLAYER", fonts['message'], layout_baccarat.PLAYER_CARD_RECTS[0].centerx + layout_cards.CARD_WIDTH * 0.5, layout_baccarat.PLAYER_HAND_Y - 30, colors.WHITE, center=True) # Centered above hand
    # --- MODIFICATION END ---
    for i, card in enumerate(player_hand):
        if i < len(layout_baccarat.PLAYER_CARD_RECTS):
            img = get_card_image(card, card_images)
            surface.blit(img, layout_baccarat.PLAYER_CARD_RECTS[i])
    if player_value is not None:
        # --- MODIFICATION START: Use layout_cards.CARD_WIDTH ---
        draw_text(surface, f"Value: {player_value}", fonts['message'], layout_baccarat.PLAYER_CARD_RECTS[0].centerx + layout_cards.CARD_WIDTH * 0.5, layout_baccarat.PLAYER_VALUE_TEXT_Y, colors.WHITE, center=True) # Centered below hand
        # --- MODIFICATION END ---

    # Banker Hand
    # --- MODIFICATION START: Use layout_cards.CARD_WIDTH ---
    draw_text(surface, "BANKER", fonts['message'], layout_baccarat.BANKER_CARD_RECTS[0].centerx + layout_cards.CARD_WIDTH * 0.5, layout_baccarat.BANKER_HAND_Y - 30, colors.WHITE, center=True) # Centered above hand
    # --- MODIFICATION END ---
    for i, card in enumerate(banker_hand):
         if i < len(layout_baccarat.BANKER_CARD_RECTS):
            img = get_card_image(card, card_images)
            surface.blit(img, layout_baccarat.BANKER_CARD_RECTS[i])
    if banker_value is not None:
        # --- MODIFICATION START: Use layout_cards.CARD_WIDTH ---
        draw_text(surface, f"Value: {banker_value}", fonts['message'], layout_baccarat.BANKER_CARD_RECTS[0].centerx + layout_cards.CARD_WIDTH * 0.5, layout_baccarat.BANKER_VALUE_TEXT_Y, colors.WHITE, center=True) # Centered below hand
        # --- MODIFICATION END ---

    # --- Draw Messages ---
    if message:
        draw_text(surface, message, fonts['message'], display.SCREEN_WIDTH // 2, layout_baccarat.MESSAGE_TEXT_Y, colors.WHITE, center=True)
    if result_message:
        # Check flashing state
        is_flashing = game_state.get('result_message_flash_active', False)
        is_visible = game_state.get('result_message_flash_visible', True)
        if not is_flashing or (is_flashing and is_visible):
            result_font = fonts['result']
            color = colors.GOLD
            text_x = display.SCREEN_WIDTH // 2
            text_y = layout_baccarat.RESULT_TEXT_Y
            padding = 8
            # Calculate text size
            text_surf = result_font.render(result_message, True, color)
            text_rect = text_surf.get_rect(center=(text_x, text_y))
            # Draw background rectangle
            bg_rect = text_rect.inflate(padding * 2, padding * 2) # Add padding
            pygame.draw.rect(surface, colors.BLACK, bg_rect, border_radius=5)
            # Draw text on top
            surface.blit(text_surf, text_rect)

    # --- Draw Buttons ---
    # Return to Game Selection Button
    draw_button(surface, fonts, "Game Menu", layout_general.RETURN_TO_MENU_BUTTON_RECT, colors.BUTTON_OFF, colors.WHITE)

    # Action Buttons (Deal or Clear)
    can_deal = total_bet > 0
    deal_button_color = colors.GREEN if can_deal else colors.BUTTON_OFF
    clear_button_color = colors.RED if total_bet > 0 else colors.BUTTON_OFF

    if current_state == states.STATE_BACCARAT_BETTING or current_state == states.STATE_BACCARAT_RESULT:
        draw_button(surface, fonts, "DEAL", layout_baccarat.BACCARAT_DEAL_BUTTON_RECT, deal_button_color, colors.WHITE)
        draw_button(surface, fonts, "Clear Bets", layout_baccarat.BACCARAT_CLEAR_BETS_BUTTON_RECT, clear_button_color, colors.WHITE)
    # Hide buttons during dealing/drawing phases

    # Game Over Screen elements
    if current_state == states.STATE_GAME_OVER:
        draw_text(surface, "GAME OVER", fonts['game_over_large'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2 - 50, colors.RED, center=True)
        final_money = game_state_manager.money
        draw_text(surface, f"Final Money: ${final_money}", fonts['game_over_medium'], display.SCREEN_WIDTH // 2, display.SCREEN_HEIGHT // 2, colors.WHITE, center=True)
        draw_button(surface, fonts, "Play Again", layout_general.PLAY_AGAIN_BUTTON_RECT, colors.GREEN, colors.WHITE)


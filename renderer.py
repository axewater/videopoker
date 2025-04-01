import pygame
import os
import sys
from typing import List, Tuple, Dict, Optional

import constants
from card import Card
from poker_rules import PAY_TABLE, HandRank

class Renderer:
    """Handles all drawing operations for the game."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.card_images = self._load_card_images(constants.CARD_ASSET_PATH)
        self.fonts = {
            'money': self._get_font(constants.MONEY_FONT_SIZE),
            'message': self._get_font(constants.MESSAGE_FONT_SIZE),
            'pay_table': self._get_font(constants.PAY_TABLE_FONT_SIZE),
            'button': self._get_font(constants.BUTTON_FONT_SIZE),
            'result': self._get_font(constants.RESULT_FONT_SIZE),
            'hold': self._get_font(constants.HOLD_FONT_SIZE),
            'game_over_large': self._get_font(64),
            'game_over_medium': self._get_font(32),
        }

    def _get_font(self, size: int, font_name: Optional[str] = None) -> pygame.font.Font:
        """Helper to load fonts."""
        return pygame.font.Font(pygame.font.match_font(font_name) if font_name else None, size)

    def _load_card_images(self, path: str) -> Dict[str, pygame.Surface]:
        """Loads card images from the specified path."""
        images = {}
        if not os.path.exists(path):
            print(f"Error: Asset path not found: {os.path.abspath(path)}")
            print("Please ensure card images are in an 'assets/cards' directory relative to main.py.")
            print("Exiting.")
            pygame.quit()
            sys.exit()

        try:
            # Standard ranks and suits for filenames
            ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
            suits_short = ['S', 'H', 'D', 'C'] # Spades, Hearts, Diamonds, Clubs

            for suit_short in suits_short:
                for rank in ranks:
                    filename = f"{rank}{suit_short}.png"
                    filepath = os.path.join(path, filename)
                    if not os.path.isfile(filepath):
                         print(f"Warning: Card image file not found: {filepath}")
                         continue # Skip if a specific file is missing

                    img = pygame.image.load(filepath).convert_alpha()
                    # Scale image if needed (optional, adjust CARD_WIDTH/HEIGHT in constants)
                    img = pygame.transform.scale(img, (constants.CARD_WIDTH, constants.CARD_HEIGHT))
                    images[f"{rank}{suit_short}"] = img

        except pygame.error as e:
            print(f"Error loading image: {e}")
            print(f"Searched in path: {os.path.abspath(path)}")
            pygame.quit()
            sys.exit()

        if len(images) < 52:
            print(f"Warning: Loaded only {len(images)} card images from {os.path.abspath(path)}. Expected 52.")
            if not images: # Exit if no images loaded at all
                 print("Error: No card images loaded. Exiting.")
                 pygame.quit()
                 sys.exit()

        return images

    def _get_card_image(self, card: Card) -> pygame.Surface:
        """Gets the pre-loaded image surface for a specific card."""
        suit_map = {"♠": "S", "♥": "H", "♦": "D", "♣": "C"}
        suit_short = suit_map.get(card.suit, '?')
        key = f"{card.rank}{suit_short}"

        if key not in self.card_images:
            print(f"Error: Image not found for card key: {key}")
            # Return a blank surface or a default 'back' image if available
            return pygame.Surface((constants.CARD_WIDTH, constants.CARD_HEIGHT))
        return self.card_images[key]

    def draw_text(self, text: str, font_key: str, x: int, y: int, color: Tuple[int, int, int], center: bool = False):
        """Draws text using a pre-loaded font."""
        font = self.fonts.get(font_key)
        if not font:
            print(f"Warning: Font key '{font_key}' not found.")
            font = self.fonts['message'] # Fallback

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.surface.blit(text_surface, text_rect)

    def draw_hand(self, hand: List[Card], held_indices: List[int]):
        """Draws the player's hand and the HOLD buttons below them."""
        hold_font = self.fonts['hold']
        for i, card in enumerate(hand):
            img = self._get_card_image(card)
            card_rect = constants.CARD_RECTS[i]
            self.surface.blit(img, card_rect)

            # Draw HOLD button below card
            hold_rect = constants.HOLD_BUTTON_RECTS[i]
            button_color = constants.BUTTON_ON if i in held_indices else constants.BUTTON_OFF
            pygame.draw.rect(self.surface, button_color, hold_rect, border_radius=5)

            # Draw HOLD text on the button
            hold_text_surface = hold_font.render("HOLD", True, constants.WHITE)
            text_rect = hold_text_surface.get_rect(center=hold_rect.center)
            self.surface.blit(hold_text_surface, text_rect)

    def draw_pay_table(self, x: int, y: int, winning_rank: Optional[HandRank] = None):
        """Draws the pay table."""
        pay_table_font = self.fonts['pay_table']
        line_height = pay_table_font.get_linesize()
        padding = 5
        highlight_color = constants.YELLOW
        background_color = constants.BLACK
        text_color = constants.WHITE
        title_color = constants.GOLD
        colon_color = constants.WHITE # Color for the colon separator
        colon_str = ":"

        # Sort ranks by payout (highest first)
        sorted_ranks = sorted([rank for rank in PAY_TABLE if PAY_TABLE[rank][1] > 0],
                              key=lambda k: PAY_TABLE[k][1], reverse=True)

        # Prepare title
        title_font = self._get_font(constants.PAY_TABLE_FONT_SIZE + 2)
        title_text = "--- Pay Table (Bet: 1) ---"
        title_surf = title_font.render(title_text, True, title_color)
        title_width = title_surf.get_width()
        current_y = y + line_height * 1.5 # Start below title

        # Prepare text surfaces and calculate dimensions
        name_surfaces = []
        payout_surfaces = []
        max_name_width = 0
        max_payout_width = 0

        for rank in sorted_ranks:
            name, payout = PAY_TABLE[rank]
            name_surf = pay_table_font.render(name, True, text_color)
            payout_str = f"{payout}x"
            payout_surf = pay_table_font.render(payout_str, True, text_color)
            
            name_surfaces.append((rank, name_surf)) # Store rank with surface
            payout_surfaces.append(payout_surf)
            
            max_name_width = max(max_name_width, name_surf.get_width())
            max_payout_width = max(max_payout_width, payout_surf.get_width())

        # Render colon separately for precise alignment
        colon_surf = pay_table_font.render(colon_str, True, colon_color)
        colon_width = colon_surf.get_width()
        column_spacing = 5 # Space around the colon

        # Calculate total width and height for background
        total_content_width = max_name_width + column_spacing + colon_width + column_spacing + max_payout_width
        max_width = max(title_width, total_content_width)
        total_height = (line_height * 1.5) + (len(sorted_ranks) * line_height) # Title + entries

        # Draw background rectangle
        bg_rect = pygame.Rect(x - padding, y - padding, max_width + 2 * padding, total_height + 2 * padding)
        pygame.draw.rect(self.surface, background_color, bg_rect, border_radius=5)

        # Draw title
        self.surface.blit(title_surf, (x, y))

        # Draw each winning hand
        for i, (rank, name_surface) in enumerate(name_surfaces):
            payout_surface = payout_surfaces[i]
            
            # Calculate positions
            name_x = x
            colon_x = x + max_name_width + column_spacing
            payout_x = colon_x + colon_width + column_spacing
            
            if rank == winning_rank: # Check if this is the winning hand
                highlight_rect = pygame.Rect(x - padding // 2, current_y - padding // 2, max_width + padding, line_height + padding // 2)
                pygame.draw.rect(self.surface, highlight_color, highlight_rect, width=2, border_radius=3) # Draw border
                
            # Draw components: Name (left-aligned), Colon, Payout (left-aligned in its column)
            self.surface.blit(name_surface, (name_x, current_y))
            self.surface.blit(colon_surf, (colon_x, current_y))
            self.surface.blit(payout_surface, (payout_x, current_y))
            
            current_y += line_height # Move down for the next line

    def draw_button(self, text: str, rect: pygame.Rect, color: Tuple[int, int, int], text_color: Tuple[int, int, int]):
        """Draws a button with text."""
        pygame.draw.rect(self.surface, color, rect, border_radius=5)
        self.draw_text(text, 'button', rect.centerx, rect.centery, text_color, center=True)

    def draw_game_screen(self, game_data: dict):
        """Draws the entire game screen based on the provided game data."""
        self.surface.fill(constants.DARK_GREEN)

        winning_rank = game_data.get('winning_rank')

        # Draw Pay Table
        self.draw_pay_table(x=20, y=20, winning_rank=winning_rank)

        # Draw Money
        money_text = f"Money: ${game_data.get('money', 0)}"
        # Draw money animation if active
        if game_data.get('money_animation_active', False):
            amount = game_data.get('money_animation_amount', 0)
            anim_text = f"+${amount}"
            # Position slightly below the main money text
            self.draw_text(anim_text, 'money', constants.SCREEN_WIDTH - 150, 20 + constants.MONEY_ANIMATION_OFFSET_Y, constants.YELLOW)

        self.draw_text(money_text, 'money', constants.SCREEN_WIDTH - 150, 20, constants.GOLD)

        # Draw Hand (if available)
        hand = game_data.get('hand')
        held_indices = game_data.get('held_indices', [])
        current_state = game_data.get('current_state')

        # Only draw hand if not in start menu or if game over but hand exists (showing final hand)
        if hand and (current_state != constants.STATE_START_MENU or (current_state == constants.STATE_GAME_OVER and hand)):
             self.draw_hand(hand, held_indices)

        # Draw Messages
        message = game_data.get('message', '')
        result_message = game_data.get('result_message', '')

        if message:
            self.draw_text(message, 'message', constants.SCREEN_WIDTH // 2, constants.HAND_Y_POS - 60, constants.WHITE, center=True)
        if result_message:
             color = constants.GOLD if "WINNER" in result_message else constants.WHITE
             self.draw_text(result_message, 'result', constants.SCREEN_WIDTH // 2, constants.HAND_Y_POS - 100, color, center=True) # Position above hand

        # Draw Buttons
        # Quit Button (always visible)
        self.draw_button("QUIT", constants.QUIT_BUTTON_RECT, constants.RED, constants.WHITE)

        # Contextual Deal/Draw Button
        can_play = game_data.get('can_play', False)
        if current_state == constants.STATE_START_MENU:
            self.draw_button("DEAL", constants.DEAL_DRAW_BUTTON_RECT, constants.GREEN, constants.WHITE)
        elif current_state == constants.STATE_WAITING_FOR_HOLD:
            self.draw_button("DRAW", constants.DEAL_DRAW_BUTTON_RECT, constants.GREEN, constants.WHITE)
        elif current_state == constants.STATE_SHOWING_RESULT:
             button_color = constants.GREEN if can_play else constants.RED
             self.draw_button("DEAL", constants.DEAL_DRAW_BUTTON_RECT, button_color, constants.WHITE)

        # Game Over Screen elements
        if current_state == constants.STATE_GAME_OVER:
            self.draw_text("GAME OVER", 'game_over_large', constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 50, constants.RED, center=True)
            final_money = game_data.get('money', 0)
            self.draw_text(f"Final Money: ${final_money}", 'game_over_medium', constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2, constants.WHITE, center=True)
            self.draw_button("Play Again", constants.PLAY_AGAIN_BUTTON_RECT, constants.GREEN, constants.WHITE)

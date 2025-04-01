import pygame
import sys
import os
from typing import List, Tuple, Dict, Optional

from card import Card
from deck import Deck
from game_state import GameState
from poker_rules import evaluate_hand, PAY_TABLE, get_pay_table_string

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 71
CARD_HEIGHT = 96
HAND_Y_POS = 400
HAND_X_START = (SCREEN_WIDTH - 5 * (CARD_WIDTH + 10)) // 2
CARD_SPACING = 10
HELD_OFFSET = -20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
GOLD = (218, 165, 32)
DARK_GREEN = (0, 100, 0)

STATE_START_MENU = "START_MENU"
STATE_DEALING = "DEALING"
STATE_WAITING_FOR_HOLD = "WAITING_FOR_HOLD"
STATE_DRAWING = "DRAWING"
STATE_SHOWING_RESULT = "SHOWING_RESULT"
STATE_GAME_OVER = "GAME_OVER"

def load_card_images(path: str = "assets/cards") -> Dict[str, pygame.Surface]:
    images = {}
    if not os.path.exists(path):
        print(f"Error: Asset path not found: {os.path.abspath(path)}")
        print("Please ensure card images are in an 'assets/cards' directory.")
        print("Exiting.")
        sys.exit()

    try:
        for suit in ['S', 'H', 'D', 'C']:
            for rank in ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                filename = f"{rank}{suit}.png"
                filepath = os.path.join(path, filename)
                img = pygame.image.load(filepath).convert_alpha()
                images[f"{rank}{suit}"] = img
    except pygame.error as e:
        print(f"Error loading image: {e}")
        print(f"Searched in path: {os.path.abspath(path)}")
        sys.exit()
    except FileNotFoundError as e:
         print(f"Error: Card image file not found: {e}")
         print(f"Searched in path: {os.path.abspath(path)}")
         sys.exit()

    if len(images) < 52:
         print(f"Warning: Loaded only {len(images)} card images from {os.path.abspath(path)}. Expected 52.")

    return images

def get_card_image(card: Card, card_images: Dict[str, pygame.Surface]) -> pygame.Surface:
    # Map the suit symbols (like '♠') to the characters used in filenames ('S')
    suit_map = {
        "♠": "S",
        "♥": "H",
        "♦": "D",
        "♣": "C",
    }
    suit_short = suit_map.get(card.suit, '?') # Get the short suit, default to '?' if not found
    key = f"{card.rank}{suit_short}"
    if key not in card_images:
        print(f"Error: Image not found for card key: {key}")
        fallback_key = list(card_images.keys())[0]
        print(f"Using fallback image: {fallback_key}")
        return card_images.get(fallback_key, pygame.Surface((CARD_WIDTH, CARD_HEIGHT)))
    return card_images[key]

def draw_text(surface: pygame.Surface, text: str, size: int, x: int, y: int, color: Tuple[int, int, int], font_name: Optional[str] = None, center: bool = False):
    font = pygame.font.Font(pygame.font.match_font(font_name) if font_name else None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_hand(surface: pygame.Surface, hand: List[Card], held_indices: List[int], card_images: Dict[str, pygame.Surface], card_rects: List[pygame.Rect]):
    held_font = pygame.font.Font(None, 24)
    for i, card in enumerate(hand):
        img = get_card_image(card, card_images)
        rect = card_rects[i]
        y_pos = rect.y
        if i in held_indices:
            y_pos += HELD_OFFSET
            held_text = held_font.render("HELD", True, GOLD)
            held_rect = held_text.get_rect(centerx=rect.centerx, bottom=rect.top - 5)
            surface.blit(held_text, held_rect)

        surface.blit(img, (rect.x, y_pos))

def draw_pay_table(surface: pygame.Surface, font_size: int, x: int, y: int):
    pay_table_font = pygame.font.Font(None, font_size)
    line_height = pay_table_font.get_linesize()

    sorted_ranks = sorted(PAY_TABLE.keys(), key=lambda k: PAY_TABLE[k][1], reverse=True)

    draw_text(surface, "--- Pay Table (Bet: 1) ---", font_size + 2, x, y, GOLD)
    y += line_height * 1.5

    for rank in sorted_ranks:
        name, payout = PAY_TABLE[rank]
        if payout > 0:
            line = f"{name:<18}: {payout:>3}x"
            text_surface = pay_table_font.render(line, True, WHITE)
            surface.blit(text_surface, (x, y))
            y += line_height

def draw_button(surface: pygame.Surface, text: str, rect: pygame.Rect, color: Tuple[int, int, int], text_color: Tuple[int, int, int], font_size: int = 30):
    pygame.draw.rect(surface, color, rect, border_radius=5)
    draw_text(surface, text, font_size, rect.centerx, rect.centery, text_color, center=True)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Video Poker")
    clock = pygame.time.Clock()

    try:
        card_images = load_card_images()
    except SystemExit:
        pygame.quit()
        return

    money_font_size = 30
    message_font_size = 28
    pay_table_font_size = 20
    button_font_size = 30
    result_font_size = 36

    game_state_manager = GameState(starting_money=10)
    current_state = STATE_START_MENU
    hand: List[Card] = []
    held_indices: List[int] = []
    deck = Deck()
    message = ""
    result_message = ""
    final_hand_rank_name = ""

    card_rects: List[pygame.Rect] = []
    for i in range(5):
        x = HAND_X_START + i * (CARD_WIDTH + CARD_SPACING)
        rect = pygame.Rect(x, HAND_Y_POS, CARD_WIDTH, CARD_HEIGHT)
        card_rects.append(rect)

    button_width = 150
    button_height = 50
    deal_draw_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, HAND_Y_POS + CARD_HEIGHT + 30, button_width, button_height)
    quit_button_rect = pygame.Rect(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT - button_height - 20, button_width, button_height)
    play_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 50, button_width, button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if quit_button_rect.collidepoint(mouse_pos):
                    running = False
                    continue

                if current_state == STATE_START_MENU:
                     if deal_draw_button_rect.collidepoint(mouse_pos):
                         if game_state_manager.can_play():
                             game_state_manager.start_game()
                             deck = Deck()
                             hand = deck.deal(5)
                             held_indices = []
                             message = "Click cards to hold, then click DRAW"
                             result_message = ""
                             final_hand_rank_name = ""
                             current_state = STATE_WAITING_FOR_HOLD
                         else:
                             message = "Not enough money to play!"
                             current_state = STATE_GAME_OVER

                elif current_state == STATE_WAITING_FOR_HOLD:
                    for i, rect in enumerate(card_rects):
                        click_check_rect = rect.copy()
                        if i in held_indices:
                            click_check_rect.y += HELD_OFFSET
                        if click_check_rect.collidepoint(mouse_pos):
                            if i in held_indices:
                                held_indices.remove(i)
                            else:
                                held_indices.append(i)
                            held_indices.sort()
                            break

                    if deal_draw_button_rect.collidepoint(mouse_pos):
                        cards_to_draw = 5 - len(held_indices)
                        new_hand: List[Card] = []
                        
                        for i in range(5):
                             if i in held_indices:
                                 new_hand.append(hand[i])
                        
                        replace_indices = [i for i in range(5) if i not in held_indices]
                        
                        new_cards = deck.deal(cards_to_draw)
                        
                        final_hand_list = [None] * 5
                        held_card_idx = 0
                        new_card_idx = 0
                        for i in range(5):
                            if i in held_indices:
                                final_hand_list[i] = hand[i]
                            else:
                                if new_card_idx < len(new_cards):
                                    final_hand_list[i] = new_cards[new_card_idx]
                                    new_card_idx += 1
                                else:
                                     print("Error: Mismatch in drawing cards.")
                        
                        if None in final_hand_list:
                             print("Error: Final hand reconstruction failed.")
                             hand = hand
                        else:
                             hand = final_hand_list

                        rank, hand_name, payout = evaluate_hand(hand)
                        final_hand_rank_name = hand_name

                        if payout > 0:
                            winnings = payout * game_state_manager.cost_per_game
                            result_message = f"WINNER! {hand_name}! +${winnings}"
                            game_state_manager.add_winnings(winnings)
                        else:
                            result_message = f"Result: {hand_name}. No win."

                        message = "Click DEAL to play again."
                        current_state = STATE_SHOWING_RESULT

                elif current_state == STATE_SHOWING_RESULT:
                    if deal_draw_button_rect.collidepoint(mouse_pos):
                        if game_state_manager.can_play():
                            game_state_manager.start_game()
                            deck = Deck()
                            hand = deck.deal(5)
                            held_indices = []
                            message = "Click cards to hold, then click DRAW"
                            result_message = ""
                            final_hand_rank_name = ""
                            current_state = STATE_WAITING_FOR_HOLD
                        else:
                            message = "GAME OVER! Not enough money."
                            result_message = ""
                            current_state = STATE_GAME_OVER

                elif current_state == STATE_GAME_OVER:
                     if play_again_button_rect.collidepoint(mouse_pos):
                         game_state_manager = GameState(starting_money=10)
                         hand = []
                         held_indices = []
                         message = "Welcome! Click DEAL to start."
                         result_message = ""
                         final_hand_rank_name = ""
                         current_state = STATE_START_MENU

        screen.fill(DARK_GREEN)

        draw_pay_table(screen, pay_table_font_size, 20, 20)

        draw_text(screen, f"Money: ${game_state_manager.money}", money_font_size, SCREEN_WIDTH - 150, 20, GOLD)

        if current_state not in [STATE_START_MENU, STATE_GAME_OVER] or (current_state == STATE_GAME_OVER and hand):
             if hand:
                 draw_hand(screen, hand, held_indices, card_images, card_rects)

        if message:
            draw_text(screen, message, message_font_size, SCREEN_WIDTH // 2, HAND_Y_POS - 60, WHITE, center=True)
        if result_message:
             color = GOLD if "WINNER" in result_message else WHITE
             draw_text(screen, result_message, result_font_size, SCREEN_WIDTH // 2, HAND_Y_POS - 100, color, center=True)

        draw_button(screen, "QUIT", quit_button_rect, RED, WHITE, button_font_size)

        if current_state == STATE_START_MENU:
            button_text = "DEAL"
            button_color = GREEN
            draw_button(screen, button_text, deal_draw_button_rect, button_color, WHITE, button_font_size)
        elif current_state == STATE_WAITING_FOR_HOLD:
            button_text = "DRAW"
            button_color = GREEN
            draw_button(screen, button_text, deal_draw_button_rect, button_color, WHITE, button_font_size)
        elif current_state == STATE_SHOWING_RESULT:
             button_text = "DEAL"
             button_color = GREEN if game_state_manager.can_play() else RED
             draw_button(screen, button_text, deal_draw_button_rect, button_color, WHITE, button_font_size)

        if current_state == STATE_GAME_OVER:
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, RED, center=True)
            draw_text(screen, f"Final Money: ${game_state_manager.money}", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE, center=True)
            draw_button(screen, "Play Again", play_again_button_rect, GREEN, WHITE, button_font_size)
            message = ""
            result_message = ""

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

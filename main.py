import pygame
import sys
from typing import Dict, Any

# Local Imports
import constants
from card import Card
from deck import Deck
from game_state import GameState
from input_handler import InputHandler
from poker_rules import HandRank
from blackjack_rules import get_hand_value, is_blackjack, determine_winner, BLACKJACK_PAYOUT, WIN_PAYOUT, LOSS_PAYOUT, PUSH_PAYOUT

# --- Import Extracted Functions ---
# Renderer Functions
from renderer_functions.get_font import get_font
from renderer_functions.load_card_images import load_card_images
from renderer_functions.draw_top_menu import draw_top_menu
from renderer_functions.draw_game_selection_menu import draw_game_selection_menu
from renderer_functions.draw_game_screen import draw_game_screen
from renderer_functions.draw_settings_menu import draw_settings_menu
from renderer_functions.draw_confirm_exit import draw_confirm_exit
from renderer_functions.draw_blackjack_screen import draw_blackjack_screen
from renderer_functions.draw_roulette_screen import draw_roulette_screen
from renderer_functions.draw_spinning_wheel import draw_spinning_wheel
from renderer_functions.draw_text import draw_text

# Game Logic Functions
from game_functions.load_sounds import load_sounds
from game_functions.dummy_sound import DummySound
from game_functions.process_input import process_input
from game_functions.update_game import update_game
from game_functions.reset_game_variables import reset_game_variables
from game_functions.start_blackjack_round import start_blackjack_round
from game_functions.process_blackjack_action import process_blackjack_action
from game_functions.resolve_blackjack_round import resolve_blackjack_round
from game_functions.place_roulette_bet import place_roulette_bet
from game_functions.determine_roulette_result import determine_roulette_result
from game_functions.calculate_roulette_winnings import calculate_roulette_winnings

def main():
    # --- Pygame Initialization ---
    pygame.init()
    try:
        pygame.mixer.init()
        print("Sound system initialized.")
    except pygame.error as e:
        print(f"Warning: Failed to initialize sound system: {e}")
        print("Game will run without sound.")
        initial_sound_enabled = False
    else:
        initial_sound_enabled = True

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    # --- Helper Function to Apply Volume ---
    def apply_volume(volume_level: float, sounds_dict: Dict[str, Any]):
        """Sets the volume for all loaded sound objects."""
        print(f"Applying volume: {volume_level:.2f}")
        for name, sound_obj in sounds_dict.items():
            if hasattr(sound_obj, 'set_volume'):
                sound_obj.set_volume(volume_level)

    pygame.display.set_caption("Video Poker (Modular)")
    clock = pygame.time.Clock()

    # --- Load Assets ---
    fonts = {
        'money': get_font(constants.MONEY_FONT_SIZE),
        'message': get_font(constants.MESSAGE_FONT_SIZE),
        'pay_table': get_font(constants.PAY_TABLE_FONT_SIZE),
        'button': get_font(constants.BUTTON_FONT_SIZE),
        'result': get_font(constants.RESULT_FONT_SIZE),
        'multi_result': get_font(constants.MULTI_RESULT_FONT_SIZE),
        'hold': get_font(constants.HOLD_FONT_SIZE),
        'game_over_large': get_font(64),
        'game_over_medium': get_font(32),
    }
    constants.GREY = (128, 128, 128) # Add this if needed by wheel drawing
    card_images = load_card_images(constants.CARD_ASSET_PATH)

    # --- Initialize Game State Variables ---
    sounds = load_sounds(initial_sound_enabled)
    initial_volume = 0.7

    # --- Initialize Game Components ---
    input_handler = InputHandler()
    game_state_manager = GameState(starting_money=10)

    # --- Initialize Game State Variables ---
    game_state: Dict[str, Any] = {
        'current_state': constants.STATE_TOP_MENU,
        'hand': [],
        'multi_hands': [],
        'multi_results': [],
        'held_indices': [],
        'message': "",
        'result_message': "",
        'final_hand_rank': None,
        'total_winnings': 0,
        'money_animation_active': False,
        'money_animation_timer': 0,
        'money_animation_amount': 0,
        'result_message_flash_active': False,
        'result_message_flash_timer': 0,
        'result_message_flash_visible': True,
        'player_hand': [],
        'dealer_hand': [],
        'dealer_shows_one_card': False,
        'deck': Deck(),
        'running': True,
        'sound_enabled': initial_sound_enabled,
        'needs_money_reset': False,
        'confirm_exit_destination': None,
        'sound_setting_changed': False,
        'volume_level': initial_volume,
        'volume_changed': False,
        'previous_state_before_confirm': None,
        'confirm_action_type': None,
        # --- Add Roulette Specific State ---
        'roulette_bets': {},
        'roulette_winning_number': None,
        'roulette_spin_timer': 0,
    }

    # Apply initial volume
    apply_volume(game_state['volume_level'], sounds)

    # --- Main Game Loop ---
    while game_state['running']:
        # 1. Handle Input
        actions = input_handler.handle_events(game_state['current_state'])

        # 2. Process Input Actions -> Update State
        game_state = process_input(actions, game_state, game_state_manager, sounds, screen, fonts)

        # Handle specific state changes triggered by input processing
        if game_state.get('needs_money_reset', False):
            game_state_manager = GameState(starting_money=10)
            game_state['needs_money_reset'] = False

        # Check if quit action was processed
        if not game_state['running']:
            break

        # Reload sounds if setting changed
        if game_state.get('sound_setting_changed', False):
            sounds = load_sounds(game_state['sound_enabled'])
            game_state['sound_setting_changed'] = False
            apply_volume(game_state['volume_level'], sounds)

        # Apply volume changes if flagged
        if game_state.get('volume_changed', False):
            apply_volume(game_state['volume_level'], sounds)
            game_state['volume_changed'] = False

        # 3. Update Game Logic (Timers, Game Over Checks) -> Update State
        game_state = update_game(game_state, game_state_manager, sounds) # Pass sounds

        # 4. Render Output
        screen.fill(constants.DARK_GREEN)

        render_data = {
            'current_state': game_state['current_state'],
            'money': game_state_manager.money,
            'hand': game_state['hand'],
            'held_indices': game_state['held_indices'],
            'message': game_state['message'],
            'result_message': game_state['result_message'],
            'winning_rank': game_state['final_hand_rank'],
            'can_play': game_state_manager.can_play(),
            'multi_hands': game_state['multi_hands'],
            'multi_results': game_state['multi_results'],
            'money_animation_active': game_state['money_animation_active'],
            'money_animation_amount': game_state['money_animation_amount'],
        }

        if game_state['current_state'] == constants.STATE_TOP_MENU:
            draw_top_menu(screen, fonts)
        elif game_state['current_state'] == constants.STATE_GAME_SELECTION:
            draw_game_selection_menu(screen, fonts, game_state_manager.money)
        elif game_state['current_state'] == constants.STATE_SETTINGS:
            draw_settings_menu(screen, fonts, game_state['sound_enabled'], game_state['volume_level'])
        elif game_state['current_state'] == constants.STATE_CONFIRM_EXIT:
            draw_confirm_exit(screen, fonts, game_state)
        elif game_state['current_state'] in [constants.STATE_BLACKJACK_IDLE, constants.STATE_BLACKJACK_PLAYER_TURN,
                                             constants.STATE_BLACKJACK_DEALER_TURN, constants.STATE_BLACKJACK_SHOWING_RESULT]:
            draw_blackjack_screen(screen, fonts, card_images, game_state, game_state_manager)
        elif game_state['current_state'] in [constants.STATE_ROULETTE_BETTING, constants.STATE_ROULETTE_SPINNING, constants.STATE_ROULETTE_RESULT]:
            # draw_roulette_screen now handles drawing the table OR the spinning wheel based on the state
            draw_roulette_screen(screen, fonts, game_state, game_state_manager)
        else:
            # Ensure render_data includes necessary items like money animation status
            render_data['money_animation_active'] = game_state.get('money_animation_active', False)
            render_data['money_animation_amount'] = game_state.get('money_animation_amount', 0)
            render_data['result_message_flash_active'] = game_state.get('result_message_flash_active', False)
            render_data['result_message_flash_visible'] = game_state.get('result_message_flash_visible', True)

            draw_game_screen(screen, fonts, card_images, render_data, game_state)


        pygame.display.flip()

        # 5. Control Frame Rate
        clock.tick(30)

    # --- Clean up ---
    pygame.quit()
    print("Game exited normally.")
    sys.exit()


if __name__ == "__main__":
    main()

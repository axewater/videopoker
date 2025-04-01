import pygame
import sys
from typing import Dict, Any

# Local Imports
import constants
from card import Card # Keep if needed directly, maybe not
from deck import Deck # Keep for type hinting if needed
from game_state import GameState
from input_handler import InputHandler
from poker_rules import HandRank # Keep for type hinting

# --- Import Extracted Functions ---
# Renderer Functions
from renderer_functions.get_font import get_font
from renderer_functions.load_card_images import load_card_images
from renderer_functions.draw_top_menu import draw_top_menu
from renderer_functions.draw_game_selection_menu import draw_game_selection_menu
from renderer_functions.draw_game_screen import draw_game_screen
from renderer_functions.draw_settings_menu import draw_settings_menu
from renderer_functions.draw_confirm_exit import draw_confirm_exit

# Game Logic Functions
from game_functions.load_sounds import load_sounds
from game_functions.dummy_sound import DummySound # For type hinting
from game_functions.process_input import process_input
from game_functions.update_game import update_game
from game_functions.reset_game_variables import reset_game_variables


def main():
    # --- Pygame Initialization ---
    pygame.init()
    try: # Try initializing mixer early
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
            if hasattr(sound_obj, 'set_volume'): # Check if it's a real sound, not DummySound
                sound_obj.set_volume(volume_level)
            # else: print(f"Skipping volume set for {name} (DummySound)") # Debug

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
    card_images = load_card_images(constants.CARD_ASSET_PATH)

    # --- Initialize Game State Variables ---
    sounds = load_sounds(initial_sound_enabled)
    initial_volume = 0.7 # Default volume level (70%)

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
        'deck': Deck(), # Start with a deck, even if unused initially
        'running': True,
        'sound_enabled': initial_sound_enabled, # Add sound setting
        'needs_money_reset': False, # Flag for play again action
        'confirm_exit_destination': None, # State to go to after confirming exit
        'sound_setting_changed': False, # Flag to reload sounds if setting changed
        'volume_level': initial_volume, # Add volume level (0.0 to 1.0)
        'volume_changed': False, # Flag to apply volume changes
        'previous_state_before_confirm': None, # Store previous state for confirmation dialog
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
            game_state_manager = GameState(starting_money=10) # Re-initialize money
            game_state['needs_money_reset'] = False # Reset flag

        # Check if quit action was processed
        if not game_state['running']:
            break

        # Reload sounds if setting changed
        if game_state.get('sound_setting_changed', False):
            sounds = load_sounds(game_state['sound_enabled'])
            game_state['sound_setting_changed'] = False # Reset flag
            # Re-apply volume when sounds are reloaded
            apply_volume(game_state['volume_level'], sounds)

        # Apply volume changes if flagged
        if game_state.get('volume_changed', False):
            apply_volume(game_state['volume_level'], sounds)
            game_state['volume_changed'] = False # Reset flag

        # 3. Update Game Logic (Timers, Game Over Checks) -> Update State
        game_state = update_game(game_state, game_state_manager)

        # 4. Render Output
        screen.fill(constants.DARK_GREEN) # Default background

        render_data = {
            'current_state': game_state['current_state'],
            'money': game_state_manager.money,
            'hand': game_state['hand'],
            'held_indices': game_state['held_indices'],
            'message': game_state['message'],
            'result_message': game_state['result_message'],
            'winning_rank': game_state['final_hand_rank'],
            'can_play': game_state_manager.can_play(), # Check current playability
            'multi_hands': game_state['multi_hands'],
            'multi_results': game_state['multi_results'],
            'money_animation_active': game_state['money_animation_active'],
            'money_animation_amount': game_state['money_animation_amount'],
        }

        if game_state['current_state'] == constants.STATE_TOP_MENU:
            draw_top_menu(screen, fonts)
        elif game_state['current_state'] == constants.STATE_GAME_SELECTION:
            draw_game_selection_menu(screen, fonts)
        elif game_state['current_state'] == constants.STATE_SETTINGS:
            draw_settings_menu(screen, fonts, game_state['sound_enabled'], game_state['volume_level'])
        elif game_state['current_state'] == constants.STATE_CONFIRM_EXIT:
            draw_confirm_exit(screen, fonts)
        else:
            # Draw the main game screen elements using the combined data
            draw_game_screen(screen, fonts, card_images, render_data, game_state)

        pygame.display.flip() # Update the full screen

        # 5. Control Frame Rate
        clock.tick(30) # Limit to 30 FPS

    # --- Clean up ---
    pygame.quit()
    print("Game exited normally.")
    sys.exit()


if __name__ == "__main__":
    main()

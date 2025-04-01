# /game_functions/process_input.py
from typing import List, Tuple, Optional, Dict, Any
import pygame # Keep pygame for type hints if needed

# --- Config Imports ---
import config_states as states
import config_actions as actions_cfg

# --- Local Imports ---
from game_state import GameState
# --- Import New Handlers ---
from .handle_menu_input import handle_menu_action
from .handle_poker_input import handle_poker_action
from .handle_blackjack_input import handle_blackjack_action
from .handle_roulette_input import handle_roulette_action
from .handle_slots_input import handle_slots_action
from .handle_confirmation_input import handle_confirmation_action

def process_input(actions: List[Tuple[str, Optional[any]]], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any], screen: Optional[pygame.Surface] = None, fonts: Optional[Dict[str, pygame.font.Font]] = None) -> Dict[str, Any]:
    """
    Processes actions received from the InputHandler and updates the game state.
    Returns a dictionary containing the potentially modified game state variables.
    """
    # Start with the current state, modify it based on actions
    new_game_state = current_game_state.copy()

    for action, payload in actions:
        current_state_str = new_game_state['current_state']

        # --- Dispatch to the appropriate handler based on current state ---

        # Menu States (Top, Game Select, Settings, Game Over)
        if current_state_str in [states.STATE_TOP_MENU, states.STATE_GAME_SELECTION, states.STATE_SETTINGS, states.STATE_GAME_OVER]:
            new_game_state = handle_menu_action(action, payload, new_game_state, game_state_manager, sounds)

        # Poker States
        elif current_state_str in [states.STATE_DRAW_POKER_IDLE, states.STATE_DRAW_POKER_WAITING_FOR_HOLD, states.STATE_DRAW_POKER_SHOWING_RESULT,
                                   states.STATE_MULTI_POKER_IDLE, states.STATE_MULTI_POKER_WAITING_FOR_HOLD, states.STATE_MULTI_POKER_SHOWING_RESULT]:
            new_game_state = handle_poker_action(action, payload, new_game_state, game_state_manager, sounds)

        # Blackjack States
        elif current_state_str in [states.STATE_BLACKJACK_IDLE, states.STATE_BLACKJACK_PLAYER_TURN, states.STATE_BLACKJACK_SHOWING_RESULT]:
             # Note: STATE_BLACKJACK_DEALER_TURN doesn't typically handle direct player input
            new_game_state = handle_blackjack_action(action, payload, new_game_state, game_state_manager, sounds)

        # Roulette States
        elif current_state_str in [states.STATE_ROULETTE_BETTING, states.STATE_ROULETTE_SPINNING, states.STATE_ROULETTE_RESULT]:
            new_game_state = handle_roulette_action(action, payload, new_game_state, game_state_manager, sounds)

        # Slots States
        elif current_state_str in [states.STATE_SLOTS_IDLE, states.STATE_SLOTS_SPINNING, states.STATE_SLOTS_SHOWING_RESULT]:
            new_game_state = handle_slots_action(action, payload, new_game_state, game_state_manager, sounds)

        # Confirmation State
        elif current_state_str == states.STATE_CONFIRM_EXIT:
            new_game_state = handle_confirmation_action(action, payload, new_game_state, game_state_manager, sounds)

        # Handle global quit action if not handled by specific state handlers (e.g., top menu quit)
        # Note: Quit action now triggers confirmation, handled by handle_confirmation_action
        elif action == actions_cfg.ACTION_QUIT:
             # If quit is pressed outside of a state that handles it (like Top Menu), trigger confirmation
             if current_state_str not in [states.STATE_TOP_MENU, states.STATE_CONFIRM_EXIT]: # Avoid double confirmation
                 if sounds.get("button"): sounds["button"].play()
                 new_game_state['confirm_action_type'] = 'QUIT'
                 new_game_state['previous_state_before_confirm'] = current_state_str
                 new_game_state['current_state'] = states.STATE_CONFIRM_EXIT

        # If the state changes, the next action in the list will be processed
        # according to the *new* state's handler in the next iteration.

    # --- End of action processing loop ---

    # The 'running' state is now managed within handle_confirmation_action

    return new_game_state

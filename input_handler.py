# /input_handler.py
import pygame
from typing import List, Optional, Tuple

# Config Imports
import config_states as states
import config_actions as actions_cfg

# Import the new handler functions
from input_handlers.menu_input import handle_menu_event
from input_handlers.poker_input import handle_poker_event
from input_handlers.blackjack_input import handle_blackjack_event
from input_handlers.roulette_input import handle_roulette_event
from input_handlers.slots_input import handle_slots_event
from input_handlers.baccarat_input import handle_baccarat_event
from input_handlers.confirmation_input import handle_confirmation_event

# Mapping states to their handler functions for cleaner dispatch
STATE_HANDLERS = {
    states.STATE_TOP_MENU: handle_menu_event,
    states.STATE_GAME_SELECTION: handle_menu_event,
    states.STATE_SETTINGS: handle_menu_event,
    states.STATE_GAME_OVER: handle_menu_event, # Game Over uses menu handler for Play Again
    states.STATE_DRAW_POKER_IDLE: handle_poker_event,
    states.STATE_DRAW_POKER_WAITING_FOR_HOLD: handle_poker_event,
    states.STATE_DRAW_POKER_SHOWING_RESULT: handle_poker_event,
    states.STATE_MULTI_POKER_IDLE: handle_poker_event,
    states.STATE_MULTI_POKER_WAITING_FOR_HOLD: handle_poker_event,
    states.STATE_MULTI_POKER_SHOWING_RESULT: handle_poker_event,
    states.STATE_BLACKJACK_IDLE: handle_blackjack_event,
    states.STATE_BLACKJACK_PLAYER_TURN: handle_blackjack_event,
    states.STATE_BLACKJACK_SHOWING_RESULT: handle_blackjack_event,
    # Note: STATE_BLACKJACK_DEALER_TURN typically doesn't need direct input handling
    states.STATE_ROULETTE_BETTING: handle_roulette_event,
    states.STATE_ROULETTE_SPINNING: handle_roulette_event,
    states.STATE_ROULETTE_RESULT: handle_roulette_event,
    states.STATE_SLOTS_IDLE: handle_slots_event,
    states.STATE_SLOTS_SPINNING: handle_slots_event,
    states.STATE_SLOTS_SHOWING_RESULT: handle_slots_event,
    states.STATE_BACCARAT_BETTING: handle_baccarat_event,
    states.STATE_BACCARAT_DEALING: handle_baccarat_event,
    states.STATE_BACCARAT_DRAWING: handle_baccarat_event,
    states.STATE_BACCARAT_RESULT: handle_baccarat_event,
    states.STATE_CONFIRM_EXIT: handle_confirmation_event,
}

class InputHandler:
    """Handles user input events."""

    def __init__(self):
        """Initializes the input handler."""
        # No specific state needed here for now, but could hold things
        # like previous mouse state if needed for drag detection etc.
        pass

    def handle_events(self, current_state: str) -> List[Tuple[str, Optional[any]]]:
        """
        Processes Pygame events and returns a list of actions.
        Each action is a tuple: (ACTION_TYPE, payload).
        Payload is None for simple actions, or data like card index for HOLD_TOGGLE.
        """
        all_actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Add the global quit action immediately
                all_actions.append((actions_cfg.ACTION_QUIT, None))
                # Skip further processing for this event
                continue

            # Find the appropriate handler for the current state
            handler = STATE_HANDLERS.get(current_state)

            if handler:
                # Call the specific handler function for this event and state
                state_actions = handler(event, current_state)
                if state_actions:
                    all_actions.extend(state_actions)
            else:
                # Optional: Log a warning if no handler is found for a state
                # print(f"Warning: No input handler found for state: {current_state}")
                pass # Ignore events if no handler is defined for the state

        return all_actions # Return the list of all processed actions for this frame

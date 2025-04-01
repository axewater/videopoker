import pygame
from typing import List, Optional, Tuple

import constants

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
        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append((constants.ACTION_QUIT, None))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # --- State-dependent checks ---
                if current_state == constants.STATE_TOP_MENU:
                    if constants.PLAY_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_GOTO_PLAY, None))
                    elif constants.SETTINGS_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_GOTO_SETTINGS, None))
                    elif constants.TOP_MENU_QUIT_BUTTON_RECT.collidepoint(mouse_pos): # Check Quit button only when in Top Menu
                         actions.append((constants.ACTION_QUIT, None)) # Quit from top menu

                elif current_state == constants.STATE_GAME_SELECTION:
                    if constants.DRAW_POKER_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_CHOOSE_DRAW_POKER, None))
                    elif constants.MULTI_POKER_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_CHOOSE_MULTI_POKER, None))
                    elif constants.BLACKJACK_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_CHOOSE_BLACKJACK, None))
                    elif constants.ROULETTE_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_CHOOSE_ROULETTE, None))
                    elif constants.SETTINGS_BACK_BUTTON_RECT.collidepoint(mouse_pos): # Back button on game select
                        actions.append((constants.ACTION_RETURN_TO_TOP_MENU, None))

                elif current_state == constants.STATE_BLACKJACK_PLAYER_TURN:
                    if constants.BLACKJACK_HIT_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_BLACKJACK_HIT, None))
                    elif constants.BLACKJACK_STAND_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_BLACKJACK_STAND, None))
                    elif constants.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos): # Allow exit during turn
                        actions.append((constants.ACTION_RETURN_TO_MENU, None))

                elif current_state in [constants.STATE_DRAW_POKER_IDLE, constants.STATE_MULTI_POKER_IDLE,
                                       constants.STATE_DRAW_POKER_WAITING_FOR_HOLD, constants.STATE_MULTI_POKER_WAITING_FOR_HOLD,
                                       constants.STATE_DRAW_POKER_SHOWING_RESULT, constants.STATE_MULTI_POKER_SHOWING_RESULT]:
                    # Check Deal/Draw button first
                    if constants.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_DEAL_DRAW, None))
                    elif constants.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_RETURN_TO_MENU, None))
                    else:
                        # Check card clicks (only if Deal/Draw or Menu wasn't clicked)
                        for i, card_rect in enumerate(constants.CARD_RECTS):
                            if card_rect.collidepoint(mouse_pos):
                                actions.append((constants.ACTION_HOLD_TOGGLE, i))
                                break # Process only one card click per event

                        # Check hold button clicks (if card wasn't clicked)
                        else: # This 'else' belongs to the 'for' loop
                            for i, hold_rect in enumerate(constants.HOLD_BUTTON_RECTS):
                                if hold_rect.collidepoint(mouse_pos):
                                    actions.append((constants.ACTION_HOLD_TOGGLE, i))
                                    break # Process only one hold button click

                elif current_state in [constants.STATE_BLACKJACK_IDLE, constants.STATE_BLACKJACK_SHOWING_RESULT]:
                     # Check Deal button first
                    if constants.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_DEAL_DRAW, None))
                    elif constants.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_RETURN_TO_MENU, None))

                elif current_state == constants.STATE_GAME_OVER:
                    if constants.PLAY_AGAIN_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_PLAY_AGAIN, None))

                elif current_state == constants.STATE_SETTINGS:
                    if constants.SOUND_TOGGLE_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_TOGGLE_SOUND, None))
                    elif constants.VOLUME_DOWN_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_VOLUME_DOWN, None))
                    elif constants.VOLUME_UP_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_VOLUME_UP, None))
                    elif constants.SETTINGS_BACK_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_RETURN_TO_TOP_MENU, None))

                elif current_state == constants.STATE_CONFIRM_EXIT:
                    if constants.CONFIRM_YES_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_CONFIRM_YES, None))
                    elif constants.CONFIRM_NO_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_CONFIRM_NO, None))

        return actions

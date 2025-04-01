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

                # --- Always check Quit button ---
                if constants.QUIT_BUTTON_RECT.collidepoint(mouse_pos):
                    actions.append((constants.ACTION_QUIT, None))
                    continue # Don't process other clicks if quit is clicked

                # --- Always check Return to Menu button (if not already in menu) ---
                if current_state != constants.STATE_MAIN_MENU and constants.RETURN_TO_MENU_BUTTON_RECT.collidepoint(mouse_pos):
                    actions.append((constants.ACTION_RETURN_TO_MENU, None))
                    continue # Don't process other clicks if returning to menu

                # --- State-dependent checks ---
                if current_state == constants.STATE_MAIN_MENU:
                    if constants.DRAW_POKER_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_CHOOSE_DRAW_POKER, None))
                    elif constants.MULTI_POKER_BUTTON_RECT.collidepoint(mouse_pos):
                        # Add action for multi poker later
                        # actions.append((constants.ACTION_CHOOSE_MULTI_POKER, None))
                        print("Multi Poker selected (not implemented yet)") # Placeholder

                elif current_state == constants.STATE_DRAW_POKER_WAITING_FOR_HOLD:
                    # Check Deal/Draw button first
                    if constants.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_DEAL_DRAW, None))
                    else:
                        # Check card clicks
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

                elif current_state == constants.STATE_DRAW_POKER_SHOWING_RESULT:
                    if constants.DEAL_DRAW_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_DEAL_DRAW, None))

                elif current_state == constants.STATE_GAME_OVER:
                    if constants.PLAY_AGAIN_BUTTON_RECT.collidepoint(mouse_pos):
                        actions.append((constants.ACTION_PLAY_AGAIN, None))

        return actions

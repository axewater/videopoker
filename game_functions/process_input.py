from typing import List, Tuple, Optional, Dict, Any

import constants
from game_state import GameState
from .start_draw_poker_round import start_draw_poker_round
from .start_multi_poker_round import start_multi_poker_round
from .process_drawing import process_drawing
from .process_multi_drawing import process_multi_drawing
from .reset_game_variables import reset_game_variables

def process_input(actions: List[Tuple[str, Optional[any]]], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes actions received from the InputHandler and updates the game state.
    Returns a dictionary containing the potentially modified game state variables.
    """
    # Start with the current state, modify it based on actions
    new_game_state = current_game_state.copy()
    running = new_game_state.get('running', True) # Get running state

    for action, payload in actions:
        if action == constants.ACTION_QUIT:
            sounds["button"].play() # Optional: sound on quit
            running = False
            break # Exit loop immediately on quit

        elif action == constants.ACTION_CHOOSE_DRAW_POKER:
            if new_game_state['current_state'] == constants.STATE_MAIN_MENU:
                sounds["button"].play()
                round_state = start_draw_poker_round(game_state_manager, sounds)
                new_game_state.update(round_state) # Update state with results

        elif action == constants.ACTION_CHOOSE_MULTI_POKER:
            if new_game_state['current_state'] == constants.STATE_MAIN_MENU:
                sounds["button"].play()
                round_state = start_multi_poker_round(game_state_manager, sounds)
                new_game_state.update(round_state)

        elif action == constants.ACTION_RETURN_TO_MENU:
            if new_game_state['current_state'] != constants.STATE_MAIN_MENU:
                sounds["button"].play()
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['message'] = "" # Clear any lingering game messages
                new_game_state['current_state'] = constants.STATE_MAIN_MENU

        elif action == constants.ACTION_DEAL_DRAW:
            current_state_str = new_game_state['current_state']
            if current_state_str == constants.STATE_DRAW_POKER_WAITING_FOR_HOLD:
                sounds["button"].play()
                draw_results = process_drawing(
                    new_game_state['hand'],
                    new_game_state['held_indices'],
                    new_game_state['deck'],
                    game_state_manager,
                    sounds
                )
                new_game_state.update(draw_results)
            elif current_state_str == constants.STATE_MULTI_POKER_WAITING_FOR_HOLD:
                 sounds["button"].play()
                 multi_draw_results = process_multi_drawing(
                     new_game_state['hand'],
                     new_game_state['held_indices'],
                     game_state_manager,
                     sounds
                 )
                 new_game_state.update(multi_draw_results)
            elif current_state_str == constants.STATE_DRAW_POKER_SHOWING_RESULT:
                sounds["button"].play()
                # Check if can play before starting next round
                if game_state_manager.money >= 1: # Cost for next draw poker game
                    round_state = start_draw_poker_round(game_state_manager, sounds)
                    new_game_state.update(round_state)
                else:
                    # Not enough money, transition to Game Over from here
                    reset_state = reset_game_variables()
                    new_game_state.update(reset_state)
                    new_game_state['message'] = "GAME OVER! Not enough money."
                    new_game_state['current_state'] = constants.STATE_GAME_OVER
            elif current_state_str == constants.STATE_MULTI_POKER_SHOWING_RESULT:
                 sounds["button"].play()
                 cost_next_multi = constants.NUM_MULTI_HANDS
                 if game_state_manager.money >= cost_next_multi:
                     round_state = start_multi_poker_round(game_state_manager, sounds)
                     new_game_state.update(round_state)
                 else:
                     # Not enough money for multi-poker
                     reset_state = reset_game_variables()
                     new_game_state.update(reset_state)
                     new_game_state['message'] = f"GAME OVER! Need ${cost_next_multi} for Multi Poker."
                     new_game_state['current_state'] = constants.STATE_GAME_OVER


        elif action == constants.ACTION_HOLD_TOGGLE:
            if new_game_state['current_state'] in [constants.STATE_DRAW_POKER_WAITING_FOR_HOLD, constants.STATE_MULTI_POKER_WAITING_FOR_HOLD]:
                index = payload
                if index is not None and 0 <= index < 5: # Basic validation
                    held_indices = new_game_state['held_indices']
                    if index in held_indices:
                        held_indices.remove(index)
                        sounds["hold"].play()
                    else:
                        held_indices.append(index)
                        held_indices.sort() # Keep sorted for consistency
                        sounds["hold"].play()
                    new_game_state['held_indices'] = held_indices # Update state

        elif action == constants.ACTION_PLAY_AGAIN:
             if new_game_state['current_state'] == constants.STATE_GAME_OVER:
                 sounds["button"].play()
                 # Reset money by re-initializing the manager
                 # This function shouldn't re-init, main loop should handle this logic maybe?
                 # For now, let's just reset state and go to menu. Money reset needs to happen in main.
                 reset_state = reset_game_variables()
                 new_game_state.update(reset_state)
                 new_game_state['current_state'] = constants.STATE_MAIN_MENU
                 # Signal that money needs reset? Or handle in main loop based on PLAY_AGAIN action.
                 new_game_state['needs_money_reset'] = True # Add a flag


    new_game_state['running'] = running # Update running state
    return new_game_state

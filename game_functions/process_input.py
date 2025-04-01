# /game_functions/process_input.py
from typing import List, Tuple, Optional, Dict, Any
import pygame, random

import constants
from game_state import GameState
from .start_draw_poker_round import start_draw_poker_round
from .start_multi_poker_round import start_multi_poker_round
from .start_blackjack_round import start_blackjack_round
from .process_drawing import process_drawing
from .place_roulette_bet import place_roulette_bet
from .process_multi_drawing import process_multi_drawing
from .process_blackjack_action import process_blackjack_action
from .reset_game_variables import reset_game_variables
# Need determine_roulette_result for spin action completion, but spin starts here
# Need calculate_roulette_winnings? No, that's after spin.

def process_input(actions: List[Tuple[str, Optional[any]]], current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any], screen: Optional[pygame.Surface] = None, fonts: Optional[Dict[str, pygame.font.Font]] = None) -> Dict[str, Any]:
    """
    Processes actions received from the InputHandler and updates the game state.
    Returns a dictionary containing the potentially modified game state variables.
    """
    # Start with the current state, modify it based on actions
    new_game_state = current_game_state.copy()
    running = new_game_state.get('running', True) # Get running state

    for action, payload in actions:
        if action == constants.ACTION_QUIT:
            if sounds.get("button"): sounds["button"].play() # Optional: sound on quit
            # Trigger confirmation dialog instead of quitting directly
            new_game_state['confirm_action_type'] = 'QUIT'
            new_game_state['previous_state_before_confirm'] = new_game_state['current_state'] # Store current state
            new_game_state['current_state'] = constants.STATE_CONFIRM_EXIT
            # Note: We don't set running = False here anymore, it's handled by CONFIRM_YES
            # break # Don't break, let other actions process if needed, though unlikely after quit click

        # --- Top Menu Actions ---
        elif action == constants.ACTION_GOTO_PLAY:
            if new_game_state['current_state'] == constants.STATE_TOP_MENU:
                if sounds.get("button"): sounds["button"].play()
                new_game_state['current_state'] = constants.STATE_GAME_SELECTION

        elif action == constants.ACTION_GOTO_SETTINGS:
            if new_game_state['current_state'] == constants.STATE_TOP_MENU:
                if sounds.get("button"): sounds["button"].play()
                new_game_state['current_state'] = constants.STATE_SETTINGS

        # --- Settings Actions ---
        elif action == constants.ACTION_TOGGLE_SOUND:
            if new_game_state['current_state'] == constants.STATE_SETTINGS:
                new_game_state['sound_enabled'] = not new_game_state['sound_enabled']
                new_game_state['sound_setting_changed'] = True # Flag to reload sounds in main loop
                # Play button sound *after* potentially enabling sound
                if new_game_state['sound_enabled'] and sounds.get("button"): sounds["button"].play()

        elif action == constants.ACTION_VOLUME_DOWN:
             if new_game_state['current_state'] == constants.STATE_SETTINGS and new_game_state['sound_enabled']:
                 current_volume = new_game_state.get('volume_level', 0.7)
                 new_volume = max(0.0, current_volume - 0.1) # Decrease by 10%, min 0
                 new_game_state['volume_level'] = round(new_volume, 2) # Round to avoid float issues
                 new_game_state['volume_changed'] = True # Flag to apply volume in main loop
                 if sounds.get("button"): sounds["button"].play()

        elif action == constants.ACTION_VOLUME_UP:
             if new_game_state['current_state'] == constants.STATE_SETTINGS and new_game_state['sound_enabled']:
                 current_volume = new_game_state.get('volume_level', 0.7)
                 new_volume = min(1.0, current_volume + 0.1) # Increase by 10%, max 1
                 new_game_state['volume_level'] = round(new_volume, 2) # Round to avoid float issues
                 new_game_state['volume_changed'] = True # Flag to apply volume in main loop
                 if sounds.get("button"): sounds["button"].play()


        elif action == constants.ACTION_RETURN_TO_TOP_MENU: # From Settings or Game Selection
            if new_game_state['current_state'] in [constants.STATE_SETTINGS, constants.STATE_GAME_SELECTION]:
                if sounds.get("button"): sounds["button"].play()
                new_game_state['current_state'] = constants.STATE_TOP_MENU

        # --- Game Selection Actions ---
        elif action == constants.ACTION_CHOOSE_DRAW_POKER:
            if new_game_state['current_state'] == constants.STATE_GAME_SELECTION:
                if sounds.get("button"): sounds["button"].play()
                # Transition to IDLE state, don't start round yet
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['current_state'] = constants.STATE_DRAW_POKER_IDLE
                new_game_state['message'] = "Click DEAL to start ($1)"

        elif action == constants.ACTION_CHOOSE_MULTI_POKER:
            if new_game_state['current_state'] == constants.STATE_GAME_SELECTION:
                if sounds.get("button"): sounds["button"].play()
                # Transition to IDLE state
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['current_state'] = constants.STATE_MULTI_POKER_IDLE
                new_game_state['message'] = f"Click DEAL to start (${constants.NUM_MULTI_HANDS})"

        elif action == constants.ACTION_CHOOSE_BLACKJACK:
            if new_game_state['current_state'] == constants.STATE_GAME_SELECTION:
                if sounds.get("button"): sounds["button"].play()
                # Transition to Blackjack IDLE state
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['current_state'] = constants.STATE_BLACKJACK_IDLE
                new_game_state['message'] = "Click DEAL to play Blackjack ($1)"
                new_game_state['player_hand'] = [] # Ensure blackjack state is clean
                new_game_state['dealer_hand'] = []

        elif action == constants.ACTION_CHOOSE_ROULETTE:
            if new_game_state['current_state'] == constants.STATE_GAME_SELECTION:
                if sounds.get("button"): sounds["button"].play()
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                new_game_state['current_state'] = constants.STATE_ROULETTE_BETTING
                new_game_state['message'] = "Place your bets!" # Initial Roulette message
                new_game_state['roulette_bets'] = {}
                new_game_state['roulette_winning_number'] = None
                new_game_state['roulette_total_bet'] = 0

        elif action == constants.ACTION_RESTART_GAME:
            if new_game_state['current_state'] == constants.STATE_GAME_SELECTION:
                if sounds.get("button"): sounds["button"].play()
                # Trigger confirmation dialog specifically for restart
                new_game_state['confirm_action_type'] = 'RESTART' # Set the reason for confirmation
                new_game_state['previous_state_before_confirm'] = constants.STATE_GAME_SELECTION # Store where to return if 'No'
                new_game_state['current_state'] = constants.STATE_CONFIRM_EXIT

        elif action == constants.ACTION_RETURN_TO_MENU:
            # This action now means "Return to Game Selection Menu" from a game
            current_state_str = new_game_state['current_state']
            # Check if in a game state where returning might lose progress or is disruptive
            if current_state_str in [constants.STATE_DRAW_POKER_WAITING_FOR_HOLD,
                                     constants.STATE_MULTI_POKER_WAITING_FOR_HOLD,
                                     constants.STATE_BLACKJACK_PLAYER_TURN,
                                     constants.STATE_ROULETTE_BETTING, # Confirm if bets placed
                                     constants.STATE_ROULETTE_SPINNING]: # Confirm/disallow during spin
                if sounds.get("button"): sounds["button"].play()

                # Disallow exit during spin
                if current_state_str == constants.STATE_ROULETTE_SPINNING:
                    new_game_state['message'] = "Cannot exit while wheel is spinning!"
                    # Keep current state, don't show confirmation
                # If betting in roulette and bets exist, confirm
                elif current_state_str == constants.STATE_ROULETTE_BETTING and new_game_state.get('roulette_bets'):
                    new_game_state['confirm_action_type'] = 'EXIT'
                    new_game_state['confirm_exit_destination'] = constants.STATE_GAME_SELECTION
                    new_game_state['previous_state_before_confirm'] = current_state_str
                    new_game_state['current_state'] = constants.STATE_CONFIRM_EXIT
                # If betting in roulette but no bets placed yet, allow direct exit
                elif current_state_str == constants.STATE_ROULETTE_BETTING and not new_game_state.get('roulette_bets'):
                     reset_state = reset_game_variables()
                     new_game_state.update(reset_state)
                     new_game_state['message'] = ""
                     new_game_state['current_state'] = constants.STATE_GAME_SELECTION
                # Otherwise (Poker hold states, Blackjack turn), confirm exit
                else:
                    new_game_state['confirm_action_type'] = 'EXIT'
                    new_game_state['confirm_exit_destination'] = constants.STATE_GAME_SELECTION
                    new_game_state['previous_state_before_confirm'] = current_state_str
                    new_game_state['current_state'] = constants.STATE_CONFIRM_EXIT

            # If in a state where returning is safe (idle, showing result)
            elif current_state_str not in [constants.STATE_TOP_MENU, constants.STATE_GAME_SELECTION, constants.STATE_SETTINGS, constants.STATE_GAME_OVER, constants.STATE_CONFIRM_EXIT]:
                if sounds.get("button"): sounds["button"].play()
                reset_state = reset_game_variables()
                new_game_state.update(reset_state)
                # Clear potential game-specific state
                new_game_state['player_hand'] = []
                new_game_state['dealer_hand'] = []
                new_game_state['multi_hands'] = []
                new_game_state['multi_results'] = []
                new_game_state['roulette_bets'] = {} # Clear roulette bets too
                new_game_state['message'] = "" # Clear any lingering game messages
                new_game_state['current_state'] = constants.STATE_GAME_SELECTION

        elif action == constants.ACTION_DEAL_DRAW:
            current_state_str = new_game_state['current_state']
            if current_state_str == constants.STATE_DRAW_POKER_IDLE: # Start new Draw Poker game
                if sounds.get("button"): sounds["button"].play()
                round_state = start_draw_poker_round(game_state_manager, sounds)
                new_game_state.update(round_state)
            elif current_state_str == constants.STATE_MULTI_POKER_IDLE: # Start new Multi Poker game
                if sounds.get("button"): sounds["button"].play()
                round_state = start_multi_poker_round(game_state_manager, sounds)
                new_game_state.update(round_state)
            elif current_state_str == constants.STATE_DRAW_POKER_WAITING_FOR_HOLD: # Process Draw Poker draw
                if sounds.get("button"): sounds["button"].play()
                draw_results = process_drawing(
                    new_game_state['hand'],
                    new_game_state['held_indices'],
                    new_game_state['deck'],
                    game_state_manager,
                    sounds
                )
                new_game_state.update(draw_results)
            elif current_state_str == constants.STATE_MULTI_POKER_WAITING_FOR_HOLD: # Process Multi Poker draw
                 if sounds.get("button"): sounds["button"].play()
                 multi_draw_results = process_multi_drawing(
                     new_game_state['hand'],
                     new_game_state['held_indices'],
                     game_state_manager,
                     sounds
                 )
                 new_game_state.update(multi_draw_results)
            elif current_state_str == constants.STATE_DRAW_POKER_SHOWING_RESULT: # Start next Draw Poker hand
                if sounds.get("button"): sounds["button"].play()
                # Check if can play before starting next round
                if game_state_manager.can_afford_bet(1): # Cost for next draw poker game
                    round_state = start_draw_poker_round(game_state_manager, sounds)
                    new_game_state.update(round_state)
                else:
                    # Not enough money, transition to Game Over from here
                    reset_state = reset_game_variables()
                    new_game_state.update(reset_state)
                    new_game_state['message'] = "GAME OVER! Not enough money."
                    new_game_state['current_state'] = constants.STATE_GAME_OVER
            elif current_state_str == constants.STATE_MULTI_POKER_SHOWING_RESULT: # Start next Multi Poker hand
                 if sounds.get("button"): sounds["button"].play()
                 cost_next_multi = constants.NUM_MULTI_HANDS
                 if game_state_manager.can_afford_bet(cost_next_multi):
                     round_state = start_multi_poker_round(game_state_manager, sounds)
                     new_game_state.update(round_state)
                 else:
                     # Not enough money for multi-poker
                     reset_state = reset_game_variables()
                     new_game_state.update(reset_state)
                     new_game_state['message'] = f"GAME OVER! Need ${cost_next_multi} for Multi Poker."
                     new_game_state['current_state'] = constants.STATE_GAME_OVER
            elif current_state_str == constants.STATE_BLACKJACK_IDLE: # Start new Blackjack game
                if sounds.get("button"): sounds["button"].play()
                round_state = start_blackjack_round(game_state_manager, sounds)
                new_game_state.update(round_state)
            elif current_state_str == constants.STATE_BLACKJACK_SHOWING_RESULT: # Start next Blackjack hand
                if sounds.get("button"): sounds["button"].play()
                if game_state_manager.can_afford_bet(1): # Cost for next blackjack game
                    round_state = start_blackjack_round(game_state_manager, sounds)
                    new_game_state.update(round_state)
                else:
                    reset_state = reset_game_variables()
                    new_game_state.update(reset_state)
                    new_game_state['message'] = "GAME OVER! Not enough money for Blackjack."
                    new_game_state['current_state'] = constants.STATE_GAME_OVER

        elif action == constants.ACTION_HOLD_TOGGLE:
            if new_game_state['current_state'] in [constants.STATE_DRAW_POKER_WAITING_FOR_HOLD, constants.STATE_MULTI_POKER_WAITING_FOR_HOLD]:
                index = payload
                if index is not None and 0 <= index < 5: # Basic validation
                    held_indices = new_game_state['held_indices']
                    if index in held_indices:
                        held_indices.remove(index)
                        if sounds.get("hold"): sounds["hold"].play()
                    else:
                        held_indices.append(index)
                        held_indices.sort() # Keep sorted for consistency
                        if sounds.get("hold"): sounds["hold"].play()
                    new_game_state['held_indices'] = held_indices # Update state

        elif action == constants.ACTION_BLACKJACK_HIT or action == constants.ACTION_BLACKJACK_STAND:
             if new_game_state['current_state'] == constants.STATE_BLACKJACK_PLAYER_TURN:
                 # Let process_blackjack_action handle sound internally based on hit/stand
                 action_result_state = process_blackjack_action(action, new_game_state, game_state_manager, sounds)
                 new_game_state.update(action_result_state)

        elif action == constants.ACTION_PLAY_AGAIN:
             if new_game_state['current_state'] == constants.STATE_GAME_OVER:
                 if sounds.get("button"): sounds["button"].play()
                 # Reset money by re-initializing the manager
                 reset_state = reset_game_variables()
                 new_game_state.update(reset_state)
                 new_game_state['current_state'] = constants.STATE_TOP_MENU # Go back to top menu
                 # Signal that money needs reset? Or handle in main loop based on PLAY_AGAIN action.
                 new_game_state['needs_money_reset'] = True # Add a flag

        # --- Confirmation Actions ---
        elif action == constants.ACTION_CONFIRM_YES:
            if new_game_state['current_state'] == constants.STATE_CONFIRM_EXIT:
                if sounds.get("button"): sounds["button"].play()
                action_type = new_game_state.get('confirm_action_type')

                if action_type == 'QUIT':
                    # Actually quit the game now
                    running = False # Signal main loop to exit
                    # No need to change state, loop will terminate

                elif action_type == 'RESTART':
                    # Set flag for main loop to reset money and return to game selection
                    new_game_state['needs_money_reset'] = True
                    new_game_state['current_state'] = constants.STATE_GAME_SELECTION # Go back to game selection after reset
                    # Clear confirmation flags
                    new_game_state['confirm_action_type'] = None
                    new_game_state['previous_state_before_confirm'] = None

                else: # Default to 'EXIT' action (Exit to Game Menu)
                    # Proceed to the intended destination after confirming exit
                    destination_state = new_game_state.get('confirm_exit_destination', constants.STATE_GAME_SELECTION) # Default to Game Select
                    reset_state = reset_game_variables()
                    new_game_state.update(reset_state)
                    # Clear potential game-specific state
                    new_game_state['player_hand'] = []
                    new_game_state['dealer_hand'] = []
                    new_game_state['multi_hands'] = []
                    new_game_state['multi_results'] = []
                    new_game_state['roulette_bets'] = {} # Clear roulette bets too
                    new_game_state['message'] = "" # Clear any lingering game messages
                    new_game_state['current_state'] = destination_state
                    # Clear confirmation flags
                    new_game_state['confirm_action_type'] = None
                    new_game_state['confirm_exit_destination'] = None
                    new_game_state['previous_state_before_confirm'] = None


        elif action == constants.ACTION_CONFIRM_NO:
            if new_game_state['current_state'] == constants.STATE_CONFIRM_EXIT:
                if sounds.get("button"): sounds["button"].play()
                # Return to the state the player was in before the confirmation was triggered
                previous_state = new_game_state.get('previous_state_before_confirm')
                if previous_state:
                    new_game_state['current_state'] = previous_state
                else:
                    # Fallback if previous state wasn't stored correctly
                    new_game_state['current_state'] = constants.STATE_GAME_SELECTION
                # Clear confirmation flags
                new_game_state['confirm_action_type'] = None
                new_game_state['confirm_exit_destination'] = None
                new_game_state['previous_state_before_confirm'] = None

        # --- Roulette Actions ---
        elif action == constants.ACTION_ROULETTE_BET:
             # Allow placing bets in BETTING state, or in RESULT state (implicitly clears old bets/results)
             if new_game_state['current_state'] in [constants.STATE_ROULETTE_BETTING, constants.STATE_ROULETTE_RESULT]:
                 # If placing a bet after a result, reset the result state first
                 if new_game_state['current_state'] == constants.STATE_ROULETTE_RESULT:
                     new_game_state['roulette_bets'] = {}
                     new_game_state['roulette_winning_number'] = None
                     new_state['result_message'] = "" # Use new_state here
                     new_state['message'] = "Place your bets!"
                     new_state['current_state'] = constants.STATE_ROULETTE_BETTING # Change state back
                     game_state_manager.reset_round_bet() # Reset internal tracker for new round

                 bet_result_state = place_roulette_bet(payload, new_game_state, game_state_manager, sounds)
                 new_game_state.update(bet_result_state)

        elif action == constants.ACTION_ROULETTE_SPIN:
             if new_game_state['current_state'] == constants.STATE_ROULETTE_BETTING:
                 total_bet = new_game_state.get('roulette_total_bet', 0)
                 if total_bet <= 0:
                     new_game_state['message'] = "Place a bet before spinning!"
                     if sounds.get("lose"): sounds["lose"].play() # Error/negative sound
                 elif game_state_manager.can_afford_bet(total_bet):
                     if game_state_manager.deduct_bet(total_bet): # Deduct the total bet amount
                         if sounds.get("deal"): sounds["deal"].play() # Sound for spin start

                         # *** Determine winning number HERE, before animation starts ***
                         winning_number = random.choice(constants.ROULETTE_WHEEL_NUMBERS)
                         new_game_state['roulette_winning_number'] = winning_number

                         # Set state and timer for animation
                         new_game_state['current_state'] = constants.STATE_ROULETTE_SPINNING
                         new_game_state['roulette_spin_timer'] = constants.ROULETTE_SPIN_DURATION
                         new_game_state['message'] = "Spinning..."
                         new_game_state['result_message'] = "" # Clear previous result
                     else:
                         # Should not happen if can_afford_bet passed, but as a fallback
                         new_game_state['message'] = "Error deducting bet!"
                         if sounds.get("lose"): sounds["lose"].play()
                 else:
                     new_game_state['message'] = f"Not enough money! Need ${total_bet} to spin."
                     if sounds.get("lose"): sounds["lose"].play()

        elif action == constants.ACTION_ROULETTE_CLEAR_BETS: # Check constant name
             # Allow clearing in BETTING or RESULT state
             if new_game_state['current_state'] in [constants.STATE_ROULETTE_BETTING, constants.STATE_ROULETTE_RESULT]:
                 if new_game_state.get('roulette_bets'): # Only clear if bets exist
                     if sounds.get("button"): sounds["button"].play()
                     new_game_state['roulette_bets'] = {}
                     new_game_state['roulette_total_bet'] = 0
                     new_game_state['result_message'] = "" # Clear result message too
                     new_game_state['message'] = "Bets cleared. Place new bets."
                     game_state_manager.reset_round_bet() # Reset internal tracker
                     # If clearing from RESULT state, transition back to BETTING
                     if new_game_state['current_state'] == constants.STATE_ROULETTE_RESULT:
                          new_game_state['current_state'] = constants.STATE_ROULETTE_BETTING
                          new_game_state['roulette_winning_number'] = None # Clear winning number display

    # --- End of action processing loop ---

    # Update the running state in the dictionary before returning
    new_game_state['running'] = running

    return new_game_state

from typing import Dict, Any

import config_animations as animations
import config_states as states
from deck import Deck
from game_state import GameState
from blackjack_rules import is_blackjack, determine_winner, BLACKJACK_PAYOUT, LOSS_PAYOUT, PUSH_PAYOUT
from .reset_game_variables import reset_game_variables

def start_blackjack_round(game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Starts a new round of Blackjack. Deals cards and checks for initial Blackjacks.
    Returns a dictionary of the updated game state variables.
    """
    bet_amount = 1 # Fixed bet for now
    game_state_manager.set_cost_per_game(bet_amount)

    if game_state_manager.start_fixed_cost_game(): 
        updated_state = reset_game_variables() # Reset general variables
        deck = Deck() # Get a fresh shuffled deck

        # Deal initial hands
        player_hand = deck.deal(2)
        dealer_hand = deck.deal(2)

        updated_state['player_hand'] = player_hand
        updated_state['dealer_hand'] = dealer_hand
        updated_state['dealer_shows_one_card'] = True # Flag to hide dealer's first card
        updated_state['deck'] = deck # Store the deck

        if sounds.get("deal"):
            sounds["deal"].play()

        # Check for initial Blackjacks
        player_has_blackjack = is_blackjack(player_hand)
        dealer_has_blackjack = is_blackjack(dealer_hand)

        # Determine immediate outcome if Blackjack occurs
        if player_has_blackjack or dealer_has_blackjack:
            updated_state['dealer_shows_one_card'] = False # Reveal dealer card if game ends now
            result_message, payout_multiplier = determine_winner(player_hand, dealer_hand)

            winnings = int(payout_multiplier * bet_amount) # Calculate winnings/loss
            if winnings > 0:
                game_state_manager.add_winnings(winnings + bet_amount) # Add winnings + original bet back
                updated_state['result_message'] = f"{result_message} +${winnings + bet_amount}"
                if sounds.get("win"): sounds["win"].play()
                # Trigger animations
                updated_state['money_animation_active'] = True
                updated_state['money_animation_amount'] = winnings + bet_amount
                updated_state['money_animation_timer'] = animations.MONEY_ANIMATION_DURATION
                updated_state['result_message_flash_active'] = True
                updated_state['result_message_flash_timer'] = animations.RESULT_FLASH_DURATION
                updated_state['result_message_flash_visible'] = True
            elif payout_multiplier == PUSH_PAYOUT:
                game_state_manager.add_winnings(bet_amount) # Return original bet
                updated_state['result_message'] = f"{result_message} Bet Returned"
                # No win/lose sound for push
            else: # Loss
                updated_state['result_message'] = f"{result_message} -${bet_amount}"
                if sounds.get("lose"): sounds["lose"].play()
                # Ensure animations are off
                updated_state['money_animation_active'] = False
                updated_state['result_message_flash_active'] = False


            updated_state['message'] = "Click DEAL for next hand"
            updated_state['current_state'] = states.STATE_BLACKJACK_SHOWING_RESULT

        else:
            # No immediate Blackjack resolution, proceed to player's turn
            updated_state['message'] = "Your Turn: Hit or Stand?"
            updated_state['current_state'] = states.STATE_BLACKJACK_PLAYER_TURN

        return updated_state
    else:
        # Game Over state
        updated_state = reset_game_variables()
        updated_state['message'] = "GAME OVER! Not enough money for Blackjack."
        updated_state['result_message'] = ""
        updated_state['current_state'] = states.STATE_GAME_OVER
        updated_state['deck'] = Deck() # Still provide a deck object
        # Ensure Blackjack specific state is cleared
        updated_state['player_hand'] = []
        updated_state['dealer_hand'] = []
        updated_state['dealer_shows_one_card'] = False
        return updated_state

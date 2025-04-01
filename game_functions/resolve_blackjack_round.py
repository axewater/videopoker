from typing import Dict, Any

import config_animations as animations
import config_states as states
from deck import Deck
from game_state import GameState
from blackjack_rules import get_hand_value, is_busted, should_dealer_hit, determine_winner, WIN_PAYOUT, LOSS_PAYOUT, PUSH_PAYOUT, BLACKJACK_PAYOUT

def resolve_blackjack_round(current_game_state: Dict[str, Any], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles the dealer's turn, determines the winner, calculates payout,
    and updates the game state for Blackjack.
    Assumes player's turn is finished (stood or busted).
    Returns a dictionary of the updated game state variables.
    """
    new_state = current_game_state.copy()
    player_hand = new_state.get('player_hand', [])
    dealer_hand = new_state.get('dealer_hand', [])
    deck = new_state.get('deck')
    bet_amount = game_state_manager.get_cost_per_game() # Get the bet amount for this round

    new_state['dealer_shows_one_card'] = False # Reveal dealer's hidden card

    player_value = get_hand_value(player_hand)

    # If player already busted, dealer doesn't need to play. Player loses.
    if player_value > 21:
        result_message = "Player Busts!"
        payout_multiplier = LOSS_PAYOUT
    else:
        # Dealer plays according to rules (hit until 17+)
        while should_dealer_hit(dealer_hand):
            if deck and len(deck) > 0:
                dealer_hand.extend(deck.deal(1))
                new_state['dealer_hand'] = dealer_hand
                if sounds.get("draw"): sounds["draw"].play() # Sound for dealer hit
            else:
                new_state['message'] = "Deck empty during dealer turn!"
                # Handle error - maybe push? For now, let current result stand.
                break # Exit loop if deck is empty

        # Now determine the winner based on final hands
        result_message, payout_multiplier = determine_winner(player_hand, dealer_hand)

    # Calculate winnings/loss based on payout multiplier
    winnings = int(payout_multiplier * bet_amount)

    # Update money and set messages/sounds
    if winnings > 0:
        # For Blackjack (1.5x), winnings = 1.5 * bet. Total return = 1.5*bet + bet = 2.5*bet? No, payout includes bet.
        # Payout 1.5 means win 1.5x bet. Total return = 1.5 * bet. Add this amount.
        # Payout 1.0 means win 1.0x bet. Total return = 1.0 * bet. Add this amount.
        # Let's adjust: add_winnings should add NET winnings.
        net_winnings = winnings
        game_state_manager.add_winnings(net_winnings + bet_amount) # Add net winnings + original bet back
        new_state['result_message'] = f"{result_message} +${net_winnings + bet_amount}"
        if sounds.get("win"): sounds["win"].play()
        # Trigger animations
        new_state['money_animation_active'] = True
        new_state['money_animation_amount'] = net_winnings + bet_amount
        new_state['money_animation_timer'] = animations.MONEY_ANIMATION_DURATION
        new_state['result_message_flash_active'] = True
        new_state['result_message_flash_timer'] = animations.RESULT_FLASH_DURATION
        new_state['result_message_flash_visible'] = True
    elif payout_multiplier == PUSH_PAYOUT:
        game_state_manager.add_winnings(bet_amount) # Return original bet
        new_state['result_message'] = f"{result_message} Bet Returned"
        # No win/lose sound for push
        new_state['money_animation_active'] = False
        new_state['result_message_flash_active'] = False
    else: # Loss
        # Bet was already deducted, so no change to money needed.
        new_state['result_message'] = f"{result_message} -${bet_amount}"
        if sounds.get("lose"): sounds["lose"].play()
        new_state['money_animation_active'] = False
        new_state['result_message_flash_active'] = False


    new_state['message'] = "Click DEAL for next hand"
    new_state['current_state'] = states.STATE_BLACKJACK_SHOWING_RESULT

    return new_state

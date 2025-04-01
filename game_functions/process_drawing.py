from typing import List, Optional, Dict, Any

import config_states as states
import config_animations as anim
from card import Card
from deck import Deck
from game_state import GameState
from poker_rules import evaluate_hand

def process_drawing(hand: List[Card], held_indices: List[int], deck: Deck, game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles the logic for drawing new cards in standard Draw Poker.
    Returns a dictionary of the updated game state variables.
    """
    updated_state = {} # Dictionary to hold changes

    cards_to_draw = 5 - len(held_indices)
    new_hand_list: List[Optional[Card]] = [None] * 5 # Placeholder

    # Keep held cards
    for i in held_indices:
        if i < len(hand): # Basic bounds check
            new_hand_list[i] = hand[i]

    # Get new cards for non-held positions
    try:
        # Ensure deck has enough cards BEFORE dealing
        if len(deck) < cards_to_draw:
             raise IndexError(f"Not enough cards left in deck ({len(deck)}) to draw {cards_to_draw}.")
        new_cards = deck.deal(cards_to_draw)
    except IndexError as e:
         print(f"Error: {e}")
         updated_state['message'] = "Deck error! Please restart."
         updated_state['current_state'] = states.STATE_GAME_OVER
         updated_state['hand'] = hand # Return original hand on error
         return updated_state

    # Place new cards into the empty slots
    new_card_idx = 0
    for i in range(5):
        if new_hand_list[i] is None: # If this position needs a new card
            if new_card_idx < len(new_cards):
                new_hand_list[i] = new_cards[new_card_idx]
                new_card_idx += 1
            else:
                print(f"Error: Mismatch drawing cards. Needed card for index {i}, but ran out of new cards.")
                updated_state['message'] = "Card drawing error!"
                updated_state['current_state'] = states.STATE_GAME_OVER
                updated_state['hand'] = hand # Return original hand
                return updated_state

    # Final hand is now complete
    final_hand: List[Card] = [card for card in new_hand_list if card is not None]
    updated_state['hand'] = final_hand

    # Evaluate the final hand
    rank, hand_name, payout = evaluate_hand(final_hand)
    updated_state['final_hand_rank'] = rank # Store the actual rank

    if payout > 0:
        winnings = payout * 1 # Payout is based on a 1-unit bet
        updated_state['result_message'] = f"WINNER! {hand_name}! +${winnings}"
        if sounds.get("win"):
            sounds["win"].play() # Play win sound
        game_state_manager.add_winnings(winnings) # Update money directly
        # Trigger money animation
        updated_state['money_animation_active'] = True
        updated_state['money_animation_amount'] = winnings
        updated_state['money_animation_timer'] = anim.MONEY_ANIMATION_DURATION
        # Trigger result message flashing
        updated_state['result_message_flash_active'] = True
        updated_state['result_message_flash_timer'] = anim.RESULT_FLASH_DURATION # Use a constant
        updated_state['result_message_flash_visible'] = True
    else:
        updated_state['result_message'] = f"Result: {hand_name}. No win."
        if sounds.get("lose"):
            sounds["lose"].play() # Play lose sound
        # Ensure animation state is off if no win
        updated_state['money_animation_active'] = False
        updated_state['money_animation_amount'] = 0
        updated_state['money_animation_timer'] = 0
        # Ensure flashing is off if no win
        updated_state['result_message_flash_active'] = False
        updated_state['result_message_flash_timer'] = 0
        updated_state['result_message_flash_visible'] = True


    if sounds.get("draw"):
        sounds["draw"].play() # Play draw sound (after cards are replaced)
    updated_state['message'] = "" # Clear the action message
    updated_state['current_state'] = states.STATE_DRAW_POKER_SHOWING_RESULT
    updated_state['deck'] = deck # Pass back the potentially modified deck

    return updated_state

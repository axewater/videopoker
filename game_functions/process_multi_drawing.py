from typing import List, Dict, Any, Optional

import constants
from card import Card
from deck import Deck
from game_state import GameState
from poker_rules import evaluate_hand

def process_multi_drawing(base_hand: List[Card], held_indices: List[int], game_state_manager: GameState, sounds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles drawing cards for multiple hands in Multi Poker.
    Returns a dictionary of the updated game state variables.
    """
    updated_state = {} # Dictionary to hold changes
    num_hands = constants.NUM_MULTI_HANDS
    multi_hands_list = []
    multi_results_list = []
    total_winnings = 0

    # Create separate decks for each hand draw.
    # Each new deck should be a standard 52-card deck.
    draw_decks = [Deck() for _ in range(num_hands)]

    held_cards = {i: base_hand[i] for i in held_indices if i < len(base_hand)}

    for i in range(num_hands):
        current_hand_list: List[Optional[Card]] = [None] * 5
        # Place held cards
        for index, card in held_cards.items():
            current_hand_list[index] = card

        # Determine cards needed
        cards_to_draw = 5 - len(held_cards)

        # Deal new cards from the corresponding draw deck
        try:
            new_cards = []
            deck_for_draw = draw_decks[i]
            attempts = 0
            # Make sure deck has enough cards potentially
            if len(deck_for_draw) < cards_to_draw:
                 raise IndexError(f"Initial deck size too small for hand {i+1}")

            while len(new_cards) < cards_to_draw and attempts < 100:
                if len(deck_for_draw) == 0: # Check if deck ran out during loop
                    raise IndexError(f"Deck ran out of cards while drawing for hand {i+1}")

                potential_card = deck_for_draw.deal(1)[0]
                # Check if this card (rank and suit) is already held
                is_held = any(potential_card == held_card for held_card in held_cards.values())
                if not is_held:
                     # Also check if it's already been drawn for *this specific hand*
                     is_drawn_for_this_hand = any(potential_card == drawn_card for drawn_card in new_cards)
                     if not is_drawn_for_this_hand:
                         new_cards.append(potential_card)
                attempts += 1 # Prevent infinite loops in edge cases

            if len(new_cards) < cards_to_draw:
                 # This might happen if the held cards + needed cards > 52 unique cards,
                 # though extremely unlikely with standard decks per hand.
                 # More likely indicates a logic flaw or deck issue.
                 print(f"Warning: Could not deal enough unique cards for hand {i+1} after {attempts} attempts. Needed {cards_to_draw}, got {len(new_cards)}")
                 # Handle gracefully - maybe skip this hand or assign a default loss?
                 # For now, let's signal an error state.
                 raise IndexError(f"Failed to gather sufficient unique cards for hand {i+1}")


        except IndexError as e:
            print(f"Error dealing for multi-hand {i+1}: {e}")
            updated_state['message'] = "Deck error during multi-draw!"
            updated_state['current_state'] = constants.STATE_GAME_OVER # Or error state
            # Return partial results if needed, or just error out
            updated_state['multi_hands'] = multi_hands_list
            updated_state['multi_results'] = multi_results_list
            updated_state['total_winnings'] = total_winnings
            return updated_state

        # Place new cards
        new_card_idx = 0
        for j in range(5):
            if current_hand_list[j] is None:
                if new_card_idx < len(new_cards):
                    current_hand_list[j] = new_cards[new_card_idx]
                    new_card_idx += 1
                else:
                    # Logic error if this happens
                    print(f"Error: Mismatch placing drawn cards in multi-hand {i+1}.")
                    updated_state['message'] = "Multi-hand card placement error!"
                    updated_state['current_state'] = constants.STATE_GAME_OVER
                    return updated_state


        final_hand: List[Card] = [card for card in current_hand_list if card is not None]
        if len(final_hand) != 5:
             print(f"Error: Multi-hand {i+1} reconstruction failed (size {len(final_hand)}).")
             updated_state['message'] = "Multi-hand reconstruction error!"
             updated_state['current_state'] = constants.STATE_GAME_OVER
             return updated_state

        # Evaluate this hand
        rank, name, payout = evaluate_hand(final_hand)
        multi_hands_list.append(final_hand)
        multi_results_list.append((rank, name, payout))
        total_winnings += payout # Payout is per unit bet (1)

    # Update game state after processing all hands
    updated_state['multi_hands'] = multi_hands_list
    updated_state['multi_results'] = multi_results_list
    updated_state['total_winnings'] = total_winnings

    if total_winnings > 0:
        updated_state['result_message'] = f"WINNER! Total: +${total_winnings}"
        if sounds.get("win"):
            sounds["win"].play()
        game_state_manager.add_winnings(total_winnings) # Update money directly
        # Trigger money animation for total amount
        updated_state['money_animation_active'] = True
        updated_state['money_animation_amount'] = total_winnings
        updated_state['money_animation_timer'] = constants.MONEY_ANIMATION_DURATION
        # Trigger result message flashing
        updated_state['result_message_flash_active'] = True
        updated_state['result_message_flash_timer'] = constants.RESULT_FLASH_DURATION # Use a constant
        updated_state['result_message_flash_visible'] = True
    else:
        updated_state['result_message'] = "No winning hands."
        if sounds.get("lose"):
            sounds["lose"].play()
        # Ensure animation state is off if no win
        updated_state['money_animation_active'] = False
        updated_state['money_animation_amount'] = 0
        updated_state['money_animation_timer'] = 0
        # Ensure flashing is off if no win
        updated_state['result_message_flash_active'] = False
        updated_state['result_message_flash_timer'] = 0
        updated_state['result_message_flash_visible'] = True


    if sounds.get("draw"):
        sounds["draw"].play() # Play draw sound once after all hands are set
    updated_state['message'] = "" # Clear action message
    updated_state['current_state'] = constants.STATE_MULTI_POKER_SHOWING_RESULT
    # Base hand remains the same, it's just used for holds
    updated_state['hand'] = base_hand
    # Held indices might be cleared or kept depending on game flow, let's clear them
    updated_state['held_indices'] = [] # Clear holds after multi-draw

    return updated_state

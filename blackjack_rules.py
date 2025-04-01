import collections
from typing import List, Tuple

from card import Card

# Using namedtuple for lightweight, immutable card objects if not already imported elsewhere
# Card = collections.namedtuple("Card", ["rank", "suit"]) # Assuming Card is imported

# Blackjack card values
BLACKJACK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "T": 10, "J": 10, "Q": 10, "K": 10, "A": 11 # Ace initially counts as 11
}

# Payout constants
BLACKJACK_PAYOUT = 1.5 # 3:2 payout for Blackjack
WIN_PAYOUT = 1.0      # 1:1 payout for regular win
PUSH_PAYOUT = 0.0     # 0 payout for a push
LOSS_PAYOUT = -1.0    # Player loses their bet

def get_hand_value(hand: List[Card]) -> int:
    """Calculates the value of a Blackjack hand, handling Aces optimally."""
    value = 0
    num_aces = 0
    for card in hand:
        value += BLACKJACK_VALUES[card.rank]
        if card.rank == "A":
            num_aces += 1

    # Adjust for Aces if value is over 21
    while value > 21 and num_aces > 0:
        value -= 10 # Change an Ace from 11 to 1
        num_aces -= 1

    return value

def is_blackjack(hand: List[Card]) -> bool:
    """Checks if a hand is a Blackjack (2 cards totaling 21)."""
    return len(hand) == 2 and get_hand_value(hand) == 21

def is_busted(hand: List[Card]) -> bool:
    """Checks if a hand's value is over 21."""
    return get_hand_value(hand) > 21

def should_dealer_hit(dealer_hand: List[Card]) -> bool:
    """Determines if the dealer should hit based on standard rules (stand on 17+)."""
    # Simple rule: Stand on 17 or higher (including soft 17 for now)
    # More complex rules (like hit soft 17) could be added here.
    return get_hand_value(dealer_hand) < 17

def determine_winner(player_hand: List[Card], dealer_hand: List[Card]) -> Tuple[str, float]:
    """
    Determines the winner of a Blackjack round and the payout multiplier.

    Args:
        player_hand: List of player's Card objects.
        dealer_hand: List of dealer's Card objects.

    Returns:
        A tuple containing:
        - Result message ("Player Blackjack!", "Player Wins!", "Dealer Wins!", "Push!", "Player Busts!", "Dealer Busts!").
        - Payout multiplier (e.g., 1.5, 1.0, 0.0, -1.0).
    """
    player_value = get_hand_value(player_hand)
    dealer_value = get_hand_value(dealer_hand)
    player_has_blackjack = is_blackjack(player_hand)
    dealer_has_blackjack = is_blackjack(dealer_hand)

    # Check for player bust first
    if player_value > 21:
        return "Player Busts!", LOSS_PAYOUT

    # Check for dealer bust
    if dealer_value > 21:
        return "Dealer Busts! Player Wins!", WIN_PAYOUT

    # Check for Blackjacks (only if player didn't bust)
    if player_has_blackjack and dealer_has_blackjack:
        return "Push! (Both Blackjack)", PUSH_PAYOUT
    if player_has_blackjack:
        return "Player Blackjack!", BLACKJACK_PAYOUT
    if dealer_has_blackjack:
        return "Dealer Blackjack! Dealer Wins.", LOSS_PAYOUT

    # Compare non-busted, non-blackjack hands
    if player_value > dealer_value:
        return "Player Wins!", WIN_PAYOUT
    elif dealer_value > player_value:
        return "Dealer Wins.", LOSS_PAYOUT
    else: # player_value == dealer_value
        return "Push!", PUSH_PAYOUT

if __name__ == '__main__':
    # Example Usage
    hand1 = [Card("A", "S"), Card("K", "D")] # Blackjack
    hand2 = [Card("Q", "H"), Card("7", "C")] # 17
    hand3 = [Card("A", "C"), Card("5", "H"), Card("A", "D")] # 17 (soft)
    hand4 = [Card("T", "S"), Card("T", "C"), Card("2", "H")] # 22 (Bust)
    hand5 = [Card("6", "S"), Card("A", "H")] # 17 (soft)
    hand6 = [Card("A", "S"), Card("A", "D"), Card("A", "C"), Card("7", "H")] # 20

    print(f"Hand: {hand1}, Value: {get_hand_value(hand1)}, Blackjack: {is_blackjack(hand1)}")
    print(f"Hand: {hand2}, Value: {get_hand_value(hand2)}, Blackjack: {is_blackjack(hand2)}")
    print(f"Hand: {hand3}, Value: {get_hand_value(hand3)}, Blackjack: {is_blackjack(hand3)}")
    print(f"Hand: {hand4}, Value: {get_hand_value(hand4)}, Busted: {is_busted(hand4)}")
    print(f"Hand: {hand5}, Value: {get_hand_value(hand5)}, Dealer Hit? {should_dealer_hit(hand5)}")
    print(f"Hand: {hand6}, Value: {get_hand_value(hand6)}, Dealer Hit? {should_dealer_hit(hand6)}")

    # Test determine_winner
    p_bj = [Card("A", "S"), Card("K", "D")]
    d_bj = [Card("A", "C"), Card("Q", "H")]
    p_20 = [Card("T", "S"), Card("T", "D")]
    d_19 = [Card("T", "C"), Card("9", "H")]
    p_18 = [Card("K", "S"), Card("8", "D")]
    d_18 = [Card("Q", "C"), Card("8", "H")]
    p_bust = [Card("T", "S"), Card("T", "D"), Card("3", "C")]
    d_bust = [Card("T", "C"), Card("T", "H"), Card("5", "S")]

    print("\nWinner Tests:")
    print(f"Player BJ vs Dealer BJ: {determine_winner(p_bj, d_bj)}")
    print(f"Player BJ vs Dealer 19: {determine_winner(p_bj, d_19)}")
    print(f"Player 20 vs Dealer BJ: {determine_winner(p_20, d_bj)}")
    print(f"Player 20 vs Dealer 19: {determine_winner(p_20, d_19)}")
    print(f"Player 18 vs Dealer 19: {determine_winner(p_18, d_19)}")
    print(f"Player 18 vs Dealer 18: {determine_winner(p_18, d_18)}")
    print(f"Player Bust vs Dealer 18: {determine_winner(p_bust, d_18)}")
    print(f"Player 20 vs Dealer Bust: {determine_winner(p_20, d_bust)}")

from collections import Counter
from typing import List, Tuple, Optional, NewType
from card import Card, RANK_VALUES
from enum import Enum, auto # Using Enum for better type safety and clarity

# Define Hand Ranks using Enum
class HandRank(Enum):
    ROYAL_FLUSH = auto()
    STRAIGHT_FLUSH = auto()
    FOUR_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FLUSH = auto()
    STRAIGHT = auto()
    THREE_OF_A_KIND = auto()
    TWO_PAIR = auto()
    JACKS_OR_BETTER = auto()
    NOTHING = auto() # Represents hands below Jacks or Better


# Standard Jacks or Better Pay Table (Bet = 1 unit)
# Maps Hand Rank constant to (Name, Payout Multiplier)
PAY_TABLE = {
    HandRank.ROYAL_FLUSH: ("Royal Flush", 250), # Often higher with max bet, but simplifying
    HandRank.STRAIGHT_FLUSH: ("Straight Flush", 50),
    HandRank.FOUR_OF_A_KIND: ("Four of a Kind", 25),
    HandRank.FULL_HOUSE: ("Full House", 9),
    HandRank.FLUSH: ("Flush", 6),
    HandRank.STRAIGHT: ("Straight", 4),
    HandRank.THREE_OF_A_KIND: ("Three of a Kind", 3),
    HandRank.TWO_PAIR: ("Two Pair", 2),
    HandRank.JACKS_OR_BETTER: ("Jacks or Better", 1),
    HandRank.NOTHING: ("Nothing", 0)
}

def get_pay_table_string() -> str:
    """Returns a formatted string representation of the pay table."""
    lines = ["--- Pay Table (Bet: 1) ---"]
    
    # Sort by payout for display (descending)
    sorted_ranks = sorted([rank for rank in PAY_TABLE if PAY_TABLE[rank][1] > 0], key=lambda k: PAY_TABLE[k][1], reverse=True)
    
    # Find the maximum length of the hand names for alignment
    max_name_width = 0
    if sorted_ranks:
        max_name_width = max(len(PAY_TABLE[rank][0]) for rank in sorted_ranks)

    for rank in sorted_ranks:
        name, payout = PAY_TABLE[rank]
        lines.append(f"{name:<{max_name_width}} : {payout:>3}x") # Left-align name, right-align payout
    return "\n".join(lines)


def evaluate_hand(hand: List[Card]) -> Tuple[HandRank, str, int]:
    """
    Evaluates a 5-card hand and returns its rank, name, and payout multiplier.

    Args:
        hand: A list of 5 Card objects.

    Returns:
        A tuple containing:
        - The rank of the hand (HandRank enum member).
        - The name of the hand (e.g., "Royal Flush", "Four of a Kind").
        - The payout multiplier for that hand based on PAY_TABLE.
    """
    if len(hand) != 5:
        raise ValueError("Hand must contain exactly 5 cards.")

    ranks = sorted([RANK_VALUES[card.rank] for card in hand], reverse=True)
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    most_common_ranks = rank_counts.most_common() # List of (rank_value, count) tuples

    is_flush = len(set(suits)) == 1
    # Check for straight: difference between max and min rank is 4, and no duplicates
    # Special case: A-2-3-4-5 straight (ranks are 14, 2, 3, 4, 5 -> sorted 14, 5, 4, 3, 2)
    is_straight = (len(set(ranks)) == 5 and (ranks[0] - ranks[4] == 4)) or \
                  (set(ranks) == {RANK_VALUES['A'], RANK_VALUES['2'], RANK_VALUES['3'], RANK_VALUES['4'], RANK_VALUES['5']})

    # Handle Ace-low straight rank sorting if necessary for evaluation
    if set(ranks) == {RANK_VALUES['A'], RANK_VALUES['2'], RANK_VALUES['3'], RANK_VALUES['4'], RANK_VALUES['5']}:
         # Treat Ace as low for straight calculation (value 1)
         ranks = sorted([1 if r == RANK_VALUES['A'] else r for r in ranks], reverse=True)
         is_straight = True # Re-confirm as straight might have been missed above if Ace was high

    # --- Evaluate hands from highest rank to lowest ---

    # Royal Flush / Straight Flush
    if is_straight and is_flush:
        if ranks[0] == RANK_VALUES['A'] and ranks[1] == RANK_VALUES['K']: # Ace-high straight flush
            rank = HandRank.ROYAL_FLUSH
        else:
            rank = HandRank.STRAIGHT_FLUSH
        name, payout = PAY_TABLE[rank]
        return rank, name, payout

    # Four of a Kind
    if most_common_ranks[0][1] == 4:
        rank = HandRank.FOUR_OF_A_KIND
        name, payout = PAY_TABLE[rank]
        return rank, name, payout

    # Full House
    if most_common_ranks[0][1] == 3 and most_common_ranks[1][1] == 2:
        rank = HandRank.FULL_HOUSE
        name, payout = PAY_TABLE[rank]
        return rank, name, payout

    # Flush (but not Straight Flush)
    if is_flush:
        rank = HandRank.FLUSH
        name, payout = PAY_TABLE[rank]
        return rank, name, payout

    # Straight (but not Straight Flush)
    if is_straight:
        rank = HandRank.STRAIGHT
        name, payout = PAY_TABLE[rank]
        return rank, name, payout

    # Three of a Kind
    if most_common_ranks[0][1] == 3:
        rank = HandRank.THREE_OF_A_KIND
        name, payout = PAY_TABLE[rank]
        return rank, name, payout

    # Two Pair
    if most_common_ranks[0][1] == 2 and most_common_ranks[1][1] == 2:
        rank = HandRank.TWO_PAIR
        name, payout = PAY_TABLE[rank]
        return rank, name, payout

    # Jacks or Better (One Pair)
    if most_common_ranks[0][1] == 2:
        pair_rank_value = most_common_ranks[0][0]
        # Check if the pair rank is Jack (11) or higher
        if pair_rank_value >= RANK_VALUES['J']:
            rank = HandRank.JACKS_OR_BETTER
            name, payout = PAY_TABLE[rank]
            return rank, name, payout

    # Nothing
    rank = HandRank.NOTHING
    name, payout = PAY_TABLE[rank]
    return rank, name, payout


if __name__ == '__main__':
    # Example Hand Evaluations
    from card import Card

    print(get_pay_table_string())
    print("-" * 30)

    # Test hands
    royal = [Card('T','♠'), Card('J','♠'), Card('Q','♠'), Card('K','♠'), Card('A','♠')]
    straight_flush = [Card('8','♦'), Card('9','♦'), Card('T','♦'), Card('J','♦'), Card('Q','♦')]
    four_kind = [Card('7','♣'), Card('7','♦'), Card('7','♥'), Card('7','♠'), Card('K','♠')]
    full_house = [Card('3','♣'), Card('3','♦'), Card('3','♥'), Card('9','♠'), Card('9','♣')]
    flush = [Card('2','♥'), Card('5','♥'), Card('8','♥'), Card('T','♥'), Card('K','♥')]
    straight = [Card('5','♣'), Card('6','♦'), Card('7','♥'), Card('8','♠'), Card('9','♣')]
    ace_low_straight = [Card('A','♣'), Card('2','♦'), Card('3','♥'), Card('4','♠'), Card('5','♣')]
    three_kind = [Card('Q','♣'), Card('Q','♦'), Card('Q','♥'), Card('2','♠'), Card('8','♣')]
    two_pair = [Card('J','♣'), Card('J','♦'), Card('4','♥'), Card('4','♠'), Card('A','♣')]
    jacks_or_better = [Card('K','♣'), Card('K','♦'), Card('2','♥'), Card('5','♠'), Card('T','♣')]
    low_pair = [Card('6','♣'), Card('6','♦'), Card('A','♥'), Card('Q','♠'), Card('3','♣')]
    nothing = [Card('2','♣'), Card('5','♦'), Card('9','♥'), Card('J','♠'), Card('K','♣')]

    hands_to_test = {
        "Royal Flush": royal,
        "Straight Flush": straight_flush,
        "Four of a Kind": four_kind,
        "Full House": full_house,
        "Flush": flush,
        "Straight": straight,
        "Ace-Low Straight": ace_low_straight,
        "Three of a Kind": three_kind,
        "Two Pair": two_pair,
        "Jacks or Better": jacks_or_better,
        "Low Pair (Nothing)": low_pair,
        "Nothing": nothing
    }

    for name, hand in hands_to_test.items():
        hand_str = ", ".join([f"{c.rank}{c.suit}" for c in hand])
        rank, hand_name, payout = evaluate_hand(hand)
        print(f"Hand: {hand_str:<30} -> {name:<18} | Result: {hand_name} ({payout}x)")

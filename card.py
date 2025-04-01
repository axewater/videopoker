import collections

# Using namedtuple for lightweight, immutable card objects
Card = collections.namedtuple("Card", ["rank", "suit"])

SUITS = ["♣", "♦", "♥", "♠"] # Clubs, Diamonds, Hearts, Spades
# Using strings for ranks for easier display. Special ranks first for sorting.
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

# Map ranks to values for easier comparison/evaluation later
RANK_VALUES = {rank: i for i, rank in enumerate(RANKS, 2)} # 2=2, ..., T=10, J=11, Q=12, K=13, A=14

def card_to_string(card: Card) -> str:
    """Returns a string representation of a card (e.g., 'K♠', 'T♥')."""
    return f"{card.rank}{card.suit}"

if __name__ == '__main__':
    # Example usage and demonstration
    c1 = Card("A", "♠")
    c2 = Card("T", "♥")
    print(f"Created card: {c1}")
    print(f"String representation: {card_to_string(c1)}")
    print(f"Rank value of {c1.rank}: {RANK_VALUES[c1.rank]}")
    print(f"Rank value of {c2.rank}: {RANK_VALUES[c2.rank]}")
    print(f"Available suits: {SUITS}")
    print(f"Available ranks: {RANKS}")

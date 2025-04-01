import random
from typing import List
from card import Card, SUITS, RANKS # Assuming card.py is in the same directory

class Deck:
    """Represents a standard 52-card deck."""

    def __init__(self):
        """Initializes a new deck of 52 cards."""
        self._cards: List[Card] = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck in place."""
        random.shuffle(self._cards)
        print("Deck shuffled.") # Optional: for debugging/visibility

    def deal(self, num_cards: int = 1) -> List[Card]:
        """
        Deals a specified number of cards from the top of the deck.
        Removes the dealt cards from the deck.
        Raises an IndexError if not enough cards are left.
        """
        if num_cards > len(self._cards):
            raise IndexError("Not enough cards left in the deck to deal.")
        
        dealt_cards = self._cards[:num_cards]
        self._cards = self._cards[num_cards:]
        return dealt_cards

    def __len__(self) -> int:
        """Returns the number of cards remaining in the deck."""
        return len(self._cards)

    def is_empty(self) -> bool:
        """Checks if the deck is empty."""
        return len(self._cards) == 0

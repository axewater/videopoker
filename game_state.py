class GameState:
    """Manages the player's money and current game status."""

    def __init__(self, starting_money: int = 10):
        """Initializes the game state with starting money."""
        if starting_money < 1:
            raise ValueError("Starting money must be at least 1.")
        self._money = starting_money
        self.cost_per_game = 1

    @property
    def money(self) -> int:
        """Returns the current amount of money the player has."""
        return self._money

    def can_play(self) -> bool:
        """Checks if the player has enough money to play a game."""
        return self._money >= self.cost_per_game

    def start_game(self) -> bool:
        """Deducts the cost of a game if the player can afford it."""
        if self.can_play():
            self._money -= self.cost_per_game
            return True
        return False

    def add_winnings(self, amount: int):
        """Adds winnings to the player's money."""
        if amount < 0:
            raise ValueError("Winnings amount cannot be negative.")
        self._money += amount

if __name__ == '__main__':
    # Example usage
    state = GameState(starting_money=5)
    print(f"Initial money: ${state.money}")
    print(f"Can play? {state.can_play()}")

    if state.start_game():
        print(f"Started game. Money left: ${state.money}")
    else:
        print("Cannot start game.")

    state.add_winnings(3)
    print(f"Won $3. Current money: ${state.money}")

    # Play until broke
    while state.start_game():
        print(f"Played a game. Money left: ${state.money}")

    print(f"Final money: ${state.money}")
    print(f"Can play? {state.can_play()}")

    # Test invalid starting money
    try:
        GameState(0)
    except ValueError as e:
        print(f"Caught expected error: {e}")

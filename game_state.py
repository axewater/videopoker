class GameState:
    """Manages the player's money and current game status."""

    def __init__(self, starting_money: int = 10):
        """Initializes the game state with starting money."""
        if starting_money < 1:
            raise ValueError("Starting money must be at least 1.")
        self._money = starting_money
        self._cost_per_game = 1 # Default cost

    @property
    def money(self) -> int:
        """Returns the current amount of money the player has."""
        return self._money

    def can_play(self) -> bool:
        """Checks if the player has enough money for the current cost per game."""
        return self._money >= self._cost_per_game

    def set_cost_per_game(self, cost: int):
        """Sets the cost for the next game."""
        if cost < 1:
            raise ValueError("Cost per game must be at least 1.")
        self._cost_per_game = cost

    def get_cost_per_game(self) -> int:
        """Returns the current cost per game."""
        return self._cost_per_game

    def start_game(self) -> bool:
        """Deducts the cost of a game if the player can afford it."""
        if self.can_play():
            self._money -= self._cost_per_game
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
    print(f"Cost per game: ${state.get_cost_per_game()}")
    print(f"Can play? {state.can_play()}")

    if state.start_game():
        print(f"Started game. Money left: ${state.money}")
    else:
        print("Cannot start game.")

    state.add_winnings(3)
    print(f"Won $3. Current money: ${state.money}")

    # Test changing cost
    state.set_cost_per_game(3)
    print(f"New cost per game: ${state.get_cost_per_game()}")

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

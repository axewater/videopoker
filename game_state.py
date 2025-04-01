class GameState:
    """Manages the player's money and current game status."""

    def __init__(self, starting_money: int = 10):
        """Initializes the game state with starting money."""
        if starting_money < 1:
            raise ValueError("Starting money must be at least 1.")
        self._money = starting_money
        self._cost_per_game = 1 # Default cost
        self._current_total_bet = 0 # Track total bet for current round (e.g., Roulette)

    @property
    def money(self) -> int:
        """Returns the current amount of money the player has."""
        return self._money

    def can_play(self) -> bool:
        """Checks if the player has enough money for the default cost per game."""
        return self._money >= self.get_cost_per_game()

    def set_cost_per_game(self, cost: int):
        """Sets the cost for the next game."""
        if cost < 1:
            raise ValueError("Cost per game must be at least 1.")
        self._cost_per_game = cost

    def get_cost_per_game(self) -> int:
        """Returns the current cost per game."""
        return self._cost_per_game

    def start_fixed_cost_game(self) -> bool:
        """Deducts the cost of a game if the player can afford it."""
        if self._money >= self._cost_per_game:
            self._money -= self._cost_per_game
            return True
        return False

    def can_afford_bet(self, amount: int) -> bool:
        """Checks if the player has enough money to place a specific bet."""
        if amount < 0:
             raise ValueError("Bet amount cannot be negative.")
        return self._money >= amount

    def deduct_bet(self, amount: int) -> bool:
        """Deducts a specific bet amount if the player can afford it."""
        if self.can_afford_bet(amount):
            self._money -= amount
            self._current_total_bet += amount # Track total bet for the round
            return True
        return False

    def add_winnings(self, amount: int):
        """Adds winnings to the player's money."""
        if amount < 0:
            raise ValueError("Winnings amount cannot be negative.")
        self._money += amount

    def reset_round_bet(self):
        """Resets the tracked total bet for the round."""
        self._current_total_bet = 0

if __name__ == '__main__':
    # Example usage
    state = GameState(starting_money=5)
    print(f"Initial money: ${state.money}")
    print(f"Cost per game: ${state.get_cost_per_game()}")
    print(f"Can play? {state.can_play()}")
    # Use start_fixed_cost_game for poker/blackjack
    if state.start_game():
        print(f"Started game. Money left: ${state.money}")
    else:
        print("Cannot start game.")

    state.add_winnings(3)
    print(f"Won $3. Current money: ${state.money}")

    # Test changing cost
    state.set_cost_per_game(3)
    print(f"New cost per game: ${state.get_cost_per_game()}")

    # Test variable bets
    print(f"Can afford $2 bet? {state.can_afford_bet(2)}")
    if state.deduct_bet(2):
        print(f"Placed $2 bet. Money left: ${state.money}")
    print(f"Can afford $10 bet? {state.can_afford_bet(10)}")
    if not state.deduct_bet(10):
        print(f"Could not place $10 bet. Money left: ${state.money}")

    # Play until broke
    while state.start_fixed_cost_game():
        print(f"Played a game. Money left: ${state.money}")

    print(f"Final money: ${state.money}")
    print(f"Can play? {state.can_play()}")

    # Test invalid starting money
    try:
        GameState(0)
    except ValueError as e:
        print(f"Caught expected error: {e}")

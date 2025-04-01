# /roulette_rules.py
from typing import Dict, Tuple, Set, Any

# --- Bet Types ---
# Using strings for bet keys for easy storage in game_state
# Format: 'type_value' e.g., 'number_5', 'color_red', 'dozen_1'

# --- Payout Odds ---
# Dictionary mapping bet type prefix to payout multiplier (X:1)
# Payout includes the original bet back (e.g., 35:1 means you get 36 back for $1 bet)
ROULETTE_PAYOUTS: Dict[str, int] = {
    "number": 35,  # Single number (Straight Up)
    "split": 17,   # Two numbers
    "street": 11,  # Three numbers (row)
    "corner": 8,   # Four numbers
    "sixline": 5,  # Six numbers (two rows)
    "column": 2,   # Column (12 numbers)
    "dozen": 2,    # Dozen (1-12, 13-24, 25-36)
    "color": 1,    # Red or Black (18 numbers)
    "parity": 1,   # Even or Odd (18 numbers)
    "half": 1,     # Low (1-18) or High (19-36)
}

# --- Number Properties ---
RED_NUMBERS: Set[int] = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_NUMBERS: Set[int] = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
GREEN_NUMBER: Set[int] = {0}

# --- Bet Definitions (Mapping bet keys to winning numbers) ---
# This helps determine if a bet wins based on the winning number.
# We can generate this dynamically or define it explicitly. Let's define some common ones.

def get_winning_numbers_for_bet(bet_key: str) -> Set[int]:
    """Returns the set of numbers that win for a given bet key."""
    parts = bet_key.split('_')
    bet_type = parts[0]
    bet_value = parts[1] if len(parts) > 1 else None

    if bet_type == "number" and bet_value is not None:
        return {int(bet_value)}
    elif bet_type == "color":
        if bet_value == "red":
            return RED_NUMBERS
        elif bet_value == "black":
            return BLACK_NUMBERS
    elif bet_type == "parity":
        if bet_value == "even":
            # Exclude 0 for even/odd bets
            return {n for n in range(1, 37) if n % 2 == 0}
        elif bet_value == "odd":
            return {n for n in range(1, 37) if n % 2 != 0}
    elif bet_type == "half":
        if bet_value == "low": # 1-18
            return set(range(1, 19))
        elif bet_value == "high": # 19-36
            return set(range(19, 37))
    elif bet_type == "dozen":
        if bet_value == "1": # 1-12
            return set(range(1, 13))
        elif bet_value == "2": # 13-24
            return set(range(13, 25))
        elif bet_value == "3": # 25-36
            return set(range(25, 37))
    elif bet_type == "column":
        col_num = int(bet_value)
        # Column 1: 1, 4, 7, ... 34
        # Column 2: 2, 5, 8, ... 35
        # Column 3: 3, 6, 9, ... 36
        start_num = col_num
        return {n for n in range(start_num, 37, 3)}

    # TODO: Add logic for Split, Street, Corner, Sixline if needed later
    # These require knowing the grid layout precisely.

    return set() # Return empty set for unknown or unimplemented bet types

def get_payout_for_bet(bet_key: str) -> int:
    """Returns the payout multiplier (e.g., 35 for number) for a given bet key."""
    bet_type = bet_key.split('_')[0]
    return ROULETTE_PAYOUTS.get(bet_type, 0)

if __name__ == '__main__':
    # Example Usage
    print(f"Payout for number_5: {get_payout_for_bet('number_5')}")
    print(f"Payout for color_red: {get_payout_for_bet('color_red')}")
    print(f"Winning numbers for color_red: {get_winning_numbers_for_bet('color_red')}")
    print(f"Winning numbers for dozen_2: {get_winning_numbers_for_bet('dozen_2')}")
    print(f"Winning numbers for column_3: {get_winning_numbers_for_bet('column_3')}")
    print(f"Winning numbers for parity_even: {get_winning_numbers_for_bet('parity_even')}")
    print(f"Winning numbers for half_high: {get_winning_numbers_for_bet('half_high')}")

import random
from typing import List, Tuple, Dict

# --- Constants ---
NUM_REELS = 3
# Define the symbols present on each virtual reel strip
# More frequent symbols appear more often
# Order matters for visual representation during spin, but final result is random pick
REEL_STRIPS: List[List[str]] = [
    # Reel 1
    ["cherry", "1bar", "cherry", "2bar", "cherry", "3bar", "cherry", "bell", "cherry", "7",
     "1bar", "2bar", "1bar", "bell", "1bar", "3bar", "1bar", "7", "1bar", "bell"],
    # Reel 2
    ["cherry", "1bar", "2bar", "bell", "3bar", "7", "1bar", "2bar", "bell", "1bar",
     "cherry", "3bar", "bell", "2bar", "1bar", "7", "bell", "3bar", "2bar", "cherry"],
    # Reel 3
    ["cherry", "bell", "1bar", "7", "2bar", "bell", "3bar", "1bar", "cherry", "2bar",
     "bell", "1bar", "3bar", "7", "cherry", "bell", "1bar", "2bar", "3bar", "7"]
]

# Define the single payline (middle row)
# Indices correspond to the visible symbols on the reels (e.g., [reel1_symbol, reel2_symbol, reel3_symbol])
# For a simple 3-reel machine, the payline is just the result of the spin.
# If we had multiple rows visible, we'd specify which row is the payline.

# --- Payout Table --- Adjusted for ~95% RTP (House Edge ~5%) ---
# Maps winning combinations (as tuples of symbol names) to their payout multiplier.
# Order within the tuple matters if the combination is order-dependent (usually not in slots).
# Use counts for combinations like "any bar".
SLOTS_PAYOUTS: Dict[Tuple[str, ...], int] = {
    ("7", "7", "7"): 60,         # Reduced from 100
    ("bell", "bell", "bell"): 10,  # Reduced from 20
    ("3bar", "3bar", "3bar"): 20,  # Reduced from 50
    ("2bar", "2bar", "2bar"): 15,  # Reduced from 40
    ("1bar", "1bar", "1bar"): 10,  # Reduced from 30
    # Combinations of bars (Any Bar) - Handled separately in calculation
    ("cherry", "cherry", "cherry"): 5, # Reduced from 10
    ("cherry", "cherry", None): 2,      # Reduced from 5 (Two cherries)
    ("cherry", None, None): 1,          # Reduced from 2 (One cherry - significant impact)
}

BAR_SYMBOLS = {"1bar", "2bar", "3bar"}

def spin_reels() -> List[str]:
    """Simulates spinning the reels and returns the result on the payline."""
    result = []
    for strip in REEL_STRIPS:
        # Pick a random symbol from the strip for each reel
        result.append(random.choice(strip))
    return result

def calculate_winnings(payline_symbols: List[str], bet_amount: int) -> Tuple[int, str]:
    """
    Calculates the winnings based on the symbols shown on the payline.

    Args:
        payline_symbols: A list of symbol names on the payline (e.g., ['cherry', '7', '1bar']).
        bet_amount: The amount bet for this spin.

    Returns:
        A tuple containing:
        - The total winning amount (payout * bet_amount).
        - A string describing the winning combination, or "" if no win.
    """
    payline_tuple = tuple(payline_symbols) # Convert list to tuple for dictionary lookup

    # --- Check for specific 3-symbol combinations first ---
    if payline_tuple in SLOTS_PAYOUTS:
        payout_multiplier = SLOTS_PAYOUTS[payline_tuple]
        win_name = f"{payline_symbols[0]}, {payline_symbols[1]}, {payline_symbols[2]}"
        return payout_multiplier * bet_amount, win_name

    # --- Check for "Any Bar" combination ---
    num_bars = sum(1 for symbol in payline_symbols if symbol in BAR_SYMBOLS)
    if num_bars == 3:
        # Define a payout for "Any 3 Bars" - Adjusted Payout
        any_bar_payout = 5 # Reduced from 15
        win_name = "Any 3 Bars"
        return any_bar_payout * bet_amount, win_name

    # --- Check for Cherry combinations (handle None placeholders) ---
    # Two cherries (first two reels) - MUST check before single cherry
    if payline_symbols[0] == "cherry" and payline_symbols[1] == "cherry":
        two_cherry_key = ("cherry", "cherry", None)
        if two_cherry_key in SLOTS_PAYOUTS:
            payout_multiplier = SLOTS_PAYOUTS[two_cherry_key]
            win_name = "Two Cherries"
            return payout_multiplier * bet_amount, win_name

    # One cherry (first reel only)
    if payline_symbols[0] == "cherry":
        one_cherry_key = ("cherry", None, None)
        if one_cherry_key in SLOTS_PAYOUTS:
            payout_multiplier = SLOTS_PAYOUTS[one_cherry_key]
            win_name = "One Cherry"
            return payout_multiplier * bet_amount, win_name

    # --- No win ---
    return 0, ""

if __name__ == '__main__':
    # Example Usage remains the same for testing
    print("Simulating 10 spins with adjusted payouts:")
    for i in range(10):
        result = spin_reels()
        winnings, win_name = calculate_winnings(result, 1)
        print(f"Spin {i+1}: {result} -> Win: ${winnings} ({win_name if winnings > 0 else 'No Win'})")

    print("\nTesting specific payouts (adjusted):")
    test_lines = [
        (["7", "7", "7"], "Triple 7s"),
        (["bell", "bell", "bell"], "Triple Bells"),
        (["1bar", "2bar", "3bar"], "Any 3 Bars"),
        (["cherry", "cherry", "7"], "Two Cherries"),
        (["cherry", "1bar", "bell"], "One Cherry"),
        (["1bar", "bell", "7"], "No Win"),
    ]
    for line, name in test_lines:
        winnings, win_name_calc = calculate_winnings(line, 1)
        print(f"Test: {line} ({name}) -> Win: ${winnings} ({win_name_calc})")


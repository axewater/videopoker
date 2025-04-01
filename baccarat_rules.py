# /baccarat_rules.py
"""
Defines the rules, card values, hand calculations, and win conditions for Baccarat.
"""
from typing import List, Tuple, Dict, Optional

from card import Card

# --- Baccarat Card Values ---
BACCARAT_VALUES: Dict[str, int] = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "T": 0, "J": 0, "Q": 0, "K": 0
}

# --- Payout Constants ---
# Standard payouts: Player 1:1, Banker 1:1 (with 5% commission on win), Tie 8:1
# Note: Banker payout is effectively 0.95:1
PLAYER_PAYOUT = 1.0
BANKER_PAYOUT = 0.95 # Net payout after 5% commission on win
TIE_PAYOUT = 8.0
LOSS_PAYOUT = -1.0
PUSH_PAYOUT = 0.0 # For Tie when bet is on Player/Banker

# --- Bet Types ---
BET_PLAYER = "Player"
BET_BANKER = "Banker"
BET_TIE = "Tie"

def get_baccarat_hand_value(hand: List[Card]) -> int:
    """Calculates the value of a Baccarat hand (sum modulo 10)."""
    value = sum(BACCARAT_VALUES.get(card.rank, 0) for card in hand)
    return value % 10

def is_natural(hand: List[Card]) -> bool:
    """Checks if a two-card hand is a 'Natural' (value 8 or 9)."""
    return len(hand) == 2 and get_baccarat_hand_value(hand) in [8, 9]

def should_player_draw(player_hand: List[Card]) -> bool:
    """Determines if the Player should draw a third card (value 0-5)."""
    # Player stands on 6 or 7, draws on 0-5. Naturals (8, 9) are handled separately.
    return get_baccarat_hand_value(player_hand) <= 5

def should_banker_draw(banker_hand: List[Card], player_third_card: Optional[Card]) -> bool:
    """
    Determines if the Banker should draw a third card based on Banker's value
    and the Player's third card (if drawn).
    """
    banker_value = get_baccarat_hand_value(banker_hand)

    # If Player did NOT draw a third card (stood on 6/7 or had Natural)
    if player_third_card is None:
        # Banker draws on 0-5, stands on 6-7 (Naturals already handled)
        return banker_value <= 5
    else:
        # Player DID draw a third card. Banker's draw depends on complex rules:
        player_third_card_value = BACCARAT_VALUES.get(player_third_card.rank, 0)

        if banker_value <= 2:
            return True
        elif banker_value == 3:
            return player_third_card_value != 8 # Banker draws unless Player's 3rd was 8
        elif banker_value == 4:
            # Banker draws if Player's 3rd was 2, 3, 4, 5, 6, 7
            return player_third_card_value in [2, 3, 4, 5, 6, 7]
        elif banker_value == 5:
            # Banker draws if Player's 3rd was 4, 5, 6, 7
            return player_third_card_value in [4, 5, 6, 7]
        elif banker_value == 6:
            # Banker draws if Player's 3rd was 6, 7
            return player_third_card_value in [6, 7]
        else: # Banker value is 7
            return False # Banker always stands on 7

def determine_baccarat_winner(player_hand: List[Card], banker_hand: List[Card]) -> Tuple[str, int, int]:
    """
    Compares the final Player and Banker hands and determines the winner.

    Returns:
        A tuple containing:
        - Winning hand name ("Player", "Banker", "Tie").
        - Player's final hand value.
        - Banker's final hand value.
    """
    player_value = get_baccarat_hand_value(player_hand)
    banker_value = get_baccarat_hand_value(banker_hand)

    if player_value > banker_value:
        winner = BET_PLAYER
    elif banker_value > player_value:
        winner = BET_BANKER
    else:
        winner = BET_TIE

    return winner, player_value, banker_value

def calculate_baccarat_payout(bet_type: str, bet_amount: int, winning_hand: str) -> Tuple[int, float]:
    """
    Calculates the payout based on the bet placed and the winning hand.

    Args:
        bet_type: The type of bet placed ("Player", "Banker", "Tie").
        bet_amount: The amount wagered.
        winning_hand: The result of the round ("Player", "Banker", "Tie").

    Returns:
        A tuple containing:
        - The total amount returned to the player (original bet + winnings).
        - The net win/loss amount.
    """
    if bet_type == winning_hand:
        if bet_type == BET_PLAYER:
            payout_multiplier = PLAYER_PAYOUT
        elif bet_type == BET_BANKER:
            payout_multiplier = BANKER_PAYOUT
        else: # Bet was Tie, and it was a Tie
            payout_multiplier = TIE_PAYOUT

        net_winnings = bet_amount * payout_multiplier
        total_returned = bet_amount + net_winnings
        return int(round(total_returned)), net_winnings # Round to avoid float issues

    elif winning_hand == BET_TIE and bet_type in [BET_PLAYER, BET_BANKER]:
        # Push: Bet on Player or Banker, and the result is a Tie
        return bet_amount, 0.0 # Return original bet, net win is 0

    else:
        # Loss
        return 0, -bet_amount # Return 0, net loss is the bet amount

if __name__ == '__main__':
    # Example Usage
    p_hand1 = [Card("8", "S"), Card("K", "D")] # Player 8
    b_hand1 = [Card("7", "H"), Card("A", "C")] # Banker 8 (Tie)
    p_hand2 = [Card("A", "S"), Card("5", "D")] # Player 6
    b_hand2 = [Card("K", "H"), Card("Q", "C")] # Banker 0
    p_hand3 = [Card("2", "S"), Card("3", "D")] # Player 5
    b_hand3 = [Card("6", "H"), Card("J", "C")] # Banker 6

    print(f"Hand: {p_hand1}, Value: {get_baccarat_hand_value(p_hand1)}")
    print(f"Hand: {b_hand1}, Value: {get_baccarat_hand_value(b_hand1)}")
    winner1, pv1, bv1 = determine_baccarat_winner(p_hand1, b_hand1)
    print(f"Result 1: Winner={winner1}, P={pv1}, B={bv1}")

    print(f"\nHand: {p_hand2}, Value: {get_baccarat_hand_value(p_hand2)}")
    print(f"Hand: {b_hand2}, Value: {get_baccarat_hand_value(b_hand2)}")
    print(f"Player Draws? {should_player_draw(p_hand2)}") # False (stands on 6)
    print(f"Banker Draws (Player Stood)? {should_banker_draw(b_hand2, None)}") # True (draws on 0)
    # Assume Banker draws '4' -> Banker hand [K, Q, 4] -> Value 4
    b_hand2_final = b_hand2 + [Card("4", "S")]
    winner2, pv2, bv2 = determine_baccarat_winner(p_hand2, b_hand2_final)
    print(f"Result 2 (after Banker draw): Winner={winner2}, P={pv2}, B={get_baccarat_hand_value(b_hand2_final)}")

    print(f"\nHand: {p_hand3}, Value: {get_baccarat_hand_value(p_hand3)}")
    print(f"Hand: {b_hand3}, Value: {get_baccarat_hand_value(b_hand3)}")
    print(f"Player Draws? {should_player_draw(p_hand3)}") # True (draws on 5)
    # Assume Player draws '8' -> Player hand [2, 3, 8] -> Value 3
    p_hand3_final = p_hand3 + [Card("8", "C")]
    player_third = p_hand3_final[2]
    print(f"Banker Draws (Player drew {player_third.rank})? {should_banker_draw(b_hand3, player_third)}") # False (Banker stands on 6 when Player drew 8)
    winner3, pv3, bv3 = determine_baccarat_winner(p_hand3_final, b_hand3)
    print(f"Result 3 (after Player draw): Winner={winner3}, P={get_baccarat_hand_value(p_hand3_final)}, B={bv3}")

    # Payout examples (Bet $10)
    bet = 10
    print("\nPayout Tests (Bet $10):")
    ret, net = calculate_baccarat_payout(BET_PLAYER, bet, BET_PLAYER)
    print(f"Bet Player, Win Player: Returned=${ret}, Net=${net:.2f}")
    ret, net = calculate_baccarat_payout(BET_BANKER, bet, BET_BANKER)
    print(f"Bet Banker, Win Banker: Returned=${ret}, Net=${net:.2f}")
    ret, net = calculate_baccarat_payout(BET_TIE, bet, BET_TIE)
    print(f"Bet Tie, Win Tie: Returned=${ret}, Net=${net:.2f}")
    ret, net = calculate_baccarat_payout(BET_PLAYER, bet, BET_BANKER)
    print(f"Bet Player, Win Banker: Returned=${ret}, Net=${net:.2f}")
    ret, net = calculate_baccarat_payout(BET_BANKER, bet, BET_PLAYER)
    print(f"Bet Banker, Win Player: Returned=${ret}, Net=${net:.2f}")
    ret, net = calculate_baccarat_payout(BET_PLAYER, bet, BET_TIE)
    print(f"Bet Player, Win Tie: Returned=${ret}, Net=${net:.2f}")
    ret, net = calculate_baccarat_payout(BET_BANKER, bet, BET_TIE)
    print(f"Bet Banker, Win Tie: Returned=${ret}, Net=${net:.2f}")
    ret, net = calculate_baccarat_payout(BET_TIE, bet, BET_PLAYER)
    print(f"Bet Tie, Win Player: Returned=${ret}, Net=${net:.2f}")

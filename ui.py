import os
from typing import List, Optional
from card import Card, card_to_string
from poker_rules import get_pay_table_string

def clear_screen():
    """Clears the terminal screen."""
    # Works for Windows ('nt') and Linux/MacOS ('posix')
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome_message():
    """Displays the initial welcome message."""
    print("=============================")
    print("    Welcome to Video Poker!  ")
    print("=============================")
    print("(Based on Jacks or Better rules)")
    print()

def display_main_menu() -> str:
    """Displays the main menu options and gets user choice."""
    print("\n--- Main Menu ---")
    print("1: Play Game")
    print("2: Quit")
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return choice
        else:
            print("Invalid input. Please enter 1 or 2.")

def display_game_over():
    """Displays the game over message."""
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("         GAME OVER          ")
    print(" You have run out of money! ")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    input("Press Enter to return to the main menu...")

def display_hand(hand: List[Card], held_indices: Optional[List[int]] = None):
    """Displays the player's hand with indices and indicates held cards."""
    print("\n--- Your Hand ---")
    hand_str = []
    held_status = []
    for i, card in enumerate(hand):
        hand_str.append(f"({i+1}) {card_to_string(card)}")
        if held_indices is not None and i in held_indices:
            held_status.append(" [HELD] ")
        else:
            held_status.append("        ") # Match length for alignment

    print(" ".join(hand_str))
    print(" ".join(held_status))
    print("-" * (len(hand_str) * 8)) # Adjust separator length

def display_game_state(money: int, message: str = ""):
    """Displays the current money and any messages."""
    print(f"\nMoney: ${money}")
    if message:
        print(message)

def display_pay_table():
    """Displays the pay table."""
    print("\n" + get_pay_table_string())


def get_cards_to_hold(num_cards: int) -> List[int]:
    """Prompts the player to enter the indices of cards to hold."""
    while True:
        hold_input = input(f"Enter numbers (1-{num_cards}) of cards to hold (e.g., 1 3 5), or '0' for none: ").strip()
        
        if hold_input == '0':
            return []
            
        try:
            # Split input, convert to int, adjust to 0-based index
            indices = [int(x.strip()) - 1 for x in hold_input.split() if x.strip()]
            
            # Validate indices
            if not indices: # Handle empty input after splitting spaces
                 print("Invalid input. Please enter numbers separated by spaces, or 0.")
                 continue
                 
            valid = True
            for index in indices:
                if not (0 <= index < num_cards):
                    print(f"Invalid card number: {index + 1}. Please enter numbers between 1 and {num_cards}.")
                    valid = False
                    break
            
            if valid:
                 # Return unique, sorted indices
                 return sorted(list(set(indices)))
                 
        except ValueError:
            print("Invalid input. Please enter only numbers separated by spaces.")

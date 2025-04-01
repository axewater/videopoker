# /config_states.py
"""
Configuration constants defining the different states of the application.
"""

# Game States
STATE_TOP_MENU = "TOP_MENU" # New top-level menu
STATE_GAME_SELECTION = "GAME_SELECTION" # Renamed from STATE_MAIN_MENU
STATE_SETTINGS = "SETTINGS" # New settings screen
STATE_DRAW_POKER_IDLE = "DRAW_POKER_IDLE" # Before first deal
STATE_DRAW_POKER_DEALING = "DRAW_POKER_DEALING" # Optional: Could add animation later
STATE_DRAW_POKER_WAITING_FOR_HOLD = "DRAW_POKER_WAITING_FOR_HOLD"
STATE_DRAW_POKER_DRAWING = "DRAW_POKER_DRAWING" # Optional: Could add animation later
STATE_DRAW_POKER_SHOWING_RESULT = "DRAW_POKER_SHOWING_RESULT"
# Multi Poker States
STATE_MULTI_POKER_IDLE = "MULTI_POKER_IDLE" # Before first deal
STATE_MULTI_POKER_WAITING_FOR_HOLD = "MULTI_POKER_WAITING_FOR_HOLD"
STATE_MULTI_POKER_DRAWING = "MULTI_POKER_DRAWING" # Optional animation state
STATE_MULTI_POKER_SHOWING_RESULT = "MULTI_POKER_SHOWING_RESULT"
STATE_GAME_OVER = "GAME_OVER"
STATE_CONFIRM_EXIT = "CONFIRM_EXIT" # New state for exit confirmation
STATE_BLACKJACK_IDLE = "BLACKJACK_IDLE" # Before bet/deal
STATE_BLACKJACK_PLAYER_TURN = "BLACKJACK_PLAYER_TURN"
STATE_BLACKJACK_DEALER_TURN = "BLACKJACK_DEALER_TURN" # Dealer plays out
STATE_BLACKJACK_SHOWING_RESULT = "BLACKJACK_SHOWING_RESULT"
# Roulette States
STATE_ROULETTE_BETTING = "ROULETTE_BETTING"
STATE_ROULETTE_SPINNING = "ROULETTE_SPINNING" # Includes pause phase now
STATE_ROULETTE_RESULT = "ROULETTE_RESULT"
# Slots States (Added)
STATE_SLOTS_IDLE = "SLOTS_IDLE"
STATE_SLOTS_SPINNING = "SLOTS_SPINNING"
STATE_SLOTS_SHOWING_RESULT = "SLOTS_SHOWING_RESULT"
# Baccarat States (Added)
STATE_BACCARAT_BETTING = "BACCARAT_BETTING"
STATE_BACCARAT_DEALING = "BACCARAT_DEALING" # Initial deal + natural check
STATE_BACCARAT_DRAWING = "BACCARAT_DRAWING" # Player/Banker draw phase
STATE_BACCARAT_RESULT = "BACCARAT_RESULT"

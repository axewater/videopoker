# /config_animations.py
"""
Configuration constants related to animation timings and effects.
"""

# Animation Constants
MONEY_ANIMATION_DURATION = 60 # Frames (e.g., 2 seconds at 30 FPS)
ROULETTE_SPIN_DURATION = 180 # Increased duration (e.g., 6 seconds at 30 FPS)
ROULETTE_RESULT_PAUSE_DURATION = 30 # Frames to pause after spin (e.g., 1 second at 30 FPS)
ROULETTE_FLASH_COUNT = 3 # Number of times the winning slot flashes
ROULETTE_FLASH_INTERVAL = 10 # Frames for one flash state (on/off) - Total flash cycle = 2*INTERVAL
MONEY_ANIMATION_OFFSET_Y = 30 # Pixels below the main money display
RESULT_FLASH_DURATION = 45 # Frames (e.g., 1.5 seconds at 30 FPS)
RESULT_FLASH_INTERVAL = 5 # Frames between toggling visibility
# Slots Animation Constants (Added)
SLOTS_SPIN_DURATION = 90 # Frames (e.g., 3 seconds at 30 FPS)
SLOTS_RESULT_PAUSE_DURATION = 60 # Frames (e.g., 2 seconds at 30 FPS)

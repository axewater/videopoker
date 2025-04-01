import pygame
import os
import sys
from typing import Dict

import constants

def load_card_images(path: str) -> Dict[str, pygame.Surface]:
    """Loads card images from the specified path."""
    images = {}
    if not os.path.exists(path):
        print(f"Error: Asset path not found: {os.path.abspath(path)}")
        print("Please ensure card images are in an 'assets/cards' directory relative to main.py.")
        print("Exiting.")
        pygame.quit()
        sys.exit()

    try:
        # Standard ranks and suits for filenames
        ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        suits_short = ['S', 'H', 'D', 'C'] # Spades, Hearts, Diamonds, Clubs

        for suit_short in suits_short:
            for rank in ranks:
                filename = f"{rank}{suit_short}.png"
                filepath = os.path.join(path, filename)
                if not os.path.isfile(filepath):
                     print(f"Warning: Card image file not found: {filepath}")
                     continue # Skip if a specific file is missing

                img = pygame.image.load(filepath).convert_alpha()
                # Scale image if needed (optional, adjust CARD_WIDTH/HEIGHT in constants)
                img = pygame.transform.scale(img, (constants.CARD_WIDTH, constants.CARD_HEIGHT))
                images[f"{rank}{suit_short}"] = img

    except pygame.error as e:
        print(f"Error loading image: {e}")
        print(f"Searched in path: {os.path.abspath(path)}")
        pygame.quit()
        sys.exit()

    if len(images) < 52:
        print(f"Warning: Loaded only {len(images)} card images from {os.path.abspath(path)}. Expected 52.")
        if not images: # Exit if no images loaded at all
             print("Error: No card images loaded. Exiting.")
             pygame.quit()
             sys.exit()

    return images

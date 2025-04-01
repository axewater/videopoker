import pygame
import os
import sys
from typing import Dict, List

import constants

# Define the order and names of the symbols
# This order should ideally match how you want them displayed or processed
SLOT_SYMBOL_NAMES: List[str] = ["7", "3bar", "2bar", "1bar", "bell", "cherry"]

def load_slot_images(path: str, symbol_size: tuple[int, int]) -> Dict[str, pygame.Surface]:
    """Loads slot symbol images from the specified path."""
    images = {}
    if not os.path.exists(path):
        print(f"Error: Slots asset path not found: {os.path.abspath(path)}")
        print("Please ensure slot images are in an 'assets/slots' directory relative to main.py.")
        print("Exiting.")
        pygame.quit()
        sys.exit()

    try:
        for symbol_name in SLOT_SYMBOL_NAMES:
            filename = f"{symbol_name}.png"
            filepath = os.path.join(path, filename)
            if not os.path.isfile(filepath):
                 print(f"Warning: Slot image file not found: {filepath}")
                 continue # Skip if a specific file is missing

            img = pygame.image.load(filepath).convert_alpha()
            # Scale image to the desired symbol size
            img = pygame.transform.scale(img, symbol_size)
            images[symbol_name] = img
            print(f"Loaded slot image: {symbol_name}")

    except pygame.error as e:
        print(f"Error loading slot image: {e}")
        print(f"Searched in path: {os.path.abspath(path)}")
        pygame.quit()
        sys.exit()

    if len(images) != len(SLOT_SYMBOL_NAMES):
        print(f"Warning: Loaded only {len(images)} slot images from {os.path.abspath(path)}. Expected {len(SLOT_SYMBOL_NAMES)}.")
        if not images: # Exit if no images loaded at all
             print("Error: No slot images loaded. Exiting.")
             pygame.quit()
             sys.exit()

    return images

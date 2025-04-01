import pygame
import os
from typing import Dict

import config_assets as assets
from .dummy_sound import DummySound # Relative import

def load_sounds(sound_enabled: bool) -> Dict[str, pygame.mixer.Sound | DummySound]:
    """Loads sound effects from files."""
    sounds = {}
    # If sound is globally disabled, return dummy sounds immediately
    if not sound_enabled:
        for name in assets.SOUND_FILES.keys():
            sounds[name] = DummySound()
        print("Sound disabled. Using dummy sound objects.")
        return sounds

    # Initialize mixer if not already done (safe to call multiple times)
    if sound_enabled and not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
            print("Sound system initialized by load_sounds.")
        except pygame.error as e:
            print(f"Warning: Failed to initialize sound system in load_sounds: {e}")
            # Fallback to dummy sounds if init fails here
            for name in assets.SOUND_FILES.keys():
                sounds[name] = DummySound()
            return sounds

    for name, filename in assets.SOUND_FILES.items():
        path = os.path.join(assets.SOUND_ASSET_PATH, filename)
        try:
            sound = pygame.mixer.Sound(path)
            sounds[name] = sound
            print(f"Loaded sound: {name} ({filename})")
        except pygame.error as e:
            print(f"Warning: Could not load sound '{filename}': {e}")
            # Assign a dummy sound object for this specific sound
            sounds[name] = DummySound()
    return sounds

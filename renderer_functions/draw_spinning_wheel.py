# /renderer_functions/draw_spinning_wheel.py
# NEW FILE
import pygame
import math
from typing import Dict, Any, Tuple

import constants
from .draw_text import draw_text
from .get_font import get_font # Helper to get fonts if needed directly

# Helper to get color (copied from draw_roulette_screen for consistency)
def get_number_color(number: int) -> Tuple[int, int, int]:
    """Returns the Pygame color for a given roulette number."""
    if number == 0:
        return constants.ROULETTE_COLOR_GREEN
    elif number in constants.ROULETTE_RED_NUMBERS:
        return constants.ROULETTE_COLOR_RED
    elif number in constants.ROULETTE_BLACK_NUMBERS:
        return constants.ROULETTE_COLOR_BLACK
    else:
        return constants.WHITE # Should not happen

def draw_spinning_wheel(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], game_state: Dict[str, Any]):
    """Draws the spinning wheel overlay animation, including the pause/flash phase."""

    center_x = constants.SCREEN_WIDTH // 2
    center_y = constants.SCREEN_HEIGHT // 2
    wheel_radius = min(center_x, center_y) - 50 # Radius of the main wheel
    number_radius = wheel_radius - 25 # Radius for placing numbers
    # --- Ball related variables removed ---
    # ball_track_radius = wheel_radius + 15
    # ball_radius = 8

    # --- Semi-transparent background overlay ---
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) # Dark overlay
    surface.blit(overlay, (0, 0))

    # --- Calculate Rotation ---
    spin_timer = game_state.get('roulette_spin_timer', 0)
    pause_timer = game_state.get('roulette_pause_timer', 0) # Get pause timer
    total_duration = constants.ROULETTE_SPIN_DURATION
    winning_number = game_state.get('roulette_winning_number')

    if winning_number is None:
        print("Warning: Winning number not set during spin animation.")
        winning_number = 0

    try:
        winning_number_index = constants.ROULETTE_WHEEL_NUMBERS.index(winning_number)
    except ValueError:
        print(f"Error: Winning number {winning_number} not found in wheel layout.")
        winning_number_index = 0

    num_slots = len(constants.ROULETTE_WHEEL_NUMBERS)
    angle_per_slot = 360 / num_slots
    # Target angle for the *wheel* rotation to place the winning slot at the top pointer
    target_angle = (winning_number_index * angle_per_slot) + (angle_per_slot / 2)

    current_angle = 0
    # --- Ball angle calculation removed ---
    # ball_current_angle = 0

    # Determine wheel rotation based on phase (spinning or paused)
    if spin_timer > 0:
        # Still spinning
        time_elapsed = total_duration - spin_timer
        progress = time_elapsed / total_duration
        eased_progress = 1 - (1 - progress) ** 3 # Cubic ease-out

        # Wheel rotation
        total_spins = 5
        current_angle = (total_spins * 360 + target_angle) * eased_progress

        # --- Ball animation logic removed ---

    else: # spin_timer is 0, wheel is stopped (might be pausing/flashing)
        current_angle = target_angle # Wheel stops at target angle
        # --- Ball angle setting removed ---

    # --- Ball coordinate calculation removed ---

    # --- Draw Wheel ---
    wheel_surf_size = wheel_radius * 2
    wheel_surf = pygame.Surface((wheel_surf_size, wheel_surf_size), pygame.SRCALPHA)
    wheel_center = wheel_radius

    number_font = fonts.get('pay_table')
    if not number_font: number_font = get_font(16)

    # Get flashing state
    is_flashing = game_state.get('winning_slot_flash_active', False)
    is_flash_visible = game_state.get('winning_slot_flash_visible', True)

    for i, number in enumerate(constants.ROULETTE_WHEEL_NUMBERS):
        start_angle_deg = i * angle_per_slot
        end_angle_deg = (i + 1) * angle_per_slot
        color = get_number_color(number)

        # --- Flashing Logic ---
        is_winning_slot = (number == winning_number)
        current_color = color
        border_thickness = 1 # Default border
        border_color = constants.GOLD

        # Only flash when the wheel is stopped (spin_timer == 0)
        if spin_timer == 0 and is_winning_slot and is_flashing:
            if is_flash_visible:
                # Highlight when flash is visible (e.g., bright yellow border)
                border_thickness = 3
                border_color = constants.ROULETTE_FLASH_COLOR
            else:
                 pass # Draw normally when not visible during flash cycle

        # Calculate points for polygon wedge
        points = [(wheel_center, wheel_center)]
        steps = 5
        for j in range(steps + 1):
            # Angle adjustment for Pygame coordinates (-90 degrees)
            angle = math.radians(start_angle_deg + (end_angle_deg - start_angle_deg) * j / steps - 90)
            x = wheel_center + wheel_radius * math.cos(angle)
            y = wheel_center + wheel_radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(wheel_surf, current_color, points) # Use current_color
        # Draw border with potentially adjusted thickness/color
        # Exclude the center point when drawing lines
        pygame.draw.lines(wheel_surf, border_color, False, points[1:], border_thickness)


        # Draw number text (rotated)
        text_angle_deg = start_angle_deg + angle_per_slot / 2
        # Position calculation based on angle
        text_x = wheel_center + number_radius * math.cos(math.radians(text_angle_deg - 90))
        text_y = wheel_center + number_radius * math.sin(math.radians(text_angle_deg - 90))

        num_surf = number_font.render(str(number), True, constants.WHITE)
        # Rotation angle needs to be negative for clockwise text rotation in Pygame
        num_surf_rotated = pygame.transform.rotate(num_surf, -text_angle_deg)
        num_rect = num_surf_rotated.get_rect(center=(text_x, text_y))
        wheel_surf.blit(num_surf_rotated, num_rect)

    # Rotate the entire wheel surface based on the calculated current_angle
    rotated_wheel_surf = pygame.transform.rotate(wheel_surf, current_angle)
    rotated_rect = rotated_wheel_surf.get_rect(center=(center_x, center_y))

    # Blit the rotated wheel onto the main surface
    surface.blit(rotated_wheel_surf, rotated_rect)

    # Draw center pin
    pygame.draw.circle(surface, constants.GOLD, (center_x, center_y), 15)
    pygame.draw.circle(surface, constants.BLACK, (center_x, center_y), 13)

    # --- Draw Ball removed ---

    # --- Draw Pointer ---
    pointer_size = 20
    pointer_points = [
        (center_x, center_y - wheel_radius - 5), # Tip
        (center_x - pointer_size // 2, center_y - wheel_radius - pointer_size - 5), # Bottom left
        (center_x + pointer_size // 2, center_y - wheel_radius - pointer_size - 5), # Bottom right
    ]
    pygame.draw.polygon(surface, constants.GOLD, pointer_points)

    # Display winning number text only when wheel is stopped (pause phase)
    if spin_timer == 0:
         win_text = f"Result: {winning_number}"
         draw_text(surface, win_text, fonts['result'], center_x, center_y + wheel_radius + 40, constants.YELLOW, center=True)


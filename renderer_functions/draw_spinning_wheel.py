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
    """Draws the spinning wheel overlay animation."""

    center_x = constants.SCREEN_WIDTH // 2
    center_y = constants.SCREEN_HEIGHT // 2
    wheel_radius = min(center_x, center_y) - 50 # Radius of the main wheel
    number_radius = wheel_radius - 25 # Radius for placing numbers
    ball_track_radius = wheel_radius + 15 # Radius for the ball animation
    ball_radius = 8

    # --- Semi-transparent background overlay ---
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) # Dark overlay
    surface.blit(overlay, (0, 0))

    # --- Calculate Rotation and Ball Position ---
    spin_timer = game_state.get('roulette_spin_timer', 0)
    total_duration = constants.ROULETTE_SPIN_DURATION
    winning_number = game_state.get('roulette_winning_number')

    if winning_number is None: # Should not happen if logic is correct
        print("Warning: Winning number not set during spin animation.")
        winning_number = 0

    # Find the index/position of the winning number on the wheel layout
    try:
        winning_number_index = constants.ROULETTE_WHEEL_NUMBERS.index(winning_number)
    except ValueError:
        print(f"Error: Winning number {winning_number} not found in wheel layout.")
        winning_number_index = 0 # Default to 0

    num_slots = len(constants.ROULETTE_WHEEL_NUMBERS)
    angle_per_slot = 360 / num_slots

    # Calculate target angle (degrees, 0=top, clockwise) for the winning number slot
    # Add a small offset (half slot angle) so pointer aims at middle of slot
    target_angle = (winning_number_index * angle_per_slot) + (angle_per_slot / 2)

    # Animation timing: Ease-out effect (starts fast, ends slow)
    time_elapsed = total_duration - spin_timer
    progress = time_elapsed / total_duration # Linear progress [0, 1]
    # Apply easing function (e.g., quadratic ease-out: 1 - (1-x)^2 )
    eased_progress = 1 - (1 - progress) ** 3 # Cubic ease-out feels better

    # Total rotation: Several full spins + final positioning
    total_spins = 5 # Number of full rotations during animation
    current_angle = (total_spins * 360 + target_angle) * eased_progress
    # Ensure the final angle lands exactly on the target when timer is 0
    if spin_timer == 0:
        current_angle = target_angle

    # Ball animation: Spin opposite direction initially, slow down, drop into slot
    ball_spin_speed_factor = 8 # How many times faster the ball spins than the wheel initially
    ball_slowdown_point = 0.7 # When the ball starts slowing relative to wheel (70% duration)
    ball_angle_offset = 0

    if progress < ball_slowdown_point:
        # Ball spins faster in opposite direction
        ball_angle_offset = -(current_angle * ball_spin_speed_factor * (1 - progress / ball_slowdown_point))
    else:
        # Ball slows down and settles towards the winning slot
        # Calculate how far into the slowdown phase we are
        slowdown_progress = (progress - ball_slowdown_point) / (1 - ball_slowdown_point)
        # Ball angle moves from its fast spin position towards the target angle (relative to wheel)
        # We need the ball angle offset *at the slowdown point* to interpolate from
        ball_angle_at_slowdown = -( (total_spins * 360 + target_angle) * (1 - (1 - ball_slowdown_point) ** 3) * ball_spin_speed_factor * (1 - 1)) # Simplified, offset is relative
        # Let's simplify: just make the ball match the wheel target angle during slowdown
        ball_angle_offset = 0 # Make ball track the target directly in the final phase


    # Final ball angle relative to the fixed coordinates (0 degrees is top)
    # It should end up opposite the winning number slot (as if pointer is at top)
    final_ball_angle_rad = math.radians(-target_angle + 90) # +90 because 0 deg is right in math.atan2

    # Interpolate ball angle during spin
    # Ball spins opposite to wheel rotation, relative to the fixed pointer
    # Let's use a simpler ball animation: fixed track, ball moves around it
    ball_total_rotation = - (total_spins + 3) * 360 # Opposite direction, more spins
    ball_current_angle = ball_total_rotation * eased_progress

    # Calculate final ball position (fixed pointer at top)
    ball_final_angle_deg = -target_angle # Angle relative to top pointer
    ball_final_angle_rad = math.radians(ball_final_angle_deg + 90) # Adjust for math coordinates

    # Ball settles into the target angle in the last part of animation
    settle_start_progress = 0.85
    if progress >= settle_start_progress:
         settle_progress = (progress - settle_start_progress) / (1 - settle_start_progress)
         # Interpolate from spinning angle to final angle
         spin_angle_at_settle = ball_total_rotation * (1 - (1 - settle_start_progress)**3)
         ball_current_angle = spin_angle_at_settle + (ball_final_angle_deg - spin_angle_at_settle) * settle_progress
         # Ensure it ends exactly at the final angle
         if spin_timer == 0:
              ball_current_angle = ball_final_angle_deg


    ball_angle_rad = math.radians(ball_current_angle + 90) # Adjust for math coordinates
    ball_x = center_x + ball_track_radius * math.cos(ball_angle_rad)
    ball_y = center_y - ball_track_radius * math.sin(ball_angle_rad) # Pygame Y is inverted


    # --- Draw Wheel ---
    # Create a subsurface for the wheel for easier rotation
    wheel_surf_size = wheel_radius * 2
    wheel_surf = pygame.Surface((wheel_surf_size, wheel_surf_size), pygame.SRCALPHA)
    wheel_center = wheel_radius # Center within the subsurface

    # Draw wheel segments (arcs or polygons)
    number_font = fonts.get('pay_table') # Smaller font for numbers on wheel
    if not number_font: number_font = get_font(16) # Fallback

    for i, number in enumerate(constants.ROULETTE_WHEEL_NUMBERS):
        start_angle_deg = i * angle_per_slot
        end_angle_deg = (i + 1) * angle_per_slot
        color = get_number_color(number)

        # Calculate points for polygon wedge
        points = [(wheel_center, wheel_center)]
        steps = 5 # Number of points along the arc for smoother curve
        for j in range(steps + 1):
            angle = math.radians(start_angle_deg + (end_angle_deg - start_angle_deg) * j / steps - 90) # Adjust for pygame angle convention
            x = wheel_center + wheel_radius * math.cos(angle)
            y = wheel_center + wheel_radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(wheel_surf, color, points)
        pygame.draw.aalines(wheel_surf, constants.GOLD, False, points[1:], 1) # Outline

        # Draw number text (rotated)
        text_angle_deg = start_angle_deg + angle_per_slot / 2
        text_angle_rad = math.radians(-text_angle_deg) # Negate for rotation direction
        text_x = wheel_center + number_radius * math.cos(math.radians(text_angle_deg - 90))
        text_y = wheel_center + number_radius * math.sin(math.radians(text_angle_deg - 90))

        num_surf = number_font.render(str(number), True, constants.WHITE)
        num_surf_rotated = pygame.transform.rotate(num_surf, text_angle_deg) # Rotate text itself
        num_rect = num_surf_rotated.get_rect(center=(text_x, text_y))
        wheel_surf.blit(num_surf_rotated, num_rect)


    # Rotate the entire wheel surface
    rotated_wheel_surf = pygame.transform.rotate(wheel_surf, current_angle)
    rotated_rect = rotated_wheel_surf.get_rect(center=(center_x, center_y))

    # Blit the rotated wheel onto the main surface
    surface.blit(rotated_wheel_surf, rotated_rect)

    # Draw center pin
    pygame.draw.circle(surface, constants.GOLD, (center_x, center_y), 15)
    pygame.draw.circle(surface, constants.BLACK, (center_x, center_y), 13)

    # --- Draw Ball ---
    pygame.draw.circle(surface, constants.WHITE, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.circle(surface, constants.GREY, (int(ball_x), int(ball_y)), ball_radius - 2) # Inner shadow/highlight


    # --- Draw Pointer ---
    pointer_size = 20
    pointer_points = [
        (center_x, center_y - wheel_radius - 5), # Top point
        (center_x - pointer_size // 2, center_y - wheel_radius - pointer_size - 5),
        (center_x + pointer_size // 2, center_y - wheel_radius - pointer_size - 5),
    ]
    pygame.draw.polygon(surface, constants.GOLD, pointer_points)

    # Display winning number when stopped
    if spin_timer == 0:
         win_text = f"Result: {winning_number}"
         draw_text(surface, win_text, fonts['result'], center_x, center_y + wheel_radius + 40, constants.YELLOW, center=True)


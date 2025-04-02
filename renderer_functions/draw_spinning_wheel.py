# /renderer_functions/draw_spinning_wheel.py
# NEW FILE
import pygame
import math
from typing import Dict, Any, Tuple

# --- Config Imports ---
import config_display as display
import config_colors as colors
import config_animations as animations
import config_layout_roulette as layout_roulette
from .draw_text import draw_text
from .draw_ellipse import draw_ellipse
from .get_font import get_font # Helper to get fonts if needed directly

# Helper to get color (copied from draw_roulette_screen for consistency)
# --- Helper Function ---
def get_number_color(number: int) -> Tuple[int, int, int]:
    """Returns the Pygame color for a given roulette number."""
    if number == 0:
        return colors.ROULETTE_COLOR_GREEN
    elif number in layout_roulette.ROULETTE_RED_NUMBERS:
        return colors.ROULETTE_COLOR_RED
    elif number in layout_roulette.ROULETTE_BLACK_NUMBERS:
        return colors.ROULETTE_COLOR_BLACK
    else:
        return colors.WHITE # Should not happen

# --- Main Drawing Function ---
def draw_spinning_wheel(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], game_state: Dict[str, Any]):
    """Draws the spinning wheel overlay animation, including the pause/flash phase."""

    # Use constants from layout config
    center_pos = (layout_roulette.WHEEL_CENTER_X, layout_roulette.WHEEL_CENTER_Y)
    perspective = layout_roulette.WHEEL_PERSPECTIVE_RATIO

    # Radii (Horizontal)
    rim_outer_r = layout_roulette.RIM_OUTER_RADIUS
    rim_inner_r = layout_roulette.RIM_INNER_RADIUS
    track_outer_r = layout_roulette.TRACK_OUTER_RADIUS
    track_inner_r = layout_roulette.TRACK_INNER_RADIUS
    num_outer_r = layout_roulette.NUMBER_AREA_OUTER_RADIUS
    num_inner_r = layout_roulette.NUMBER_AREA_INNER_RADIUS
    hub_r = layout_roulette.HUB_RADIUS

    # --- Semi-transparent background overlay ---
    overlay = pygame.Surface((display.SCREEN_WIDTH, display.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) # Dark overlay
    surface.blit(overlay, (0, 0))

    # --- Calculate Rotation ---
    spin_timer = game_state.get('roulette_spin_timer', 0)
    pause_timer = game_state.get('roulette_pause_timer', 0) # Get pause timer
    flash_timer = game_state.get('winning_slot_flash_count', 0) # Use flash count timer
    total_duration = animations.ROULETTE_SPIN_DURATION
    winning_number = game_state.get('roulette_winning_number')

    if winning_number is None:
        print("Warning: Winning number not set during spin animation.")
        winning_number = 0

    try:
        winning_number_index = layout_roulette.ROULETTE_WHEEL_NUMBERS.index(winning_number)
    except ValueError:
        print(f"Error: Winning number {winning_number} not found in wheel layout.")
        winning_number_index = 0

    num_slots = len(layout_roulette.ROULETTE_WHEEL_NUMBERS)
    angle_per_slot = 360 / num_slots
    # Target angle for the *ball* to stop at the winning slot's center
    winning_slot_center_angle_deg = winning_number_index * angle_per_slot + angle_per_slot / 2

    ball_current_angle = 0
    ball_current_radius_x = layout_roulette.BALL_START_TRACK_RADIUS
    ball_current_radius_y = ball_current_radius_x * layout_roulette.WHEEL_PERSPECTIVE_RATIO

    if spin_timer > 0:
        # Still spinning
        time_elapsed = total_duration - spin_timer
        progress = time_elapsed / total_duration
        eased_progress = 1 - (1 - progress) ** 3 # Cubic ease-out

        # Ball Animation Logic
        # Ball spins faster initially and slows down, spiraling inwards
        ball_total_spins = 8 # Number of full rotations the ball makes
        ball_target_angle = (ball_total_spins * 360) + winning_slot_center_angle_deg # Absolute target angle
        ball_progress = time_elapsed / total_duration
        ball_eased_progress = 1 - (1 - ball_progress) ** 3 # Cubic ease-out for ball angle
        ball_current_angle = ball_eased_progress * ball_target_angle

        # Ball radius decreases (spirals in)
        radius_progress = time_elapsed / total_duration
        # Ease-in for radius change (starts slow, gets faster)
        radius_eased_progress = radius_progress ** 2.5
        ball_current_radius_x = layout_roulette.BALL_START_TRACK_RADIUS - (layout_roulette.BALL_START_TRACK_RADIUS - layout_roulette.BALL_END_TRACK_RADIUS) * radius_eased_progress
        ball_current_radius_y = ball_current_radius_x * layout_roulette.WHEEL_PERSPECTIVE_RATIO

    else: # spin_timer is 0, wheel is stopped (might be pausing/flashing)
        # Ball settles into the winning slot
        # Ball angle matches the winning slot's center angle
        ball_current_angle = winning_slot_center_angle_deg
        # Ball radius is at the final inner radius
        ball_current_radius_x = layout_roulette.BALL_END_TRACK_RADIUS
        ball_current_radius_y = ball_current_radius_x * layout_roulette.WHEEL_PERSPECTIVE_RATIO

    # --- Draw Static Wheel Parts (Rim, Track) ---
    # Outer Rim (e.g., dark wood color)
    rim_color = (139, 69, 19) # Saddle Brown
    draw_ellipse(surface, rim_color, center_pos, rim_outer_r, rim_outer_r * perspective)
    # Inner part of rim (slightly lighter to create edge)
    rim_inner_color = (160, 82, 45) # Sienna
    draw_ellipse(surface, rim_inner_color, center_pos, rim_inner_r, rim_inner_r * perspective)

    # Ball Track (e.g., lighter wood or grey)
    track_color = (210, 180, 140) # Tan
    draw_ellipse(surface, track_color, center_pos, track_outer_r, track_outer_r * perspective)
    # Inner edge of track (darker to show depth)
    track_inner_edge_color = (188, 143, 143) # Rosy Brown
    draw_ellipse(surface, track_inner_edge_color, center_pos, track_inner_r, track_inner_r * perspective)

    # Create a surface for the wheel itself to rotate
    # Size needs to accommodate the largest rotating part (number area outer radius)
    wheel_surf_size = int(num_outer_r * 2) + 4 # Add padding for anti-aliasing/rotation artifacts
    wheel_surf = pygame.Surface((wheel_surf_size, wheel_surf_size), pygame.SRCALPHA)
    wheel_center_on_surf = wheel_surf_size // 2 # Center of the wheel surface

    number_font = fonts.get('pay_table') # Use a smaller font for numbers on wheel
    if not number_font: number_font = get_font(16)

    # Get flashing state
    is_flashing = game_state.get('winning_slot_flash_active', False)
    is_flash_visible = game_state.get('winning_slot_flash_visible', True)

    # --- Draw Rotating Wheel Parts (Number Area, Hub) onto wheel_surf ---
    # Number Area Base (Dark Green/Black) - Draw as a filled ring (ellipse minus inner ellipse)
    draw_ellipse(wheel_surf, colors.DARK_GREEN, (wheel_center_on_surf, wheel_center_on_surf), num_outer_r, num_outer_r * perspective)

    for i, number in enumerate(layout_roulette.ROULETTE_WHEEL_NUMBERS):
        start_angle_deg = i * angle_per_slot
        end_angle_deg = (i + 1) * angle_per_slot
        color = get_number_color(number)

        # --- Flashing Logic ---
        is_winning_slot = (number == winning_number and spin_timer == 0) # Only flash when stopped
        current_color = color
        border_thickness = 1 # Default border
        border_color = colors.GOLD

        # Only flash when the wheel is stopped (spin_timer == 0)
        if spin_timer == 0 and is_winning_slot and is_flashing:
            if is_flash_visible:
                # Highlight when flash is visible (e.g., bright yellow border)
                border_thickness = 3
                border_color = colors.ROULETTE_FLASH_COLOR
            else:
                 pass # Draw normally when not visible during flash cycle

        # --- Draw Wedge ---
        # Calculate points for the outer and inner arcs of the wedge
        outer_points = []
        inner_points = []
        steps = 10 # More steps for smoother arc
        for j in range(steps + 1):
            angle = math.radians(start_angle_deg + (end_angle_deg - start_angle_deg) * j / steps - 90)
            # Outer arc points
            outer_x = wheel_center_on_surf + num_outer_r * math.cos(angle)
            outer_y = wheel_center_on_surf + num_outer_r * perspective * math.sin(angle)
            outer_points.append((outer_x, outer_y))
            # Inner arc points (calculate in reverse order for polygon)
            inner_x = wheel_center_on_surf + num_inner_r * math.cos(angle)
            inner_y = wheel_center_on_surf + num_inner_r * perspective * math.sin(angle)
            inner_points.insert(0, (inner_x, inner_y)) # Insert at beginning

        # Combine points: outer arc, then inner arc
        wedge_points = outer_points + inner_points
        if len(wedge_points) >= 3: # Need at least 3 points to draw polygon
            pygame.draw.polygon(wheel_surf, current_color, wedge_points)

            # Draw Dividers (borders of the wedge)
            # Draw the two radial lines
            if len(outer_points) > 0 and len(inner_points) > 0:
                pygame.draw.line(wheel_surf, border_color, outer_points[0], inner_points[-1], border_thickness)
                pygame.draw.line(wheel_surf, border_color, outer_points[-1], inner_points[0], border_thickness)
            # Draw the outer and inner arcs (optional, can make dividers thicker)
            # pygame.draw.lines(wheel_surf, border_color, False, outer_points, border_thickness)
            # pygame.draw.lines(wheel_surf, border_color, False, inner_points, border_thickness)

        # Draw number text (rotated and positioned on ellipse)
        text_angle_deg = start_angle_deg + angle_per_slot / 2
        # Position calculation based on average radius
        text_radius_x = (num_outer_r + num_inner_r) / 2
        text_angle_rad = math.radians(text_angle_deg - 90)
        text_x = wheel_center_on_surf + text_radius_x * math.cos(text_angle_rad)
        text_y = wheel_center_on_surf + text_radius_x * perspective * math.sin(text_angle_rad)

        num_surf = number_font.render(str(number), True, colors.WHITE)
        num_surf_rotated = pygame.transform.rotate(num_surf, -text_angle_deg)
        num_rect = num_surf_rotated.get_rect(center=(text_x, text_y))
        wheel_surf.blit(num_surf_rotated, num_rect)

    # --- Draw Center Hub (on wheel_surf before rotation) ---
    hub_base_color = (50, 50, 50) # Dark Grey
    hub_highlight_color = (100, 100, 100) # Lighter Grey
    hub_pin_color = colors.GOLD

    draw_ellipse(wheel_surf, hub_base_color, (wheel_center_on_surf, wheel_center_on_surf), hub_r, hub_r * perspective)
    draw_ellipse(wheel_surf, hub_highlight_color, (wheel_center_on_surf, wheel_center_on_surf), hub_r * 0.8, hub_r * 0.8 * perspective)
    draw_ellipse(wheel_surf, hub_pin_color, (wheel_center_on_surf, wheel_center_on_surf), hub_r * 0.5, hub_r * 0.5 * perspective)
    draw_ellipse(wheel_surf, colors.BLACK, (wheel_center_on_surf, wheel_center_on_surf), hub_r * 0.3, hub_r * 0.3 * perspective)

    # Blit the stationary wheel surface onto the main surface
    wheel_rect = wheel_surf.get_rect(center=center_pos)
    surface.blit(wheel_surf, wheel_rect)

    # --- Draw Ball ---
    # Calculate ball position based on its angle and radius (relative to screen center)
    # Ball angle is now absolute
    effective_ball_angle_deg = ball_current_angle
    ball_angle_rad = math.radians(effective_ball_angle_deg - 90) # Adjust for Pygame coordinates
    ball_x = center_pos[0] + ball_current_radius_x * math.cos(ball_angle_rad)
    ball_y = center_pos[1] + ball_current_radius_y * math.sin(ball_angle_rad) # Use perspective radius

    # Draw shadow first
    shadow_pos = (ball_x + layout_roulette.BALL_SHADOW_OFFSET, ball_y + layout_roulette.BALL_SHADOW_OFFSET)
    pygame.draw.circle(surface, layout_roulette.BALL_SHADOW_COLOR, shadow_pos, layout_roulette.BALL_RADIUS)
    # Draw ball
    pygame.draw.circle(surface, layout_roulette.BALL_COLOR, (ball_x, ball_y), layout_roulette.BALL_RADIUS)

    # --- Draw Pointer ---
    pointer_size = 20
    # Position pointer above the outer rim
    pointer_tip_y = center_pos[1] - rim_outer_r * perspective - 5 # Y-coord based on perspective radius
    pointer_points = [
        (center_pos[0], pointer_tip_y), # Tip
        (center_pos[0] - pointer_size // 2, pointer_tip_y - pointer_size), # Bottom left
        (center_pos[0] + pointer_size // 2, pointer_tip_y - pointer_size), # Bottom right
    ]
    pygame.draw.polygon(surface, colors.GOLD, pointer_points)

    # Display winning number text only when wheel is stopped (pause phase)
    if spin_timer == 0 and pause_timer > 0: # Show during pause/flash phase
         win_text = f"Result: {winning_number}"
         draw_text(surface, win_text, fonts['result'], center_pos[0], center_pos[1] + rim_outer_r + 40, colors.YELLOW, center=True)

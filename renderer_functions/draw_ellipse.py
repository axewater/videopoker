# /renderer_functions/draw_ellipse.py
# NEW FILE
import pygame
import math
from typing import Tuple

def draw_ellipse(surface: pygame.Surface, color: Tuple[int, int, int], center: Tuple[int, int], radius_x: float, radius_y: float, steps: int = 60):
    """
    Draws a filled ellipse using a polygon approximation.

    Args:
        surface: The Pygame surface to draw on.
        color: The color of the ellipse (RGB tuple).
        center: The center coordinates (x, y) of the ellipse.
        radius_x: The horizontal radius.
        radius_y: The vertical radius.
        steps: The number of points used to approximate the ellipse boundary. More steps = smoother ellipse.
    """
    if radius_x <= 0 or radius_y <= 0:
        return # Cannot draw ellipse with non-positive radius

    points = []
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        x = center[0] + radius_x * math.cos(angle)
        y = center[1] + radius_y * math.sin(angle)
        points.append((x, y))

    if len(points) >= 3: # Need at least 3 points for a polygon
        pygame.draw.polygon(surface, color, points)

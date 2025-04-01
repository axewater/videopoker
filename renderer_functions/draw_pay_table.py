import pygame
from typing import Optional, Dict

import constants
from poker_rules import PAY_TABLE, HandRank
from .get_font import get_font

def draw_pay_table(surface: pygame.Surface, fonts: Dict[str, pygame.font.Font], x: int, y: int, winning_rank: Optional[HandRank] = None):
    """Draws the pay table."""
    pay_table_font = fonts['pay_table']
    line_height = pay_table_font.get_linesize()
    padding = 5
    highlight_color = constants.YELLOW
    background_color = constants.BLACK
    text_color = constants.WHITE
    title_color = constants.GOLD
    colon_color = constants.WHITE # Color for the colon separator
    colon_str = ":"

    # Sort ranks by payout (highest first)
    sorted_ranks = sorted([rank for rank in PAY_TABLE if PAY_TABLE[rank][1] > 0],
                          key=lambda k: PAY_TABLE[k][1], reverse=True)

    # Prepare title
    # Use get_font directly here as it's a helper within the original class logic
    title_font = get_font(constants.PAY_TABLE_FONT_SIZE + 2)
    title_text = "--- Pay Table (Bet: 1) ---"
    title_surf = title_font.render(title_text, True, title_color)
    title_width = title_surf.get_width()
    current_y = y + line_height * 1.5 # Start below title

    # Prepare text surfaces and calculate dimensions
    name_surfaces = []
    payout_surfaces = []
    max_name_width = 0
    max_payout_width = 0

    for rank in sorted_ranks:
        name, payout = PAY_TABLE[rank]
        name_surf = pay_table_font.render(name, True, text_color)
        payout_str = f"{payout}x"
        payout_surf = pay_table_font.render(payout_str, True, text_color)

        name_surfaces.append((rank, name_surf)) # Store rank with surface
        payout_surfaces.append(payout_surf)

        max_name_width = max(max_name_width, name_surf.get_width())
        max_payout_width = max(max_payout_width, payout_surf.get_width())

    # Render colon separately for precise alignment
    colon_surf = pay_table_font.render(colon_str, True, colon_color)
    colon_width = colon_surf.get_width()
    column_spacing = 5 # Space around the colon

    # Calculate total width and height for background
    total_content_width = max_name_width + column_spacing + colon_width + column_spacing + max_payout_width
    max_width = max(title_width, total_content_width)
    total_height = (line_height * 1.5) + (len(sorted_ranks) * line_height) # Title + entries

    # Draw background rectangle
    bg_rect = pygame.Rect(x - padding, y - padding, max_width + 2 * padding, total_height + 2 * padding)
    pygame.draw.rect(surface, background_color, bg_rect, border_radius=5)

    # Draw title
    surface.blit(title_surf, (x, y))

    # Draw each winning hand
    for i, (rank, name_surface) in enumerate(name_surfaces):
        payout_surface = payout_surfaces[i]

        # Calculate positions
        name_x = x
        colon_x = x + max_name_width + column_spacing
        payout_x = colon_x + colon_width + column_spacing

        if rank == winning_rank: # Check if this is the winning hand
            highlight_rect = pygame.Rect(x - padding // 2, current_y - padding // 2, max_width + padding, line_height + padding // 2)
            pygame.draw.rect(surface, highlight_color, highlight_rect, width=2, border_radius=3) # Draw border

        # Draw components: Name (left-aligned), Colon, Payout (left-aligned in its column)
        surface.blit(name_surface, (name_x, current_y))
        surface.blit(colon_surf, (colon_x, current_y))
        surface.blit(payout_surface, (payout_x, current_y))

        current_y += line_height # Move down for the next line

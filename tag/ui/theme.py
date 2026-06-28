from __future__ import annotations

import pygame

from tag.utils.text import draw_text


COLORS = {
    "bg": (6, 10, 20),
    "bg_2": (10, 16, 30),
    "surface": (15, 23, 42),
    "surface_2": (22, 33, 54),
    "surface_3": (30, 41, 59),
    "border": (55, 70, 96),
    "border_soft": (34, 48, 72),
    "text": (248, 250, 252),
    "text_soft": (203, 213, 225),
    "muted": (148, 163, 184),
    "primary": (59, 130, 246),
    "primary_light": (147, 197, 253),
    "gold": (248, 199, 88),
    "success": (74, 222, 128),
    "danger": (248, 113, 113),
    "warning": (251, 191, 36),
    "shadow": (2, 6, 23),
}


def with_alpha(color: tuple[int, int, int], alpha: int) -> tuple[int, int, int, int]:
    return (*color, alpha)


def draw_cinematic_background(surface: pygame.Surface) -> None:
    width, height = surface.get_size()
    surface.fill(COLORS["bg"])

    top = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 4):
        ratio = y / max(1, height)
        color = (
            8 + int(12 * ratio),
            14 + int(10 * ratio),
            28 + int(18 * ratio),
            255,
        )
        pygame.draw.rect(top, color, pygame.Rect(0, y, width, 4))
    surface.blit(top, (0, 0))

    grid_color = (31, 42, 66)
    for x in range(-80, width + 80, 96):
        pygame.draw.line(surface, grid_color, (x, 0), (x + height // 3, height), 1)
    for y in range(80, height, 78):
        pygame.draw.line(surface, (21, 31, 52), (0, y), (width, y), 1)


def draw_vignette(surface: pygame.Surface, strength: int = 95) -> None:
    width, height = surface.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, strength), overlay.get_rect(), width=max(32, width // 12))
    surface.blit(overlay, (0, 0))


def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    *,
    fill: tuple[int, int, int] | None = None,
    border: tuple[int, int, int] | None = None,
    radius: int = 18,
    width: int = 1,
    glow: tuple[int, int, int] | None = None,
) -> None:
    if glow is not None:
        for grow, alpha in ((10, 32), (5, 52)):
            glow_rect = rect.inflate(grow, grow)
            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, with_alpha(glow, alpha), glow_surface.get_rect(), border_radius=radius + grow // 2)
            surface.blit(glow_surface, glow_rect.topleft)

    shadow_rect = rect.move(0, 5)
    shadow = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shadow, with_alpha(COLORS["shadow"], 95), shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, shadow_rect.topleft)

    pygame.draw.rect(surface, fill or COLORS["surface"], rect, border_radius=radius)
    pygame.draw.rect(surface, border or COLORS["border_soft"], rect, width, border_radius=radius)


def draw_divider(surface: pygame.Surface, rect: pygame.Rect, y: int) -> None:
    pygame.draw.line(surface, COLORS["border_soft"], (rect.left + 18, y), (rect.right - 18, y), 1)


def draw_pill(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    pos: tuple[int, int],
    *,
    fg: tuple[int, int, int] | None = None,
    bg: tuple[int, int, int] | None = None,
    border: tuple[int, int, int] | None = None,
    center: bool = False,
) -> pygame.Rect:
    padding_x = 12
    padding_y = 6
    text_size = font.size(text)
    rect = pygame.Rect(0, 0, text_size[0] + padding_x * 2, text_size[1] + padding_y * 2)
    if center:
        rect.center = pos
    else:
        rect.topleft = pos

    pygame.draw.rect(surface, bg or COLORS["surface_2"], rect, border_radius=rect.height // 2)
    pygame.draw.rect(surface, border or COLORS["border_soft"], rect, 1, border_radius=rect.height // 2)
    draw_text(surface, font, text, fg or COLORS["text_soft"], rect.center, center=True)
    return rect


def draw_button(surface: pygame.Surface, font: pygame.font.Font, rect: pygame.Rect, text: str, active: bool) -> None:
    fill = COLORS["primary"] if active else COLORS["surface_3"]
    border = COLORS["primary_light"] if active else COLORS["border"]
    text_color = COLORS["text"] if active else COLORS["text_soft"]
    draw_panel(surface, rect, fill=fill, border=border, radius=14, width=2, glow=COLORS["primary"] if active else None)
    draw_text(surface, font, text, text_color, rect.center, center=True)


def draw_progress_bar(
    surface: pygame.Surface,
    rect: pygame.Rect,
    progress: float,
    *,
    fill: tuple[int, int, int] | None = None,
    bg: tuple[int, int, int] | None = None,
) -> None:
    progress = max(0.0, min(1.0, progress))
    pygame.draw.rect(surface, bg or COLORS["surface_3"], rect, border_radius=rect.height // 2)
    fill_rect = rect.copy()
    fill_rect.width = max(0, int(rect.width * progress))
    if fill_rect.width > 0:
        pygame.draw.rect(surface, fill or COLORS["primary"], fill_rect, border_radius=rect.height // 2)
    pygame.draw.rect(surface, COLORS["border"], rect, 1, border_radius=rect.height // 2)

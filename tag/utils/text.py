from __future__ import annotations

import pygame


def draw_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    pos: tuple[int, int],
    center: bool = False,
) -> pygame.Rect:
    image = font.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(image, rect)
    return rect


def draw_wrapped_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    rect: pygame.Rect,
    line_spacing: int = 3,
) -> None:
    """Draw small menu text inside a fixed rectangle."""
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        test = word if not current else f"{current} {word}"
        if font.size(test)[0] <= rect.width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    y = rect.top
    for line in lines:
        if y + font.get_height() > rect.bottom:
            break
        image = font.render(line, True, color)
        line_rect = image.get_rect(centerx=rect.centerx, top=y)
        surface.blit(image, line_rect)
        y += font.get_height() + line_spacing


def draw_wrapped_text_left(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    rect: pygame.Rect,
    line_spacing: int = 3,
) -> int:
    """Draw wrapped HUD text from the left edge and return the next y position."""
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        test = word if not current else f"{current} {word}"
        if font.size(test)[0] <= rect.width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    y = rect.top
    for line in lines:
        if y + font.get_height() > rect.bottom:
            break
        image = font.render(line, True, color)
        surface.blit(image, (rect.left, y))
        y += font.get_height() + line_spacing

    return y

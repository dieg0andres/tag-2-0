from __future__ import annotations

import pygame


def ellipsize(font: pygame.font.Font, text: str, max_width: int) -> str:
    if font.size(text)[0] <= max_width:
        return text

    suffix = "..."
    if font.size(suffix)[0] > max_width:
        return ""

    trimmed = text
    while trimmed and font.size(trimmed + suffix)[0] > max_width:
        trimmed = trimmed[:-1].rstrip()
    return trimmed + suffix


def wrap_lines(
    font: pygame.font.Font,
    text: str,
    max_width: int,
    max_lines: int | None = None,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        test = word if not current else f"{current} {word}"
        if font.size(test)[0] <= max_width:
            current = test
            continue

        if current:
            lines.append(current)
        current = word

        if max_lines is not None and len(lines) >= max_lines:
            break

    if current and (max_lines is None or len(lines) < max_lines):
        lines.append(current)

    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]

    return lines


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
) -> int:
    """Draw small menu text inside a fixed rectangle."""
    lines = wrap_lines(font, text, rect.width)

    y = rect.top
    for line in lines:
        if y + font.get_height() > rect.bottom:
            break
        image = font.render(line, True, color)
        line_rect = image.get_rect(centerx=rect.centerx, top=y)
        surface.blit(image, line_rect)
        y += font.get_height() + line_spacing
    return y


def draw_wrapped_text_left(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    rect: pygame.Rect,
    line_spacing: int = 3,
    max_lines: int | None = None,
    overflow_text: str = "+ more",
) -> int:
    """Draw wrapped HUD text from the left edge and return the next y position."""
    all_lines = wrap_lines(font, text, rect.width)
    lines = all_lines
    clipped = False
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        clipped = True

    y = rect.top
    for index, line in enumerate(lines):
        if y + font.get_height() > rect.bottom:
            clipped = True
            break
        if clipped and index == len(lines) - 1:
            line = ellipsize(font, f"{line} {overflow_text}", rect.width)
        image = font.render(line, True, color)
        surface.blit(image, (rect.left, y))
        y += font.get_height() + line_spacing

    return y

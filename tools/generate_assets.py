from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame


ROOT_DIR = Path(__file__).resolve().parents[1]
SPRITE_DIR = ROOT_DIR / "assets" / "sprites"
SIZE = 64


def make_surface() -> pygame.Surface:
    return pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)


def draw_outline_rect(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int] = (28, 31, 38),
    radius: int = 8,
) -> None:
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, outline, rect, 2, border_radius=radius)


def save_if_missing(filename: str, surface: pygame.Surface) -> None:
    SPRITE_DIR.mkdir(parents=True, exist_ok=True)
    path = SPRITE_DIR / filename
    if path.exists():
        print(f"Skipped existing {path}")
        return
    pygame.image.save(surface, str(path))
    print(f"Created {path}")


def generate_revenge_bot() -> pygame.Surface:
    """Ducky reference: yellow lab-duck body, white eyes, orange beak, scars, blade."""
    sprite = make_surface()

    yellow = (237, 211, 50)
    yellow_dark = (190, 159, 36)
    outline = (43, 45, 51)
    orange = (232, 136, 47)
    red = (181, 57, 64)

    pygame.draw.ellipse(sprite, yellow_dark, pygame.Rect(15, 4, 34, 28))
    pygame.draw.ellipse(sprite, yellow, pygame.Rect(13, 3, 36, 30))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(13, 3, 36, 30), 2)

    draw_outline_rect(sprite, pygame.Rect(17, 25, 30, 28), yellow, outline, 9)

    for x in (23, 39):
        pygame.draw.ellipse(sprite, (238, 238, 226), pygame.Rect(x, 12, 7, 12))
        pygame.draw.ellipse(sprite, outline, pygame.Rect(x, 12, 7, 12), 1)
    pygame.draw.ellipse(sprite, orange, pygame.Rect(25, 24, 15, 7))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(25, 24, 15, 7), 1)

    pygame.draw.polygon(sprite, yellow, [(27, 2), (31, 0), (34, 7), (38, 0), (42, 6)])
    pygame.draw.line(sprite, outline, (29, 3), (32, 8), 1)
    pygame.draw.line(sprite, outline, (37, 3), (35, 8), 1)

    pygame.draw.line(sprite, yellow_dark, (18, 34), (8, 45), 4)
    pygame.draw.circle(sprite, yellow, (8, 46), 4)
    pygame.draw.line(sprite, yellow_dark, (46, 33), (56, 18), 4)
    pygame.draw.circle(sprite, yellow, (56, 18), 4)
    pygame.draw.line(sprite, (196, 200, 204), (54, 17), (62, 7), 4)
    pygame.draw.line(sprite, outline, (54, 17), (62, 7), 1)

    pygame.draw.rect(sprite, red, pygame.Rect(38, 39, 7, 8), border_radius=2)
    pygame.draw.line(sprite, (235, 229, 217), (39, 42), (44, 40), 2)
    pygame.draw.line(sprite, (83, 86, 94), (20, 53), (45, 53), 2)
    pygame.draw.circle(sprite, (112, 116, 123), (31, 53), 3)

    pygame.draw.line(sprite, yellow_dark, (24, 52), (20, 62), 4)
    pygame.draw.line(sprite, yellow_dark, (40, 52), (44, 62), 4)
    pygame.draw.ellipse(sprite, orange, pygame.Rect(13, 58, 15, 6))
    pygame.draw.ellipse(sprite, orange, pygame.Rect(37, 58, 15, 6))

    return sprite


def generate_subslasher() -> pygame.Surface:
    """Subslasher reference: blue-purple body, large pale eyes, grin, pink popsicle sword."""
    sprite = make_surface()

    blue = (91, 135, 166)
    blue_dark = (51, 88, 122)
    purple = (105, 84, 190)
    outline = (41, 45, 55)
    pink = (221, 117, 145)
    cream = (236, 216, 183)

    pygame.draw.ellipse(sprite, blue, pygame.Rect(14, 5, 38, 30))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(14, 5, 38, 30), 2)
    draw_outline_rect(sprite, pygame.Rect(18, 28, 29, 27), blue, outline, 6)

    pygame.draw.ellipse(sprite, (232, 229, 214), pygame.Rect(23, 14, 7, 12))
    pygame.draw.ellipse(sprite, (232, 229, 214), pygame.Rect(38, 14, 7, 12))
    pygame.draw.arc(sprite, outline, pygame.Rect(22, 20, 26, 15), 0.15, 2.9, 2)

    pygame.draw.polygon(sprite, blue_dark, [(31, 30), (36, 30), (41, 51), (24, 51)])
    pygame.draw.line(sprite, (38, 74, 105), (33, 31), (33, 51), 2)
    for y in (36, 43, 50):
        pygame.draw.arc(sprite, (44, 77, 108), pygame.Rect(22, y, 24, 9), 0, 3.14, 1)

    pygame.draw.line(sprite, blue_dark, (18, 36), (8, 48), 4)
    pygame.draw.circle(sprite, blue, (8, 49), 5)
    pygame.draw.line(sprite, blue_dark, (47, 34), (58, 47), 4)
    pygame.draw.circle(sprite, blue, (58, 48), 5)

    pygame.draw.line(sprite, cream, (15, 11), (5, 4), 5)
    pygame.draw.ellipse(sprite, pink, pygame.Rect(0, 0, 25, 17))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(0, 0, 25, 17), 2)
    pygame.draw.line(sprite, (178, 72, 99), (5, 8), (20, 8), 1)

    pygame.draw.line(sprite, blue_dark, (25, 54), (22, 63), 4)
    pygame.draw.line(sprite, blue_dark, (40, 54), (43, 63), 4)
    pygame.draw.ellipse(sprite, purple, pygame.Rect(17, 59, 13, 6))
    pygame.draw.ellipse(sprite, purple, pygame.Rect(37, 59, 13, 6))

    return sprite


def generate_survivor() -> pygame.Surface:
    """Survivor reference: runner pose, dark shirt/hair, light shorts, blue readable marker."""
    sprite = make_surface()

    blue = (59, 130, 246)
    blue_dark = (30, 64, 175)
    skin = (179, 113, 74)
    hair = (30, 25, 22)
    shirt = (21, 25, 32)
    shorts = (184, 196, 208)
    outline = (31, 41, 55)

    pygame.draw.ellipse(sprite, (37, 99, 235, 88), pygame.Rect(7, 7, 50, 50))

    pygame.draw.circle(sprite, skin, (33, 13), 9)
    pygame.draw.polygon(sprite, hair, [(25, 11), (31, 4), (43, 8), (39, 15), (29, 16)])
    pygame.draw.circle(sprite, outline, (33, 13), 9, 2)

    draw_outline_rect(sprite, pygame.Rect(23, 21, 23, 20), shirt, outline, 5)
    pygame.draw.rect(sprite, shorts, pygame.Rect(24, 39, 21, 10), border_radius=3)
    pygame.draw.rect(sprite, outline, pygame.Rect(24, 39, 21, 10), 1, border_radius=3)

    pygame.draw.line(sprite, skin, (24, 27), (11, 35), 4)
    pygame.draw.circle(sprite, skin, (10, 35), 4)
    pygame.draw.line(sprite, skin, (45, 27), (55, 18), 4)
    pygame.draw.circle(sprite, skin, (56, 17), 4)

    pygame.draw.line(sprite, skin, (28, 48), (18, 60), 4)
    pygame.draw.line(sprite, skin, (40, 48), (46, 61), 4)
    pygame.draw.ellipse(sprite, blue_dark, pygame.Rect(12, 58, 13, 5))
    pygame.draw.ellipse(sprite, blue_dark, pygame.Rect(41, 58, 13, 5))

    pygame.draw.polygon(sprite, blue, [(31, 18), (35, 18), (37, 25), (29, 25)])
    return sprite


def generate_show_runner() -> pygame.Surface:
    """Show Runner reference: crown, split black/white face, sharp smile, dark half-body."""
    sprite = make_surface()

    outline = (32, 32, 34)
    white = (225, 226, 218)
    black = (28, 29, 31)
    crown = (218, 220, 210)

    pygame.draw.polygon(
        sprite,
        crown,
        [(18, 10), (20, 0), (27, 8), (33, 0), (39, 8), (47, 1), (45, 14)],
    )
    pygame.draw.lines(
        sprite,
        outline,
        True,
        [(18, 10), (20, 0), (27, 8), (33, 0), (39, 8), (47, 1), (45, 14)],
        2,
    )
    for x in (27, 34, 40):
        pygame.draw.circle(sprite, (150, 150, 145), (x, 9), 2)

    pygame.draw.ellipse(sprite, white, pygame.Rect(16, 9, 34, 32))
    pygame.draw.polygon(sprite, black, [(33, 10), (50, 13), (45, 40), (31, 39), (29, 24)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(16, 9, 34, 32), 2)

    pygame.draw.polygon(sprite, black, [(22, 20), (29, 16), (28, 26)])
    pygame.draw.polygon(sprite, white, [(39, 19), (45, 16), (43, 27)])
    pygame.draw.arc(sprite, outline, pygame.Rect(25, 23, 22, 15), 0.2, 3.0, 2)
    for x in range(29, 44, 5):
        pygame.draw.polygon(sprite, white, [(x, 29), (x + 3, 31), (x, 34)])

    pygame.draw.polygon(sprite, white, [(20, 38), (31, 37), (30, 57), (15, 59)])
    pygame.draw.polygon(sprite, black, [(31, 37), (45, 38), (50, 58), (30, 57)])
    pygame.draw.line(sprite, outline, (31, 36), (31, 58), 2)
    pygame.draw.lines(sprite, outline, False, [(15, 58), (20, 38), (31, 37), (45, 38), (50, 58)], 2)

    pygame.draw.line(sprite, white, (20, 41), (7, 49), 5)
    pygame.draw.line(sprite, outline, (20, 41), (7, 49), 2)
    pygame.draw.line(sprite, black, (45, 41), (58, 49), 5)
    pygame.draw.line(sprite, outline, (45, 41), (58, 49), 2)
    pygame.draw.line(sprite, white, (25, 57), (21, 64), 5)
    pygame.draw.line(sprite, black, (39, 57), (43, 64), 5)

    return sprite


def generate_malice() -> pygame.Surface:
    """Malice reference: blue clawed body, gray shark head, red eyes, sharp teeth."""
    sprite = make_surface()

    outline = (48, 53, 56)
    blue = (72, 156, 205)
    blue_dark = (34, 104, 153)
    gray = (190, 194, 190)
    red = (202, 42, 30)
    yellow = (221, 191, 61)
    brown = (139, 90, 48)

    pygame.draw.polygon(sprite, gray, [(25, 12), (55, 18), (59, 37), (47, 53), (27, 49), (18, 32)])
    pygame.draw.polygon(sprite, outline, [(25, 12), (55, 18), (59, 37), (47, 53), (27, 49), (18, 32)], 2)
    pygame.draw.polygon(sprite, (235, 238, 232), [(27, 35), (54, 35), (48, 48), (32, 47)])
    pygame.draw.arc(sprite, outline, pygame.Rect(26, 27, 29, 22), 0.0, 3.0, 2)
    for x in range(30, 52, 5):
        pygame.draw.polygon(sprite, outline, [(x, 36), (x + 3, 39), (x, 42)])

    pygame.draw.polygon(sprite, red, [(34, 23), (40, 20), (42, 28)])
    pygame.draw.polygon(sprite, red, [(50, 24), (56, 22), (55, 30)])
    pygame.draw.circle(sprite, yellow, (37, 25), 4, 1)
    pygame.draw.circle(sprite, yellow, (53, 26), 4, 1)

    pygame.draw.polygon(sprite, blue, [(17, 26), (28, 20), (30, 53), (18, 58), (11, 43)])
    pygame.draw.line(sprite, outline, (18, 26), (29, 52), 2)
    pygame.draw.polygon(sprite, brown, [(29, 41), (38, 50), (30, 55), (24, 47)])
    pygame.draw.line(sprite, outline, (23, 47), (36, 52), 1)

    pygame.draw.line(sprite, blue_dark, (17, 34), (7, 47), 5)
    pygame.draw.line(sprite, outline, (17, 34), (7, 47), 1)
    pygame.draw.line(sprite, blue_dark, (20, 28), (9, 9), 5)
    pygame.draw.circle(sprite, blue, (9, 8), 5)
    pygame.draw.circle(sprite, (235, 238, 232), (7, 8), 2)
    pygame.draw.line(sprite, blue_dark, (30, 50), (27, 63), 5)
    pygame.draw.line(sprite, blue_dark, (46, 50), (48, 63), 5)
    for claw in [(3, 50), (8, 52), (27, 63), (47, 63)]:
        pygame.draw.line(sprite, yellow, claw, (claw[0] + 2, claw[1] - 5), 2)

    return sprite


def generate_vengance_bot() -> pygame.Surface:
    """Vengance Bot reference: gray box head, red eyes, green mark, thin robot body."""
    sprite = make_surface()

    outline = (38, 41, 43)
    gray = (128, 130, 125)
    gray_dark = (75, 78, 78)
    red = (199, 35, 29)
    green = (26, 137, 68)
    orange = (186, 112, 49)

    pygame.draw.polygon(sprite, gray, [(13, 7), (53, 6), (57, 27), (11, 28)])
    pygame.draw.polygon(sprite, outline, [(13, 7), (53, 6), (57, 27), (11, 28)], 2)
    pygame.draw.rect(sprite, gray_dark, pygame.Rect(21, 15, 9, 9), border_radius=2)
    pygame.draw.polygon(sprite, red, [(36, 13), (44, 10), (42, 19)])
    pygame.draw.polygon(sprite, red, [(47, 14), (55, 12), (53, 21)])
    pygame.draw.line(sprite, green, (44, 20), (53, 17), 3)

    draw_outline_rect(sprite, pygame.Rect(23, 27, 22, 31), gray, outline, 4)
    for x in range(26, 43, 5):
        pygame.draw.line(sprite, gray_dark, (x, 29), (x + 5, 56), 1)
    pygame.draw.rect(sprite, orange, pygame.Rect(23, 50, 8, 7), border_radius=2)
    pygame.draw.line(sprite, green, (25, 53), (29, 56), 1)

    pygame.draw.line(sprite, gray_dark, (24, 34), (8, 45), 4)
    pygame.draw.line(sprite, gray_dark, (44, 34), (59, 22), 4)
    pygame.draw.line(sprite, outline, (24, 34), (8, 45), 1)
    pygame.draw.line(sprite, outline, (44, 34), (59, 22), 1)
    pygame.draw.rect(sprite, gray, pygame.Rect(4, 42, 8, 5), border_radius=2)
    pygame.draw.rect(sprite, gray, pygame.Rect(56, 19, 7, 5), border_radius=2)

    pygame.draw.line(sprite, gray_dark, (28, 57), (27, 64), 4)
    pygame.draw.line(sprite, gray_dark, (40, 57), (41, 64), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(22, 60, 11, 4), border_radius=1)
    pygame.draw.rect(sprite, gray, pygame.Rect(37, 60, 11, 4), border_radius=1)

    return sprite


def main() -> None:
    pygame.init()
    save_if_missing("revenge_bot.png", generate_revenge_bot())
    save_if_missing("subslasher.png", generate_subslasher())
    save_if_missing("show_runner.png", generate_show_runner())
    save_if_missing("malice.png", generate_malice())
    save_if_missing("vengance_bot.png", generate_vengance_bot())
    save_if_missing("survivor.png", generate_survivor())
    pygame.quit()


if __name__ == "__main__":
    main()

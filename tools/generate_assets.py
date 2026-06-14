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


def generate_ducky_fried_chicken() -> pygame.Surface:
    """Fried Chicken skin reference: brown Ducky body, pale eyes, open mouth, mace belt."""
    sprite = make_surface()

    brown = (126, 91, 65)
    brown_dark = (80, 58, 45)
    tan = (172, 148, 118)
    cream = (226, 228, 213)
    outline = (45, 48, 50)

    pygame.draw.ellipse(sprite, tan, pygame.Rect(14, 4, 36, 30))
    pygame.draw.ellipse(sprite, brown, pygame.Rect(13, 3, 37, 31))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(13, 3, 37, 31), 2)
    draw_outline_rect(sprite, pygame.Rect(17, 26, 31, 28), brown, outline, 9)

    pygame.draw.ellipse(sprite, cream, pygame.Rect(23, 12, 8, 11))
    pygame.draw.ellipse(sprite, cream, pygame.Rect(38, 12, 8, 11))
    pygame.draw.line(sprite, outline, (27, 15), (27, 20), 1)
    pygame.draw.line(sprite, outline, (42, 15), (42, 20), 1)

    pygame.draw.rect(sprite, (12, 12, 13), pygame.Rect(24, 25, 22, 8), border_radius=4)
    pygame.draw.rect(sprite, cream, pygame.Rect(24, 25, 22, 8), 2, border_radius=4)

    for x in (18, 27, 36, 45):
        pygame.draw.line(sprite, brown_dark, (x, 8), (x + 4, 52), 1)
    pygame.draw.arc(sprite, tan, pygame.Rect(16, 15, 33, 29), 0.1, 2.9, 2)

    pygame.draw.line(sprite, brown_dark, (18, 36), (8, 48), 5)
    pygame.draw.ellipse(sprite, cream, pygame.Rect(1, 45, 11, 13))
    pygame.draw.line(sprite, brown_dark, (47, 34), (57, 18), 5)
    pygame.draw.circle(sprite, brown, (57, 18), 5)
    pygame.draw.line(sprite, (178, 181, 175), (55, 17), (63, 8), 4)
    pygame.draw.line(sprite, outline, (55, 17), (63, 8), 1)

    pygame.draw.line(sprite, cream, (20, 52), (48, 52), 4)
    for x in range(20, 50, 6):
        pygame.draw.circle(sprite, tan, (x, 52), 4)
    pygame.draw.line(sprite, brown_dark, (20, 56), (47, 55), 2)
    pygame.draw.circle(sprite, tan, (35, 56), 5)

    pygame.draw.line(sprite, brown_dark, (25, 53), (20, 63), 5)
    pygame.draw.line(sprite, brown_dark, (41, 53), (46, 63), 5)
    pygame.draw.ellipse(sprite, cream, pygame.Rect(12, 59, 16, 6))
    pygame.draw.ellipse(sprite, cream, pygame.Rect(39, 59, 16, 6))

    return sprite


def generate_ducky_inverted() -> pygame.Surface:
    """Inverted Ducky skin: blue Ducky body, green beak/shoes, black eyes, twin blades."""
    sprite = make_surface()

    outline = (43, 45, 51)
    blue = (116, 144, 189)
    blue_dark = (69, 96, 150)
    green = (107, 120, 70)
    pale = (212, 221, 220)

    pygame.draw.ellipse(sprite, pale, pygame.Rect(13, 3, 37, 31))
    pygame.draw.ellipse(sprite, blue, pygame.Rect(13, 3, 37, 31))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(13, 3, 37, 31), 2)
    draw_outline_rect(sprite, pygame.Rect(17, 26, 31, 28), blue, outline, 9)
    pygame.draw.ellipse(sprite, outline, pygame.Rect(24, 13, 5, 10))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(39, 13, 5, 10))
    pygame.draw.ellipse(sprite, green, pygame.Rect(25, 25, 17, 6))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(25, 25, 17, 6), 1)
    pygame.draw.line(sprite, blue_dark, (18, 36), (7, 47), 5)
    pygame.draw.line(sprite, blue_dark, (47, 35), (58, 24), 5)
    pygame.draw.circle(sprite, blue, (8, 47), 5)
    pygame.draw.circle(sprite, blue, (57, 24), 5)
    pygame.draw.line(sprite, green, (6, 47), (0, 54), 4)
    pygame.draw.line(sprite, green, (58, 24), (64, 17), 4)
    for x in (20, 33, 44):
        pygame.draw.line(sprite, pale, (x, 7), (x + 3, 51), 1)
    pygame.draw.line(sprite, blue_dark, (25, 53), (21, 63), 5)
    pygame.draw.line(sprite, blue_dark, (41, 53), (46, 63), 5)
    pygame.draw.ellipse(sprite, green, pygame.Rect(12, 58, 16, 6))
    pygame.draw.ellipse(sprite, green, pygame.Rect(38, 58, 16, 6))

    return sprite


def generate_ducky_ogel() -> pygame.Surface:
    """Ogel skin: red Ducky body, yellow-white head, blue legs, and axe arm."""
    sprite = make_surface()

    outline = (43, 45, 51)
    yellow = (230, 216, 72)
    cream = (239, 234, 201)
    red = (167, 57, 36)
    red_dark = (114, 43, 36)
    blue = (114, 187, 213)
    gray = (198, 202, 204)

    pygame.draw.ellipse(sprite, cream, pygame.Rect(14, 3, 37, 30))
    pygame.draw.polygon(sprite, yellow, [(16, 18), (22, 7), (30, 29), (38, 8), (48, 29), (17, 31)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(14, 3, 37, 30), 2)
    draw_outline_rect(sprite, pygame.Rect(18, 27, 31, 28), red, outline, 6)
    pygame.draw.line(sprite, red_dark, (19, 34), (7, 45), 5)
    pygame.draw.line(sprite, red_dark, (48, 34), (57, 22), 5)
    pygame.draw.line(sprite, gray, (55, 21), (64, 14), 4)
    pygame.draw.polygon(sprite, gray, [(53, 14), (63, 6), (63, 22)])
    pygame.draw.rect(sprite, red, pygame.Rect(56, 10, 8, 7), border_radius=1)
    pygame.draw.line(sprite, outline, (55, 21), (64, 14), 1)
    for x in (25, 36):
        pygame.draw.line(sprite, blue, (x, 54), (x - 2, 64), 5)
    pygame.draw.line(sprite, blue, (44, 54), (48, 64), 5)
    for x in (23, 34, 45):
        pygame.draw.line(sprite, (231, 238, 238), (x, 56), (x + 1, 63), 1)

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


def generate_subslasher_tennis_dude() -> pygame.Surface:
    """Tennis Dude skin: blue Subslasher with headband, tennis balls, and racket."""
    sprite = make_surface()
    outline = (41, 45, 55)
    blue = (93, 164, 213)
    blue_dark = (49, 106, 151)
    yellow = (229, 210, 53)
    red = (149, 63, 81)

    pygame.draw.ellipse(sprite, blue, pygame.Rect(13, 4, 38, 31))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(13, 4, 38, 31), 2)
    draw_outline_rect(sprite, pygame.Rect(18, 28, 30, 29), blue, outline, 6)
    pygame.draw.rect(sprite, red, pygame.Rect(17, 10, 31, 4), border_radius=2)
    pygame.draw.line(sprite, (235, 238, 232), (19, 12), (46, 12), 1)
    pygame.draw.ellipse(sprite, (238, 238, 229), pygame.Rect(23, 16, 7, 12))
    pygame.draw.ellipse(sprite, (238, 238, 229), pygame.Rect(39, 16, 7, 12))
    pygame.draw.arc(sprite, outline, pygame.Rect(22, 21, 25, 15), 0.2, 2.9, 2)
    pygame.draw.polygon(sprite, blue_dark, [(31, 31), (38, 31), (42, 53), (24, 53)])
    for center in ((24, 36), (39, 50)):
        pygame.draw.circle(sprite, yellow, center, 5)
        pygame.draw.arc(sprite, (245, 246, 218), pygame.Rect(center[0] - 4, center[1] - 4, 8, 8), 1, 5, 1)
    pygame.draw.line(sprite, blue_dark, (47, 34), (58, 27), 4)
    pygame.draw.line(sprite, yellow, (56, 25), (64, 19), 5)
    pygame.draw.circle(sprite, (230, 232, 224), (62, 18), 9)
    pygame.draw.circle(sprite, outline, (62, 18), 9, 2)
    pygame.draw.line(sprite, outline, (56, 18), (64, 18), 1)
    pygame.draw.line(sprite, outline, (62, 10), (62, 26), 1)
    pygame.draw.line(sprite, blue_dark, (24, 55), (22, 64), 4)
    pygame.draw.line(sprite, blue_dark, (41, 55), (44, 64), 4)
    return sprite


def generate_subslasher_pickle_ball_bro() -> pygame.Surface:
    """Pickle Ball Bro skin: Subslasher with yellow headband, paddle, and pickleballs."""
    sprite = make_surface()

    outline = (41, 45, 55)
    blue = (91, 132, 158)
    blue_dark = (50, 88, 118)
    yellow = (221, 204, 70)
    paddle = (232, 225, 213)
    red = (146, 75, 85)

    pygame.draw.ellipse(sprite, blue, pygame.Rect(13, 4, 39, 31))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(13, 4, 39, 31), 2)
    draw_outline_rect(sprite, pygame.Rect(18, 28, 30, 29), blue, outline, 6)
    pygame.draw.rect(sprite, yellow, pygame.Rect(17, 9, 32, 4), border_radius=2)
    pygame.draw.ellipse(sprite, (238, 238, 229), pygame.Rect(23, 15, 7, 12))
    pygame.draw.ellipse(sprite, (238, 238, 229), pygame.Rect(40, 15, 7, 12))
    pygame.draw.arc(sprite, outline, pygame.Rect(22, 21, 26, 15), 0.2, 2.9, 2)
    for center in ((24, 37), (42, 51)):
        pygame.draw.circle(sprite, yellow, center, 5)
        pygame.draw.circle(sprite, outline, center, 5, 1)
        pygame.draw.circle(sprite, outline, (center[0] - 1, center[1]), 1)
        pygame.draw.circle(sprite, outline, (center[0] + 2, center[1] + 1), 1)
    pygame.draw.line(sprite, blue_dark, (47, 35), (57, 27), 4)
    pygame.draw.rect(sprite, (214, 216, 209), pygame.Rect(55, 20, 9, 5), border_radius=1)
    pygame.draw.circle(sprite, paddle, (59, 18), 7)
    pygame.draw.circle(sprite, outline, (59, 18), 7, 2)
    pygame.draw.line(sprite, red, (55, 18), (62, 18), 1)
    pygame.draw.line(sprite, blue_dark, (24, 55), (22, 64), 4)
    pygame.draw.line(sprite, blue_dark, (42, 55), (45, 64), 4)
    return sprite


def generate_show_runner_pack_runner() -> pygame.Surface:
    """Pack Runner skin: crowned split yellow/pink runner with toothy seam and pack cape."""
    sprite = make_surface()
    outline = (35, 36, 39)
    yellow = (226, 201, 49)
    pink = (211, 113, 151)
    white = (231, 232, 224)

    pygame.draw.polygon(sprite, white, [(18, 12), (20, 0), (27, 9), (34, 2), (41, 9), (48, 1), (47, 15)])
    pygame.draw.lines(sprite, outline, True, [(18, 12), (20, 0), (27, 9), (34, 2), (41, 9), (48, 1), (47, 15)], 2)
    for x, color in ((25, (213, 52, 48)), (33, (74, 137, 226)), (41, (238, 205, 44))):
        pygame.draw.circle(sprite, color, (x, 10), 2)
    pygame.draw.ellipse(sprite, yellow, pygame.Rect(15, 10, 35, 31))
    pygame.draw.polygon(sprite, pink, [(33, 10), (50, 13), (47, 40), (31, 41), (30, 25)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(15, 10, 35, 31), 2)
    pygame.draw.line(sprite, white, (32, 12), (32, 41), 2)
    for y in range(15, 39, 5):
        pygame.draw.polygon(sprite, white, [(31, y), (35, y + 2), (31, y + 4)])
    pygame.draw.polygon(sprite, outline, [(22, 22), (29, 17), (28, 28)])
    pygame.draw.ellipse(sprite, white, pygame.Rect(39, 19, 7, 9))
    pygame.draw.arc(sprite, outline, pygame.Rect(21, 27, 25, 12), 0.2, 2.9, 2)
    pygame.draw.polygon(sprite, yellow, [(18, 39), (31, 38), (30, 58), (15, 59)])
    pygame.draw.polygon(sprite, pink, [(31, 38), (47, 39), (51, 58), (30, 58)])
    pygame.draw.polygon(sprite, white, [(47, 43), (64, 49), (49, 54)])
    pygame.draw.line(sprite, yellow, (20, 42), (6, 51), 5)
    pygame.draw.line(sprite, outline, (20, 42), (6, 51), 2)
    pygame.draw.line(sprite, yellow, (25, 58), (20, 64), 5)
    pygame.draw.line(sprite, pink, (40, 58), (44, 64), 5)
    return sprite


def generate_show_runner_maldin_inverted() -> pygame.Surface:
    """Maldin Inverted skin: split blue-green Show Runner with jagged seam and antenna."""
    sprite = make_surface()

    outline = (35, 39, 42)
    blue = (87, 116, 190)
    green = (91, 113, 69)
    pale = (228, 231, 220)

    pygame.draw.line(sprite, outline, (31, 8), (31, 0), 2)
    pygame.draw.line(sprite, outline, (33, 8), (40, 3), 2)
    pygame.draw.circle(sprite, pale, (43, 4), 4)
    pygame.draw.circle(sprite, blue, (41, 4), 2)
    pygame.draw.circle(sprite, green, (45, 4), 2)
    pygame.draw.ellipse(sprite, blue, pygame.Rect(15, 7, 36, 32))
    pygame.draw.polygon(sprite, green, [(33, 8), (51, 12), (48, 39), (32, 39)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(15, 7, 36, 32), 2)
    for y in range(10, 39, 5):
        pygame.draw.polygon(sprite, pale, [(31, y), (35, y + 2), (31, y + 4)])
    pygame.draw.polygon(sprite, blue, [(23, 21), (30, 17), (29, 28)])
    pygame.draw.arc(sprite, outline, pygame.Rect(24, 25, 23, 13), 0.2, 2.9, 2)
    for x in range(31, 45, 5):
        pygame.draw.polygon(sprite, pale, [(x, 30), (x + 3, 32), (x, 35)])
    pygame.draw.polygon(sprite, blue, [(19, 38), (32, 38), (31, 59), (15, 60)])
    pygame.draw.polygon(sprite, green, [(32, 38), (47, 39), (51, 59), (31, 59)])
    pygame.draw.line(sprite, outline, (32, 37), (32, 60), 2)
    pygame.draw.line(sprite, blue, (19, 43), (7, 51), 5)
    pygame.draw.line(sprite, green, (47, 43), (59, 51), 5)
    pygame.draw.line(sprite, blue, (25, 58), (20, 64), 5)
    pygame.draw.line(sprite, green, (42, 58), (46, 64), 5)
    return sprite


def generate_show_runner_mastery_1() -> pygame.Surface:
    """Show Runner Mastery 1: gray split body, red crystal crown, wing-like spikes."""
    sprite = make_surface()

    outline = (42, 44, 45)
    gray = (191, 197, 188)
    dark = (80, 84, 84)
    red = (145, 70, 82)
    pale = (230, 232, 222)

    pygame.draw.polygon(sprite, red, [(8, 14), (14, 0), (19, 16), (25, 2), (30, 17)])
    pygame.draw.polygon(sprite, red, [(36, 17), (43, 2), (48, 16), (56, 1), (60, 15)])
    pygame.draw.lines(sprite, outline, False, [(8, 14), (14, 0), (19, 16), (25, 2), (30, 17)], 2)
    pygame.draw.lines(sprite, outline, False, [(36, 17), (43, 2), (48, 16), (56, 1), (60, 15)], 2)
    pygame.draw.polygon(sprite, pale, [(19, 14), (22, 1), (28, 12), (33, 2), (39, 13), (45, 1), (49, 15)])
    pygame.draw.lines(sprite, outline, True, [(19, 14), (22, 1), (28, 12), (33, 2), (39, 13), (45, 1), (49, 15)], 2)
    pygame.draw.ellipse(sprite, gray, pygame.Rect(15, 13, 36, 31))
    pygame.draw.polygon(sprite, dark, [(15, 15), (32, 14), (31, 44), (17, 43)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(15, 13, 36, 31), 2)
    pygame.draw.line(sprite, pale, (32, 14), (32, 44), 2)
    for y in range(17, 43, 5):
        pygame.draw.polygon(sprite, gray, [(31, y), (35, y + 2), (31, y + 4)])
    pygame.draw.arc(sprite, outline, pygame.Rect(20, 25, 26, 13), 0.2, 2.8, 2)
    pygame.draw.polygon(sprite, pale, [(39, 23), (45, 18), (44, 30)])
    pygame.draw.polygon(sprite, dark, [(19, 43), (32, 43), (31, 60), (15, 61)])
    pygame.draw.polygon(sprite, gray, [(32, 43), (48, 43), (51, 61), (31, 60)])
    pygame.draw.line(sprite, outline, (32, 42), (32, 61), 2)
    pygame.draw.line(sprite, dark, (20, 47), (8, 55), 5)
    pygame.draw.line(sprite, gray, (47, 47), (58, 55), 5)
    pygame.draw.line(sprite, dark, (26, 60), (20, 64), 5)
    pygame.draw.line(sprite, gray, (41, 60), (45, 64), 5)
    return sprite


def generate_show_runner_mastery_2() -> pygame.Surface:
    """Show Runner Mastery 2: gray body, blue crystal crown, jagged dark side."""
    sprite = make_surface()

    outline = (42, 44, 45)
    gray = (194, 202, 198)
    dark = (70, 76, 80)
    blue = (118, 150, 198)
    pale = (232, 235, 226)

    pygame.draw.polygon(sprite, blue, [(9, 17), (15, 5), (20, 18), (26, 1), (32, 18), (39, 1), (45, 18), (54, 4), (58, 17)])
    pygame.draw.lines(sprite, outline, False, [(9, 17), (15, 5), (20, 18), (26, 1), (32, 18), (39, 1), (45, 18), (54, 4), (58, 17)], 2)
    pygame.draw.ellipse(sprite, gray, pygame.Rect(14, 14, 38, 31))
    pygame.draw.polygon(sprite, dark, [(31, 15), (51, 18), (45, 44), (30, 44), (28, 28)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(14, 14, 38, 31), 2)
    for y in range(17, 44, 5):
        pygame.draw.polygon(sprite, pale, [(29, y), (34, y + 2), (29, y + 4)])
    pygame.draw.polygon(sprite, dark, [(36, 23), (44, 18), (43, 31)])
    pygame.draw.arc(sprite, outline, pygame.Rect(20, 27, 27, 13), 0.1, 2.9, 2)
    for x in range(25, 45, 6):
        pygame.draw.polygon(sprite, pale, [(x, 31), (x + 3, 33), (x, 36)])
    pygame.draw.polygon(sprite, dark, [(19, 44), (31, 43), (30, 61), (14, 62)])
    pygame.draw.polygon(sprite, gray, [(31, 43), (47, 44), (53, 58), (31, 61)])
    for y in (43, 50, 57):
        pygame.draw.polygon(sprite, blue, [(47, y), (62, y + 3), (50, y + 7)])
    pygame.draw.line(sprite, dark, (20, 47), (7, 35), 5)
    pygame.draw.rect(sprite, blue, pygame.Rect(0, 30, 13, 10), border_radius=2)
    pygame.draw.line(sprite, gray, (27, 60), (21, 64), 5)
    pygame.draw.line(sprite, gray, (42, 59), (47, 64), 5)
    return sprite


def generate_show_runner_mastery_3() -> pygame.Surface:
    """Show Runner Mastery 3: blue-gray body, red crown, sharp split face."""
    sprite = make_surface()

    outline = (42, 44, 45)
    blue = (142, 174, 199)
    blue_dark = (83, 123, 176)
    red = (145, 70, 82)
    pale = (230, 234, 226)

    pygame.draw.polygon(sprite, red, [(7, 15), (14, 2), (20, 17), (26, 0), (32, 18), (38, 0), (45, 17), (53, 3), (59, 15)])
    pygame.draw.lines(sprite, outline, False, [(7, 15), (14, 2), (20, 17), (26, 0), (32, 18), (38, 0), (45, 17), (53, 3), (59, 15)], 2)
    pygame.draw.rect(sprite, red, pygame.Rect(20, 6, 29, 9), border_radius=2)
    pygame.draw.ellipse(sprite, blue, pygame.Rect(14, 15, 38, 31))
    pygame.draw.polygon(sprite, pale, [(15, 16), (32, 15), (31, 46), (16, 44)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(14, 15, 38, 31), 2)
    for y in range(18, 46, 5):
        pygame.draw.polygon(sprite, blue_dark, [(31, y), (36, y + 2), (31, y + 4)])
    pygame.draw.arc(sprite, outline, pygame.Rect(20, 28, 28, 13), 0.1, 2.9, 2)
    for x in range(24, 47, 6):
        pygame.draw.polygon(sprite, pale, [(x, 32), (x + 3, 34), (x, 37)])
    pygame.draw.polygon(sprite, blue_dark, [(18, 45), (32, 45), (31, 62), (13, 62)])
    pygame.draw.polygon(sprite, blue, [(32, 45), (48, 45), (52, 62), (31, 62)])
    pygame.draw.line(sprite, outline, (32, 44), (32, 62), 2)
    pygame.draw.line(sprite, blue_dark, (19, 49), (6, 56), 5)
    pygame.draw.line(sprite, blue, (48, 49), (60, 56), 5)
    pygame.draw.line(sprite, blue_dark, (26, 61), (19, 64), 5)
    pygame.draw.line(sprite, blue, (42, 61), (47, 64), 5)
    return sprite


def generate_show_runner_ocean_runner() -> pygame.Surface:
    """Ocean Runner skin: sea green and jellyfish colors with tentacles and fish details."""
    sprite = make_surface()
    outline = (43, 48, 51)
    green = (93, 184, 160)
    pink = (218, 135, 162)
    blue = (101, 182, 222)
    gray = (204, 214, 214)

    pygame.draw.ellipse(sprite, green, pygame.Rect(14, 5, 35, 31))
    pygame.draw.polygon(sprite, pink, [(32, 6), (51, 12), (48, 36), (32, 36)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(14, 5, 35, 31), 2)
    pygame.draw.polygon(sprite, gray, [(19, 18), (31, 13), (31, 27)])
    pygame.draw.ellipse(sprite, (238, 238, 229), pygame.Rect(39, 15, 7, 11))
    pygame.draw.line(sprite, outline, (43, 17), (43, 23), 1)
    for y in range(9, 37, 5):
        pygame.draw.polygon(sprite, gray, [(31, y), (35, y + 2), (31, y + 4)])
    pygame.draw.polygon(sprite, green, [(19, 36), (32, 36), (31, 59), (17, 59)])
    pygame.draw.polygon(sprite, blue, [(32, 36), (47, 37), (51, 58), (31, 59)])
    for x, color in ((34, pink), (39, blue), (44, gray)):
        pygame.draw.line(sprite, color, (x, 38), (x - 2, 55), 3)
    pygame.draw.circle(sprite, (180, 130, 164), (50, 45), 3)
    pygame.draw.circle(sprite, (180, 130, 164), (53, 53), 3)
    pygame.draw.polygon(sprite, (197, 153, 78), [(36, 49), (43, 46), (43, 52)])
    pygame.draw.line(sprite, green, (20, 42), (7, 52), 5)
    pygame.draw.circle(sprite, green, (7, 52), 5)
    pygame.draw.line(sprite, green, (24, 58), (22, 64), 5)
    pygame.draw.line(sprite, blue, (42, 58), (48, 64), 5)
    return sprite


def generate_vengance_wick_wonalds() -> pygame.Surface:
    """Wick Wonalds skin: gray bot with menu-board head and yellow W body mark."""
    sprite = make_surface()
    outline = (38, 41, 43)
    gray = (132, 134, 130)
    dark = (65, 67, 67)
    yellow = (217, 190, 42)

    pygame.draw.polygon(sprite, (226, 226, 216), [(7, 7), (57, 5), (60, 28), (5, 30)])
    pygame.draw.polygon(sprite, outline, [(7, 7), (57, 5), (60, 28), (5, 30)], 2)
    for x in (23, 40):
        pygame.draw.line(sprite, outline, (x, 8), (x, 28), 1)
    for y in (15, 22):
        pygame.draw.line(sprite, outline, (7, y), (58, y), 1)
    pygame.draw.circle(sprite, (130, 83, 57), (14, 12), 3)
    pygame.draw.circle(sprite, (205, 65, 70), (31, 12), 3)
    pygame.draw.circle(sprite, (72, 155, 73), (49, 12), 3)
    draw_outline_rect(sprite, pygame.Rect(21, 30, 25, 29), gray, outline, 4)
    pygame.draw.polygon(sprite, dark, [(24, 35), (32, 57), (40, 35), (44, 55), (22, 55)])
    pygame.draw.line(sprite, yellow, (25, 38), (31, 53), 3)
    pygame.draw.line(sprite, yellow, (39, 38), (33, 53), 3)
    pygame.draw.line(sprite, dark, (22, 38), (7, 47), 4)
    pygame.draw.line(sprite, dark, (45, 38), (58, 30), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(3, 44, 8, 5), border_radius=2)
    pygame.draw.rect(sprite, gray, pygame.Rect(55, 27, 8, 5), border_radius=2)
    pygame.draw.line(sprite, dark, (28, 58), (27, 64), 4)
    pygame.draw.line(sprite, dark, (40, 58), (42, 64), 4)
    return sprite


def generate_vengance_mlg() -> pygame.Surface:
    """MLG skin: green robot, white MLG head, purple launcher and green cap."""
    sprite = make_surface()
    outline = (38, 41, 43)
    green = (108, 158, 54)
    purple = (84, 78, 166)

    pygame.draw.rect(sprite, (231, 232, 224), pygame.Rect(12, 6, 42, 25), border_radius=3)
    pygame.draw.rect(sprite, outline, pygame.Rect(12, 6, 42, 25), 2, border_radius=3)
    pygame.draw.rect(sprite, green, pygame.Rect(25, 0, 14, 8), border_radius=4)
    pygame.draw.line(sprite, outline, (17, 24), (17, 12), 2)
    pygame.draw.line(sprite, outline, (17, 12), (22, 20), 2)
    pygame.draw.line(sprite, outline, (22, 20), (27, 12), 2)
    pygame.draw.line(sprite, outline, (27, 12), (27, 24), 2)
    pygame.draw.line(sprite, outline, (32, 12), (32, 24), 2)
    pygame.draw.line(sprite, outline, (32, 24), (39, 24), 2)
    pygame.draw.arc(sprite, outline, pygame.Rect(40, 12, 10, 12), 1.4, 5.1, 2)
    pygame.draw.line(sprite, outline, (46, 18), (51, 18), 2)
    pygame.draw.circle(sprite, outline, (47, 12), 2)
    draw_outline_rect(sprite, pygame.Rect(22, 31, 24, 28), green, outline, 4)
    pygame.draw.line(sprite, outline, (26, 38), (42, 38), 2)
    pygame.draw.line(sprite, outline, (26, 43), (42, 43), 2)
    pygame.draw.rect(sprite, (204, 82, 94), pygame.Rect(25, 50, 10, 6), border_radius=1)
    pygame.draw.line(sprite, green, (22, 39), (8, 49), 4)
    pygame.draw.line(sprite, green, (46, 38), (57, 24), 4)
    pygame.draw.polygon(sprite, purple, [(52, 20), (64, 14), (64, 25), (54, 30)])
    pygame.draw.rect(sprite, (230, 231, 224), pygame.Rect(3, 46, 8, 5), border_radius=2)
    pygame.draw.line(sprite, green, (28, 58), (27, 64), 4)
    pygame.draw.line(sprite, green, (40, 58), (41, 64), 4)
    return sprite


def generate_vengance_bot_mastery_1() -> pygame.Surface:
    """Vengance Bot Mastery 1: gray bot, jagged red mouth, cracked body, single eye."""
    sprite = make_surface()
    outline = (38, 41, 43)
    gray = (142, 145, 139)
    dark = (50, 52, 52)
    red = (190, 72, 68)
    blue = (92, 137, 199)
    yellow = (222, 194, 55)

    pygame.draw.polygon(sprite, gray, [(6, 7), (58, 4), (61, 28), (4, 30)])
    pygame.draw.polygon(sprite, outline, [(6, 7), (58, 4), (61, 28), (4, 30)], 2)
    pygame.draw.polygon(sprite, dark, [(39, 8), (56, 7), (51, 23), (37, 24)])
    pygame.draw.ellipse(sprite, (226, 229, 220), pygame.Rect(43, 11, 8, 12))
    pygame.draw.line(sprite, outline, (47, 14), (47, 20), 1)
    pygame.draw.polygon(sprite, (226, 229, 220), [(15, 11), (27, 8), (31, 17), (16, 18)])
    pygame.draw.line(sprite, blue, (18, 13), (30, 12), 2)
    pygame.draw.line(sprite, yellow, (21, 10), (24, 18), 2)
    pygame.draw.polygon(sprite, red, [(13, 20), (50, 20), (43, 28), (21, 28)])
    for x in range(14, 50, 6):
        pygame.draw.polygon(sprite, outline, [(x, 20), (x + 4, 24), (x, 28)])
    draw_outline_rect(sprite, pygame.Rect(20, 30, 28, 29), gray, outline, 3)
    pygame.draw.line(sprite, dark, (23, 33), (45, 57), 2)
    pygame.draw.line(sprite, dark, (42, 33), (25, 58), 2)
    pygame.draw.line(sprite, dark, (21, 39), (8, 48), 4)
    pygame.draw.line(sprite, dark, (48, 38), (59, 30), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(4, 46, 8, 5), border_radius=2)
    pygame.draw.rect(sprite, gray, pygame.Rect(56, 27, 7, 5), border_radius=2)
    pygame.draw.line(sprite, dark, (28, 58), (27, 64), 4)
    pygame.draw.line(sprite, dark, (41, 58), (43, 64), 4)
    return sprite


def generate_vengance_bot_mastery_2() -> pygame.Surface:
    """Vengance Bot Mastery 2: wider tilted head, red mouth, crystal eyes, gray body."""
    sprite = make_surface()
    outline = (38, 41, 43)
    gray = (151, 154, 148)
    dark = (42, 44, 44)
    red = (195, 74, 70)
    blue = (83, 154, 203)
    yellow = (224, 195, 62)

    pygame.draw.polygon(sprite, gray, [(3, 8), (58, 2), (63, 29), (5, 31)])
    pygame.draw.polygon(sprite, outline, [(3, 8), (58, 2), (63, 29), (5, 31)], 2)
    pygame.draw.polygon(sprite, dark, [(31, 7), (52, 5), (47, 22), (30, 24)])
    pygame.draw.polygon(sprite, (226, 229, 220), [(13, 12), (24, 8), (29, 16), (16, 20)])
    pygame.draw.line(sprite, blue, (15, 15), (27, 13), 2)
    pygame.draw.line(sprite, yellow, (19, 11), (23, 19), 2)
    pygame.draw.polygon(sprite, (226, 229, 220), [(40, 11), (49, 10), (50, 22), (39, 22)])
    pygame.draw.line(sprite, red, (44, 13), (46, 20), 2)
    pygame.draw.polygon(sprite, red, [(10, 22), (56, 20), (51, 29), (16, 30)])
    for x in range(12, 56, 6):
        pygame.draw.polygon(sprite, outline, [(x, 22), (x + 4, 25), (x, 29)])
    draw_outline_rect(sprite, pygame.Rect(21, 31, 29, 28), gray, outline, 4)
    for x in (26, 34, 43):
        pygame.draw.line(sprite, dark, (x, 33), (x + 3, 58), 1)
    pygame.draw.line(sprite, dark, (22, 39), (9, 49), 4)
    pygame.draw.line(sprite, dark, (50, 38), (60, 29), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(5, 46, 8, 6), border_radius=2)
    pygame.draw.rect(sprite, gray, pygame.Rect(57, 26, 7, 6), border_radius=2)
    pygame.draw.line(sprite, dark, (29, 58), (28, 64), 4)
    pygame.draw.line(sprite, dark, (43, 58), (45, 64), 4)
    return sprite


def generate_vengance_bot_mastery_3() -> pygame.Surface:
    """Vengance Bot Mastery 3: black head, giant red teeth, cap, green body crack."""
    sprite = make_surface()
    outline = (32, 34, 35)
    gray = (136, 139, 134)
    dark = (28, 30, 30)
    red = (190, 62, 62)
    green = (85, 135, 50)
    tan = (156, 113, 72)
    blue = (80, 132, 195)
    yellow = (224, 195, 62)

    pygame.draw.polygon(sprite, gray, [(4, 6), (57, 4), (62, 31), (5, 31)])
    pygame.draw.polygon(sprite, dark, [(6, 8), (58, 5), (60, 29), (8, 30)])
    pygame.draw.polygon(sprite, outline, [(4, 6), (57, 4), (62, 31), (5, 31)], 2)
    pygame.draw.ellipse(sprite, tan, pygame.Rect(49, 0, 14, 9))
    pygame.draw.line(sprite, outline, (52, 4), (60, 4), 1)
    pygame.draw.polygon(sprite, (226, 229, 220), [(14, 11), (26, 8), (31, 18), (16, 20)])
    pygame.draw.line(sprite, blue, (17, 13), (28, 11), 2)
    pygame.draw.line(sprite, yellow, (22, 9), (22, 18), 2)
    pygame.draw.polygon(sprite, (226, 229, 220), [(42, 12), (51, 10), (53, 21), (43, 22)])
    pygame.draw.line(sprite, red, (46, 13), (49, 20), 2)
    pygame.draw.polygon(sprite, red, [(8, 21), (57, 20), (51, 30), (13, 30)])
    for x in range(9, 57, 5):
        pygame.draw.polygon(sprite, (226, 229, 220), [(x, 21), (x + 4, 25), (x, 30)])
    draw_outline_rect(sprite, pygame.Rect(20, 31, 29, 29), gray, outline, 3)
    pygame.draw.line(sprite, green, (45, 33), (37, 45), 2)
    pygame.draw.line(sprite, green, (37, 45), (42, 58), 2)
    pygame.draw.line(sprite, dark, (22, 39), (8, 50), 4)
    pygame.draw.line(sprite, dark, (49, 39), (61, 49), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(3, 47, 9, 6), border_radius=2)
    pygame.draw.rect(sprite, gray, pygame.Rect(57, 47, 7, 6), border_radius=2)
    pygame.draw.line(sprite, dark, (29, 59), (28, 64), 4)
    pygame.draw.line(sprite, dark, (43, 59), (45, 64), 4)
    return sprite


def main() -> None:
    pygame.init()
    save_if_missing("revenge_bot.png", generate_revenge_bot())
    save_if_missing("ducky_fried_chicken.png", generate_ducky_fried_chicken())
    save_if_missing("ducky_inverted.png", generate_ducky_inverted())
    save_if_missing("ducky_ogel.png", generate_ducky_ogel())
    save_if_missing("subslasher.png", generate_subslasher())
    save_if_missing("subslasher_tennis_dude.png", generate_subslasher_tennis_dude())
    save_if_missing("subslasher_pickle_ball_bro.png", generate_subslasher_pickle_ball_bro())
    save_if_missing("show_runner.png", generate_show_runner())
    save_if_missing("show_runner_pack_runner.png", generate_show_runner_pack_runner())
    save_if_missing("show_runner_maldin_inverted.png", generate_show_runner_maldin_inverted())
    save_if_missing("show_runner_ocean_runner.png", generate_show_runner_ocean_runner())
    save_if_missing("show_runner_mastery_1.png", generate_show_runner_mastery_1())
    save_if_missing("show_runner_mastery_2.png", generate_show_runner_mastery_2())
    save_if_missing("show_runner_mastery_3.png", generate_show_runner_mastery_3())
    save_if_missing("malice.png", generate_malice())
    save_if_missing("vengance_bot.png", generate_vengance_bot())
    save_if_missing("vengance_wick_wonalds.png", generate_vengance_wick_wonalds())
    save_if_missing("vengance_mlg.png", generate_vengance_mlg())
    save_if_missing("vengance_bot_mastery_1.png", generate_vengance_bot_mastery_1())
    save_if_missing("vengance_bot_mastery_2.png", generate_vengance_bot_mastery_2())
    save_if_missing("vengance_bot_mastery_3.png", generate_vengance_bot_mastery_3())
    save_if_missing("survivor.png", generate_survivor())
    pygame.quit()


if __name__ == "__main__":
    main()

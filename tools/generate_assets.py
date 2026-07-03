from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame


ROOT_DIR = Path(__file__).resolve().parents[1]
SPRITE_DIR = ROOT_DIR / "assets" / "sprites"
ANIMATION_DIR = SPRITE_DIR / "animations"
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


def save_animation_if_missing(filename: str, surface: pygame.Surface) -> None:
    ANIMATION_DIR.mkdir(parents=True, exist_ok=True)
    path = ANIMATION_DIR / filename
    if path.exists():
        print(f"Skipped existing {path}")
        return
    pygame.image.save(surface, str(path))
    print(f"Created {path}")


def make_walk_frame(source: pygame.Surface, frame: int) -> pygame.Surface:
    """Create a simple transparent walking frame from a finished 64x64 sprite."""
    canvas = make_surface()
    shadow_alpha = 36 if frame in (0, 2) else 52
    pygame.draw.ellipse(canvas, (0, 0, 0, shadow_alpha), pygame.Rect(18, 57, 28, 6))

    if frame == 0:
        transformed = source.copy()
        offset = (0, 0)
    elif frame == 1:
        scaled = pygame.transform.smoothscale(source, (62, 64))
        transformed = pygame.transform.rotozoom(scaled, -4, 1.0)
        offset = (-1, -2)
    elif frame == 2:
        transformed = pygame.transform.smoothscale(source, (64, 62))
        offset = (0, 1)
    else:
        scaled = pygame.transform.smoothscale(source, (62, 64))
        transformed = pygame.transform.rotozoom(scaled, 4, 1.0)
        offset = (1, -2)

    rect = transformed.get_rect(center=(SIZE // 2 + offset[0], SIZE // 2 + offset[1]))
    canvas.blit(transformed, rect)

    # Tiny foot/impact accents make the motion read at small in-game scale.
    if frame == 1:
        pygame.draw.ellipse(canvas, (255, 255, 255, 58), pygame.Rect(12, 58, 12, 4))
    elif frame == 3:
        pygame.draw.ellipse(canvas, (255, 255, 255, 58), pygame.Rect(40, 58, 12, 4))

    return canvas


def should_make_walk_frames(sprite_key: str) -> bool:
    return not any(
        sprite_key.startswith(prefix)
        for prefix in ("malice_tiger_", "malice_bird_", "malice_dinosaur_")
    )


def generate_walk_animations() -> None:
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))

    for path in sorted(SPRITE_DIR.glob("*.png")):
        sprite_key = path.stem
        if not should_make_walk_frames(sprite_key):
            continue
        try:
            source = pygame.image.load(str(path)).convert_alpha()
        except pygame.error:
            continue

        source = pygame.transform.smoothscale(source, (SIZE, SIZE))
        for frame in range(4):
            save_animation_if_missing(
                f"{sprite_key}_walk_{frame}.png",
                make_walk_frame(source, frame),
            )


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


def generate_ducky_daddys_belt() -> pygame.Surface:
    """Daddy's Belt skin: yellow Ducky wrapped in brown belts with a belt-swing theme."""
    sprite = make_surface()

    outline = (43, 45, 51)
    yellow = (230, 214, 82)
    yellow_dark = (181, 163, 54)
    belt = (128, 88, 54)
    belt_dark = (76, 52, 35)
    buckle = (224, 188, 85)
    orange = (225, 135, 54)
    pale = (231, 232, 218)

    pygame.draw.ellipse(sprite, yellow, pygame.Rect(13, 3, 38, 31))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(13, 3, 38, 31), 2)
    draw_outline_rect(sprite, pygame.Rect(17, 27, 32, 27), yellow, outline, 6)
    pygame.draw.ellipse(sprite, pale, pygame.Rect(24, 12, 7, 12))
    pygame.draw.ellipse(sprite, pale, pygame.Rect(39, 12, 8, 13))
    pygame.draw.line(sprite, outline, (28, 15), (28, 21), 1)
    pygame.draw.line(sprite, outline, (43, 15), (43, 22), 1)
    pygame.draw.ellipse(sprite, orange, pygame.Rect(25, 24, 17, 7))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(25, 24, 17, 7), 1)

    for start, end in (
        ((14, 11), (49, 35)),
        ((12, 27), (42, 58)),
        ((48, 9), (19, 51)),
        ((19, 3), (48, 47)),
        ((6, 45), (28, 34)),
        ((45, 36), (61, 46)),
    ):
        pygame.draw.line(sprite, belt, start, end, 5)
        pygame.draw.line(sprite, belt_dark, start, end, 1)
    pygame.draw.rect(sprite, buckle, pygame.Rect(27, 39, 9, 7), 2, border_radius=2)

    pygame.draw.line(sprite, yellow_dark, (18, 37), (7, 50), 5)
    pygame.draw.line(sprite, belt, (8, 50), (0, 58), 4)
    pygame.draw.line(sprite, yellow_dark, (49, 36), (60, 48), 5)
    pygame.draw.line(sprite, belt, (58, 47), (64, 54), 4)
    pygame.draw.line(sprite, yellow_dark, (26, 54), (22, 64), 5)
    pygame.draw.line(sprite, yellow_dark, (42, 54), (47, 64), 5)
    pygame.draw.ellipse(sprite, orange, pygame.Rect(14, 58, 15, 6))
    pygame.draw.ellipse(sprite, orange, pygame.Rect(39, 58, 16, 6))

    return sprite


def generate_ducky_subject_5_png() -> pygame.Surface:
    """Subject 5 PNG skin: plain gray Ducky-like subject with dark eyes and feet."""
    sprite = make_surface()
    outline = (64, 67, 66)
    gray = (176, 181, 170)
    gray_dark = (95, 99, 96)
    pale = (207, 211, 201)

    pygame.draw.ellipse(sprite, pale, pygame.Rect(12, 3, 40, 31))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(12, 3, 40, 31), 2)
    draw_outline_rect(sprite, pygame.Rect(18, 28, 29, 28), pale, outline, 12)

    pygame.draw.ellipse(sprite, gray_dark, pygame.Rect(23, 11, 6, 11))
    pygame.draw.ellipse(sprite, gray_dark, pygame.Rect(40, 11, 6, 11))
    pygame.draw.ellipse(sprite, pale, pygame.Rect(24, 25, 19, 7))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(24, 25, 19, 7), 1)

    pygame.draw.line(sprite, gray, (18, 38), (5, 51), 5)
    pygame.draw.line(sprite, outline, (18, 38), (5, 51), 1)
    pygame.draw.line(sprite, gray, (49, 38), (60, 51), 5)
    pygame.draw.line(sprite, outline, (49, 38), (60, 51), 1)

    pygame.draw.line(sprite, gray, (27, 55), (21, 64), 5)
    pygame.draw.line(sprite, gray, (42, 55), (49, 64), 5)
    pygame.draw.ellipse(sprite, gray_dark, pygame.Rect(12, 58, 17, 7))
    pygame.draw.ellipse(sprite, gray_dark, pygame.Rect(41, 58, 18, 7))
    for x in range(15, 28, 4):
        pygame.draw.line(sprite, pale, (x, 59), (x - 2, 64), 1)
    for x in range(43, 58, 4):
        pygame.draw.line(sprite, pale, (x, 59), (x + 2, 64), 1)

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


def generate_survivor_odd() -> pygame.Surface:
    """Odd 1 3 5 7 9: gray mask, pale outfit, cape, green belt, odd-number badge."""
    sprite = make_surface()
    outline = (48, 52, 55)
    pale = (222, 228, 224)
    gray = (116, 120, 120)
    dark = (45, 48, 50)
    green = (93, 145, 65)
    blue = (121, 198, 226)

    pygame.draw.ellipse(sprite, gray, pygame.Rect(20, 2, 25, 24))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(20, 2, 25, 24), 2)
    pygame.draw.circle(sprite, (156, 160, 160), (32, 14), 8, 2)
    draw_outline_rect(sprite, pygame.Rect(18, 25, 31, 31), pale, outline, 5)
    pygame.draw.rect(sprite, blue, pygame.Rect(28, 34, 9, 7), border_radius=2)
    for x in (25, 39):
        pygame.draw.arc(sprite, dark, pygame.Rect(x, 31, 8, 16), 1.0, 5.1, 2)
    pygame.draw.line(sprite, green, (18, 52), (48, 50), 3)
    pygame.draw.polygon(sprite, pale, [(49, 28), (63, 39), (50, 45)])
    pygame.draw.polygon(sprite, pale, [(18, 34), (4, 47), (0, 41), (13, 33)])
    pygame.draw.circle(sprite, dark, (14, 41), 4)
    pygame.draw.circle(sprite, dark, (51, 41), 4)
    pygame.draw.line(sprite, gray, (27, 56), (24, 64), 5)
    pygame.draw.line(sprite, gray, (41, 56), (45, 64), 5)
    return sprite


def generate_survivor_explorer() -> pygame.Surface:
    """Explorer: yellow smile face, brown coat, red gloves and boots."""
    sprite = make_surface()
    outline = (48, 52, 55)
    yellow = (232, 217, 71)
    brown = (154, 116, 80)
    red = (128, 55, 66)

    pygame.draw.ellipse(sprite, yellow, pygame.Rect(18, 3, 31, 27))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(18, 3, 31, 27), 2)
    pygame.draw.circle(sprite, outline, (27, 13), 3)
    pygame.draw.circle(sprite, outline, (39, 13), 3)
    pygame.draw.arc(sprite, outline, pygame.Rect(26, 14, 16, 12), 0.2, 2.8, 2)
    draw_outline_rect(sprite, pygame.Rect(20, 29, 28, 29), brown, outline, 4)
    for x in (23, 32, 42):
        pygame.draw.line(sprite, (222, 204, 167), (x, 31), (x - 3, 56), 1)
    pygame.draw.line(sprite, brown, (20, 36), (8, 47), 5)
    pygame.draw.line(sprite, brown, (47, 36), (58, 48), 5)
    pygame.draw.circle(sprite, red, (8, 48), 5)
    pygame.draw.circle(sprite, red, (58, 48), 5)
    pygame.draw.line(sprite, red, (27, 58), (24, 64), 5)
    pygame.draw.line(sprite, red, (40, 58), (44, 64), 5)
    return sprite


def generate_survivor_kitty() -> pygame.Surface:
    """Kitty: white cat mask, purple outfit, bow mark, teal legs."""
    sprite = make_surface()
    outline = (44, 48, 52)
    white = (230, 234, 228)
    purple = (85, 74, 159)
    teal = (91, 170, 164)
    pink = (197, 101, 134)

    pygame.draw.polygon(sprite, white, [(15, 11), (20, 2), (28, 10), (39, 10), (47, 2), (52, 12), (48, 29), (19, 29)])
    pygame.draw.polygon(sprite, outline, [(15, 11), (20, 2), (28, 10), (39, 10), (47, 2), (52, 12), (48, 29), (19, 29)], 2)
    pygame.draw.circle(sprite, pink, (24, 15), 2)
    pygame.draw.circle(sprite, pink, (43, 15), 2)
    pygame.draw.rect(sprite, white, pygame.Rect(23, 18, 22, 9), border_radius=4)
    for x in (27, 34, 41):
        pygame.draw.polygon(sprite, outline, [(x, 18), (x + 3, 21), (x, 26)])
    draw_outline_rect(sprite, pygame.Rect(20, 29, 29, 29), purple, outline, 3)
    pygame.draw.polygon(sprite, pink, [(31, 37), (25, 33), (25, 41)])
    pygame.draw.polygon(sprite, pink, [(33, 37), (40, 33), (40, 41)])
    pygame.draw.line(sprite, purple, (21, 37), (8, 48), 5)
    pygame.draw.line(sprite, purple, (48, 37), (59, 49), 5)
    pygame.draw.ellipse(sprite, white, pygame.Rect(3, 45, 10, 8))
    pygame.draw.ellipse(sprite, white, pygame.Rect(55, 46, 9, 8))
    pygame.draw.line(sprite, teal, (27, 58), (25, 64), 5)
    pygame.draw.line(sprite, teal, (41, 58), (45, 64), 5)
    return sprite


def generate_survivor_kevin() -> pygame.Surface:
    """Kevin: yellow hair, black mask, brown shirt, claws and shorts."""
    sprite = make_surface()
    outline = (44, 48, 52)
    yellow = (226, 208, 72)
    brown = (126, 99, 79)
    dark = (36, 39, 42)
    green = (69, 132, 91)
    pale = (217, 222, 214)

    pygame.draw.ellipse(sprite, yellow, pygame.Rect(17, 3, 32, 25))
    pygame.draw.polygon(sprite, yellow, [(23, 3), (28, 0), (33, 7), (39, 0), (45, 9)])
    pygame.draw.ellipse(sprite, outline, pygame.Rect(17, 3, 32, 25), 2)
    pygame.draw.polygon(sprite, dark, [(18, 17), (49, 16), (44, 30), (24, 30)])
    pygame.draw.circle(sprite, green, (27, 15), 3)
    pygame.draw.circle(sprite, green, (40, 15), 3)
    draw_outline_rect(sprite, pygame.Rect(19, 29, 30, 27), brown, outline, 4)
    pygame.draw.circle(sprite, yellow, (26, 39), 4)
    pygame.draw.line(sprite, dark, (30, 43), (44, 52), 3)
    pygame.draw.line(sprite, brown, (20, 36), (8, 48), 5)
    pygame.draw.line(sprite, brown, (48, 36), (59, 48), 5)
    pygame.draw.line(sprite, dark, (58, 48), (64, 44), 2)
    pygame.draw.line(sprite, pale, (27, 56), (23, 64), 5)
    pygame.draw.line(sprite, pale, (42, 56), (47, 64), 5)
    return sprite


def generate_survivor_trashy() -> pygame.Surface:
    """Trashy: pumpkin-trash head, green-stained robe, black eyes."""
    sprite = make_surface()
    outline = (52, 55, 51)
    tan = (209, 177, 126)
    green = (109, 155, 81)
    pale = (220, 222, 204)
    dark = (44, 47, 45)

    pygame.draw.ellipse(sprite, tan, pygame.Rect(17, 2, 33, 28))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(17, 2, 33, 28), 2)
    pygame.draw.polygon(sprite, green, [(32, 2), (36, 0), (35, 9)])
    pygame.draw.ellipse(sprite, dark, pygame.Rect(24, 11, 8, 9))
    pygame.draw.ellipse(sprite, dark, pygame.Rect(38, 11, 8, 9))
    pygame.draw.rect(sprite, dark, pygame.Rect(27, 22, 18, 5), border_radius=2)
    pygame.draw.line(sprite, green, (42, 23), (48, 20), 2)
    draw_outline_rect(sprite, pygame.Rect(19, 29, 31, 29), pale, outline, 4)
    for x in (26, 36, 43):
        pygame.draw.line(sprite, green, (x, 31), (x - 8, 55), 2)
    pygame.draw.line(sprite, pale, (20, 38), (8, 50), 5)
    pygame.draw.line(sprite, pale, (49, 38), (60, 50), 5)
    pygame.draw.line(sprite, outline, (28, 58), (25, 64), 4)
    pygame.draw.line(sprite, outline, (42, 58), (46, 64), 4)
    return sprite


def generate_survivor_queen_goopy() -> pygame.Surface:
    """Queen Goopy: green goopy ghost, purple belt, long flowing base."""
    sprite = make_surface()
    outline = (59, 74, 57)
    green = (112, 139, 80)
    pale = (207, 220, 192)
    purple = (119, 103, 174)

    pygame.draw.polygon(sprite, pale, [(18, 4), (44, 4), (53, 23), (47, 38), (50, 60), (13, 60), (17, 36), (12, 25)])
    pygame.draw.polygon(sprite, outline, [(18, 4), (44, 4), (53, 23), (47, 38), (50, 60), (13, 60), (17, 36), (12, 25)], 2)
    pygame.draw.polygon(sprite, green, [(18, 5), (45, 5), (43, 27), (33, 22), (24, 28), (17, 20)])
    pygame.draw.circle(sprite, pale, (28, 16), 4)
    pygame.draw.circle(sprite, pale, (39, 16), 4)
    pygame.draw.arc(sprite, outline, pygame.Rect(27, 19, 18, 13), 0.0, 3.1, 2)
    pygame.draw.line(sprite, purple, (15, 43), (51, 42), 4)
    pygame.draw.line(sprite, green, (18, 32), (7, 43), 4)
    pygame.draw.line(sprite, green, (49, 32), (61, 43), 4)
    pygame.draw.ellipse(sprite, green, pygame.Rect(1, 56, 58, 8))
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


def generate_malice_bug() -> pygame.Surface:
    """Bug Malice skin: green insect body, dark mask eyes, antennae, and hooked legs."""
    sprite = make_surface()
    outline = (49, 54, 46)
    green = (145, 166, 91)
    green_dark = (83, 111, 55)
    pale = (221, 222, 205)
    dark = (42, 43, 39)

    pygame.draw.polygon(sprite, green, [(8, 43), (28, 26), (47, 22), (58, 32), (45, 47), (22, 51)])
    pygame.draw.polygon(sprite, outline, [(8, 43), (28, 26), (47, 22), (58, 32), (45, 47), (22, 51)], 2)
    pygame.draw.polygon(sprite, green_dark, [(22, 28), (30, 14), (38, 28)])
    pygame.draw.polygon(sprite, green_dark, [(37, 24), (46, 8), (53, 29)])
    for x in (26, 36, 46):
        pygame.draw.line(sprite, pale, (x, 27), (x - 5, 48), 3)
    pygame.draw.ellipse(sprite, pale, pygame.Rect(47, 17, 15, 18))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(47, 17, 15, 18), 2)
    pygame.draw.ellipse(sprite, dark, pygame.Rect(49, 20, 5, 7))
    pygame.draw.ellipse(sprite, dark, pygame.Rect(56, 21, 4, 6))
    pygame.draw.arc(sprite, outline, pygame.Rect(45, 6, 23, 19), 3.4, 5.4, 2)
    pygame.draw.arc(sprite, outline, pygame.Rect(43, 8, 27, 21), 3.6, 5.7, 2)
    for x in (22, 31, 41, 50):
        pygame.draw.line(sprite, green_dark, (x, 45), (x - 4, 63), 5)
        pygame.draw.line(sprite, outline, (x, 45), (x - 4, 63), 1)
        pygame.draw.line(sprite, outline, (x - 5, 62), (x + 1, 61), 2)

    return sprite


def generate_malice_bones() -> pygame.Surface:
    """Bones Malice skin: pale skeleton, rib cage, long tail, and toothy skull."""
    sprite = make_surface()
    outline = (75, 76, 68)
    bone = (219, 218, 198)
    bone_shadow = (177, 176, 158)
    dark = (39, 39, 35)

    pygame.draw.ellipse(sprite, bone, pygame.Rect(14, 29, 37, 16))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(14, 29, 37, 16), 2)
    pygame.draw.arc(sprite, bone_shadow, pygame.Rect(0, 21, 25, 30), 1.6, 4.8, 5)
    pygame.draw.line(sprite, outline, (13, 36), (2, 31), 2)
    for x in (22, 29, 36, 43):
        pygame.draw.arc(sprite, outline, pygame.Rect(x - 2, 29, 8, 18), 1.5, 4.7, 2)
    pygame.draw.ellipse(sprite, bone, pygame.Rect(44, 20, 18, 20))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(44, 20, 18, 20), 2)
    pygame.draw.ellipse(sprite, dark, pygame.Rect(49, 25, 4, 6))
    pygame.draw.ellipse(sprite, dark, pygame.Rect(57, 26, 3, 5))
    for x in (47, 53, 59):
        pygame.draw.circle(sprite, bone_shadow, (x, 41), 4)
    for x in (22, 34, 45):
        pygame.draw.line(sprite, bone_shadow, (x, 43), (x - 1, 62), 5)
        pygame.draw.line(sprite, outline, (x, 43), (x - 1, 62), 1)
        pygame.draw.circle(sprite, bone, (x - 1, 62), 4)

    return sprite


def generate_malice_robotic() -> pygame.Surface:
    """Robotic Malice skin: angular gray chassis, panel lights, vents, and heavy legs."""
    sprite = make_surface()
    outline = (38, 41, 45)
    gray = (128, 132, 126)
    gray_dark = (73, 77, 78)
    pale = (204, 207, 199)
    red = (199, 69, 45)
    green = (55, 153, 93)
    blue = (69, 134, 169)

    pygame.draw.polygon(sprite, gray, [(6, 35), (25, 23), (46, 22), (59, 34), (49, 51), (19, 50)])
    pygame.draw.polygon(sprite, outline, [(6, 35), (25, 23), (46, 22), (59, 34), (49, 51), (19, 50)], 2)
    pygame.draw.polygon(sprite, gray_dark, [(45, 14), (60, 20), (56, 35), (42, 31)])
    pygame.draw.polygon(sprite, outline, [(45, 14), (60, 20), (56, 35), (42, 31)], 2)
    pygame.draw.rect(sprite, red, pygame.Rect(49, 17, 6, 7), border_radius=1)
    pygame.draw.rect(sprite, green, pygame.Rect(53, 27, 4, 5), border_radius=1)
    pygame.draw.rect(sprite, blue, pygame.Rect(47, 27, 4, 5), border_radius=1)
    pygame.draw.line(sprite, pale, (13, 34), (40, 34), 3)
    pygame.draw.line(sprite, outline, (24, 24), (22, 49), 2)
    pygame.draw.line(sprite, outline, (40, 22), (47, 49), 2)
    for x in (18, 30, 43):
        pygame.draw.line(sprite, gray_dark, (x, 48), (x, 63), 6)
        pygame.draw.line(sprite, outline, (x, 48), (x, 63), 1)
        pygame.draw.rect(sprite, gray, pygame.Rect(x - 5, 58, 11, 6), border_radius=2)

    return sprite


def generate_malice_tiger(frame: int) -> pygame.Surface:
    """Hunter's Rage Tiger: blue striped body, yellow claws, angry face."""
    sprite = make_surface()
    outline = (34, 48, 58)
    blue = (49, 157, 205)
    blue_dark = (25, 103, 151)
    orange = (177, 91, 51)
    yellow = (234, 218, 68)
    white = (239, 244, 238)
    leg_shift = (-3, 2, -1)[frame % 3]

    pygame.draw.ellipse(sprite, blue, pygame.Rect(10, 24, 37, 22))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(10, 24, 37, 22), 2)
    pygame.draw.circle(sprite, blue, (48, 24), 15)
    pygame.draw.circle(sprite, outline, (48, 24), 15, 2)
    pygame.draw.arc(sprite, blue_dark, pygame.Rect(2, 18, 20, 24), 1.4, 4.6, 4)
    pygame.draw.line(sprite, outline, (12, 31), (4, 20), 1)

    for x in (17, 27, 37):
        pygame.draw.line(sprite, orange, (x, 25), (x - 4, 42), 3)
    pygame.draw.line(sprite, orange, (49, 12), (43, 28), 3)
    pygame.draw.line(sprite, orange, (56, 18), (44, 34), 3)

    pygame.draw.polygon(sprite, blue, [(39, 10), (42, 1), (47, 12)])
    pygame.draw.polygon(sprite, blue, [(55, 10), (60, 2), (59, 16)])
    pygame.draw.polygon(sprite, outline, [(39, 10), (42, 1), (47, 12)], 2)
    pygame.draw.polygon(sprite, outline, [(55, 10), (60, 2), (59, 16)], 2)
    pygame.draw.polygon(sprite, yellow, [(41, 20), (47, 17), (47, 24)])
    pygame.draw.polygon(sprite, yellow, [(53, 20), (59, 18), (57, 25)])
    pygame.draw.rect(sprite, white, pygame.Rect(40, 30, 17, 9), border_radius=3)
    for x in range(42, 57, 5):
        pygame.draw.polygon(sprite, outline, [(x, 30), (x + 3, 34), (x, 39)])

    for x, y in ((18, 44 + leg_shift), (28, 45 - leg_shift), (39, 44 + leg_shift)):
        pygame.draw.line(sprite, blue_dark, (x, 42), (x, min(64, y + 10)), 4)
        pygame.draw.line(sprite, yellow, (x, min(63, y + 10)), (x + 5, min(63, y + 7)), 2)
    return sprite


def generate_malice_bird(frame: int) -> pygame.Surface:
    """Hunter's Rage Bird: blue body, orange wings, yellow beak and legs."""
    sprite = make_surface()
    outline = (34, 48, 58)
    blue = (52, 169, 217)
    blue_dark = (28, 116, 167)
    orange = (194, 102, 54)
    yellow = (231, 219, 60)
    wing_top = (4, 0, 7)[frame % 3]
    wing_bottom = (32, 24, 36)[frame % 3]

    pygame.draw.ellipse(sprite, blue, pygame.Rect(10, 22, 36, 24))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(10, 22, 36, 24), 2)
    pygame.draw.circle(sprite, blue_dark, (49, 26), 11)
    pygame.draw.circle(sprite, outline, (49, 26), 11, 2)
    pygame.draw.polygon(sprite, yellow, [(57, 25), (64, 21), (64, 30)])
    pygame.draw.polygon(sprite, outline, [(57, 25), (64, 21), (64, 30)], 1)
    pygame.draw.circle(sprite, yellow, (49, 22), 2)

    pygame.draw.polygon(sprite, orange, [(20, 23), (18, wing_top), (30, wing_bottom), (28, 34)])
    pygame.draw.polygon(sprite, orange, [(30, 23), (34, wing_top + 1), (40, wing_bottom), (36, 35)])
    pygame.draw.lines(sprite, outline, False, [(20, 23), (18, wing_top), (30, wing_bottom)], 2)
    pygame.draw.lines(sprite, outline, False, [(30, 23), (34, wing_top + 1), (40, wing_bottom)], 2)

    for x in (22, 34):
        pygame.draw.line(sprite, yellow, (x, 45), (x - 2, 60), 4)
        pygame.draw.line(sprite, outline, (x, 45), (x - 2, 60), 1)
        pygame.draw.line(sprite, yellow, (x - 2, 60), (x - 8, 63), 2)
        pygame.draw.line(sprite, yellow, (x - 2, 60), (x + 4, 63), 2)
    return sprite


def generate_malice_dinosaur(frame: int) -> pygame.Surface:
    """Hunter's Rage Dinosaur: long blue body, orange back plates, yellow claws."""
    sprite = make_surface()
    outline = (34, 48, 58)
    blue = (43, 155, 202)
    blue_dark = (29, 113, 163)
    orange = (194, 101, 55)
    yellow = (230, 219, 62)
    leg_shift = (-2, 2, 0)[frame % 3]

    pygame.draw.ellipse(sprite, blue, pygame.Rect(13, 23, 38, 22))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(13, 23, 38, 22), 2)
    pygame.draw.ellipse(sprite, blue, pygame.Rect(40, 17, 20, 18))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(40, 17, 20, 18), 2)
    pygame.draw.polygon(sprite, blue, [(14, 32), (1, 23), (6, 43)])
    pygame.draw.line(sprite, outline, (14, 32), (2, 24), 2)
    pygame.draw.circle(sprite, yellow, (53, 23), 3)

    for x in (20, 29, 38):
        pygame.draw.polygon(sprite, orange, [(x, 23), (x + 5, 10), (x + 10, 24)])
        pygame.draw.lines(sprite, outline, True, [(x, 23), (x + 5, 10), (x + 10, 24)], 1)

    pygame.draw.line(sprite, blue_dark, (24, 42), (23 + leg_shift, 61), 5)
    pygame.draw.line(sprite, blue_dark, (41, 42), (43 - leg_shift, 61), 5)
    pygame.draw.line(sprite, yellow, (23 + leg_shift, 61), (17 + leg_shift, 63), 2)
    pygame.draw.line(sprite, yellow, (43 - leg_shift, 61), (49 - leg_shift, 63), 2)
    pygame.draw.line(sprite, blue_dark, (52, 32), (62, 42), 4)
    pygame.draw.line(sprite, yellow, (62, 42), (64, 37), 2)
    return sprite


def generate_malice_bug_dinosaur(frame: int) -> pygame.Surface:
    """Bug skin Hunter's Rage dinosaur: green plated insect-dino with antennae."""
    sprite = make_surface()
    outline = (48, 55, 44)
    green = (140, 163, 83)
    green_dark = (75, 105, 54)
    pale = (219, 222, 199)
    dark = (37, 39, 34)
    leg_shift = (-2, 2, 0)[frame % 3]

    pygame.draw.ellipse(sprite, green, pygame.Rect(10, 25, 42, 20))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(10, 25, 42, 20), 2)
    pygame.draw.polygon(sprite, green, [(9, 33), (0, 26), (3, 44)])
    pygame.draw.line(sprite, outline, (10, 33), (1, 27), 2)
    pygame.draw.ellipse(sprite, pale, pygame.Rect(42, 17, 19, 18))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(42, 17, 19, 18), 2)
    pygame.draw.ellipse(sprite, dark, pygame.Rect(49, 21, 4, 6))
    pygame.draw.arc(sprite, outline, pygame.Rect(45, 4, 18, 16), 3.5, 5.6, 2)
    pygame.draw.arc(sprite, outline, pygame.Rect(39, 4, 18, 18), 3.4, 5.4, 2)
    for x in (20, 31, 42):
        pygame.draw.polygon(sprite, green_dark, [(x, 25), (x + 4, 9), (x + 9, 25)])
        pygame.draw.lines(sprite, outline, True, [(x, 25), (x + 4, 9), (x + 9, 25)], 1)
    for x in (20, 32, 44):
        pygame.draw.line(sprite, green_dark, (x, 43), (x + leg_shift, 61), 5)
        pygame.draw.line(sprite, outline, (x, 43), (x + leg_shift, 61), 1)
        pygame.draw.line(sprite, outline, (x + leg_shift - 4, 62), (x + leg_shift + 4, 61), 2)
    return sprite


def generate_malice_bones_dinosaur(frame: int) -> pygame.Surface:
    """Bones skin Hunter's Rage dinosaur: skeletal long body with ribs and skull."""
    sprite = make_surface()
    outline = (73, 74, 67)
    bone = (221, 220, 201)
    shadow = (173, 172, 154)
    dark = (39, 39, 35)
    leg_shift = (-2, 2, 0)[frame % 3]

    pygame.draw.ellipse(sprite, bone, pygame.Rect(12, 27, 42, 17))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(12, 27, 42, 17), 2)
    pygame.draw.arc(sprite, shadow, pygame.Rect(0, 19, 26, 28), 1.5, 4.7, 5)
    pygame.draw.ellipse(sprite, bone, pygame.Rect(43, 16, 19, 18))
    pygame.draw.ellipse(sprite, outline, pygame.Rect(43, 16, 19, 18), 2)
    pygame.draw.ellipse(sprite, dark, pygame.Rect(51, 20, 4, 6))
    pygame.draw.line(sprite, outline, (51, 30), (62, 31), 2)
    for x in (20, 28, 36, 44):
        pygame.draw.arc(sprite, outline, pygame.Rect(x - 3, 27, 9, 18), 1.4, 4.6, 2)
    for x in (24, 42):
        pygame.draw.line(sprite, shadow, (x, 42), (x + leg_shift, 61), 5)
        pygame.draw.line(sprite, outline, (x, 42), (x + leg_shift, 61), 1)
        pygame.draw.circle(sprite, bone, (x + leg_shift, 61), 4)
    pygame.draw.line(sprite, shadow, (53, 31), (63, 42), 4)
    pygame.draw.circle(sprite, bone, (63, 42), 3)
    return sprite


def generate_malice_robotic_dinosaur(frame: int) -> pygame.Surface:
    """Robotic skin Hunter's Rage dinosaur: metal dino chassis with panel lights."""
    sprite = make_surface()
    outline = (36, 39, 43)
    gray = (130, 133, 127)
    gray_dark = (71, 75, 77)
    pale = (206, 209, 201)
    red = (207, 76, 48)
    green = (55, 154, 91)
    leg_shift = (-2, 2, 0)[frame % 3]

    pygame.draw.polygon(sprite, gray, [(9, 31), (21, 23), (48, 23), (57, 35), (48, 48), (18, 47)])
    pygame.draw.polygon(sprite, outline, [(9, 31), (21, 23), (48, 23), (57, 35), (48, 48), (18, 47)], 2)
    pygame.draw.polygon(sprite, gray_dark, [(42, 14), (61, 19), (58, 34), (43, 31)])
    pygame.draw.polygon(sprite, outline, [(42, 14), (61, 19), (58, 34), (43, 31)], 2)
    pygame.draw.rect(sprite, red, pygame.Rect(49, 17, 6, 6), border_radius=1)
    pygame.draw.rect(sprite, green, pygame.Rect(54, 27, 4, 5), border_radius=1)
    pygame.draw.line(sprite, pale, (15, 32), (39, 32), 3)
    pygame.draw.polygon(sprite, gray_dark, [(11, 31), (0, 25), (4, 42)])
    pygame.draw.line(sprite, outline, (11, 31), (1, 25), 2)
    for x in (21, 32, 43):
        pygame.draw.line(sprite, outline, (x, 24), (x + 3, 47), 2)
    for x in (24, 43):
        pygame.draw.line(sprite, gray_dark, (x, 45), (x + leg_shift, 62), 6)
        pygame.draw.rect(sprite, gray, pygame.Rect(x + leg_shift - 5, 58, 12, 6), border_radius=2)
        pygame.draw.rect(sprite, outline, pygame.Rect(x + leg_shift - 5, 58, 12, 6), 1, border_radius=2)
    pygame.draw.line(sprite, gray_dark, (54, 33), (63, 43), 4)
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


def generate_vengance_scoreboard() -> pygame.Surface:
    """Scoreboard skin: sports scoreboard head, red uniform body, and basketball hand."""
    sprite = make_surface()
    outline = (38, 41, 43)
    gray = (118, 121, 121)
    dark = (42, 43, 44)
    yellow = (222, 199, 48)
    red = (174, 65, 58)
    white = (232, 232, 224)
    orange = (184, 122, 58)

    pygame.draw.polygon(sprite, dark, [(8, 7), (58, 4), (61, 29), (7, 30)])
    pygame.draw.polygon(sprite, outline, [(8, 7), (58, 4), (61, 29), (7, 30)], 2)
    pygame.draw.line(sprite, yellow, (34, 6), (34, 29), 3)
    for x in (15, 42):
        pygame.draw.rect(sprite, gray, pygame.Rect(x, 9, 13, 8), 1)
        pygame.draw.line(sprite, yellow, (x + 2, 12), (x + 10, 12), 1)
        pygame.draw.line(sprite, yellow, (x + 2, 15), (x + 9, 15), 1)
    pygame.draw.line(sprite, yellow, (17, 23), (25, 23), 2)
    pygame.draw.line(sprite, yellow, (44, 21), (52, 21), 2)
    pygame.draw.line(sprite, yellow, (44, 25), (52, 25), 2)
    pygame.draw.circle(sprite, (235, 232, 216), (49, 12), 2)

    draw_outline_rect(sprite, pygame.Rect(22, 30, 25, 30), white, outline, 4)
    pygame.draw.rect(sprite, red, pygame.Rect(24, 37, 21, 21), border_radius=2)
    pygame.draw.rect(sprite, white, pygame.Rect(30, 39, 8, 17), border_radius=1)
    pygame.draw.line(sprite, red, (32, 41), (38, 41), 2)
    pygame.draw.line(sprite, red, (32, 48), (38, 48), 2)
    pygame.draw.line(sprite, red, (32, 55), (38, 55), 2)

    pygame.draw.line(sprite, gray, (22, 39), (8, 48), 4)
    pygame.draw.circle(sprite, orange, (5, 47), 7)
    pygame.draw.arc(sprite, outline, pygame.Rect(-2, 40, 14, 14), 0.5, 5.8, 1)
    pygame.draw.line(sprite, outline, (5, 40), (5, 54), 1)
    pygame.draw.line(sprite, outline, (0, 47), (11, 47), 1)

    pygame.draw.line(sprite, gray, (46, 39), (58, 48), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(56, 45, 8, 5), border_radius=2)
    pygame.draw.line(sprite, gray, (29, 59), (28, 64), 4)
    pygame.draw.line(sprite, gray, (40, 59), (42, 64), 4)
    return sprite


def generate_vengance_spinning() -> pygame.Surface:
    """Spinning skin: pale Vengance Bot with smile marks and motion-ring hints."""
    sprite = make_surface()
    outline = (63, 65, 66)
    pale = (219, 220, 211)
    gray = (139, 141, 138)
    dark = (55, 57, 58)
    spin = (181, 185, 181)

    pygame.draw.polygon(sprite, pale, [(5, 6), (57, 4), (62, 29), (6, 32)])
    pygame.draw.polygon(sprite, outline, [(5, 6), (57, 4), (62, 29), (6, 32)], 2)
    pygame.draw.line(sprite, outline, (10, 18), (57, 16), 1)
    pygame.draw.line(sprite, outline, (21, 6), (21, 31), 1)
    pygame.draw.line(sprite, outline, (44, 6), (44, 29), 1)
    for x in (18, 34, 50):
        pygame.draw.arc(sprite, dark, pygame.Rect(x - 4, 12, 9, 9), 0.25, 2.9, 1)

    draw_outline_rect(sprite, pygame.Rect(21, 31, 27, 28), pale, outline, 4)
    for center in ((29, 38), (41, 38), (30, 48), (41, 51)):
        pygame.draw.circle(sprite, spin, center, 5, 1)
        pygame.draw.arc(sprite, dark, pygame.Rect(center[0] - 3, center[1] - 2, 6, 6), 0.2, 2.8, 1)

    pygame.draw.arc(sprite, spin, pygame.Rect(5, 22, 54, 35), 0.2, 5.8, 2)
    pygame.draw.arc(sprite, spin, pygame.Rect(2, 16, 60, 46), 3.5, 6.0, 2)
    pygame.draw.line(sprite, gray, (21, 40), (7, 50), 4)
    pygame.draw.line(sprite, gray, (48, 38), (60, 28), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(3, 47, 9, 5), border_radius=2)
    pygame.draw.rect(sprite, gray, pygame.Rect(57, 25, 7, 5), border_radius=2)
    pygame.draw.line(sprite, gray, (28, 59), (27, 64), 4)
    pygame.draw.line(sprite, gray, (42, 59), (45, 64), 4)
    return sprite


def generate_vengance_werewolf() -> pygame.Surface:
    """Werewolf skin: Vengance Bot body with wolf head, teeth, ears, and tail."""
    sprite = make_surface()
    outline = (36, 38, 38)
    gray = (151, 153, 145)
    dark = (54, 56, 56)
    pale = (222, 224, 213)

    pygame.draw.polygon(sprite, gray, [(4, 7), (58, 5), (61, 29), (4, 31)])
    pygame.draw.polygon(sprite, outline, [(4, 7), (58, 5), (61, 29), (4, 31)], 2)
    pygame.draw.polygon(sprite, dark, [(16, 20), (44, 20), (50, 29), (12, 29)])
    pygame.draw.polygon(sprite, gray, [(14, 18), (28, 7), (48, 14), (44, 25), (18, 27)])
    pygame.draw.polygon(sprite, gray, [(26, 7), (29, 0), (34, 8)])
    pygame.draw.polygon(sprite, gray, [(34, 9), (42, 2), (43, 15)])
    pygame.draw.polygon(sprite, outline, [(14, 18), (28, 7), (48, 14), (44, 25), (18, 27)], 2)
    pygame.draw.ellipse(sprite, pale, pygame.Rect(31, 12, 7, 9))
    pygame.draw.line(sprite, outline, (35, 14), (35, 19), 1)
    pygame.draw.polygon(sprite, dark, [(14, 18), (6, 22), (15, 25)])
    for x in range(18, 43, 6):
        pygame.draw.polygon(sprite, pale, [(x, 22), (x + 4, 22), (x + 2, 28)])

    draw_outline_rect(sprite, pygame.Rect(20, 31, 28, 28), dark, outline, 4)
    pygame.draw.line(sprite, gray, (20, 39), (7, 50), 4)
    pygame.draw.line(sprite, gray, (48, 38), (60, 28), 4)
    pygame.draw.rect(sprite, gray, pygame.Rect(3, 47, 9, 6), border_radius=2)
    pygame.draw.rect(sprite, gray, pygame.Rect(57, 25, 7, 6), border_radius=2)
    pygame.draw.polygon(sprite, gray, [(48, 47), (64, 40), (61, 53), (52, 56)])
    pygame.draw.line(sprite, outline, (49, 48), (62, 43), 1)
    pygame.draw.line(sprite, gray, (29, 58), (28, 64), 4)
    pygame.draw.line(sprite, gray, (42, 58), (44, 64), 4)
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
    pygame.display.set_mode((1, 1))
    save_if_missing("revenge_bot.png", generate_revenge_bot())
    save_if_missing("ducky_fried_chicken.png", generate_ducky_fried_chicken())
    save_if_missing("ducky_inverted.png", generate_ducky_inverted())
    save_if_missing("ducky_ogel.png", generate_ducky_ogel())
    save_if_missing("ducky_daddys_belt.png", generate_ducky_daddys_belt())
    save_if_missing("ducky_subject_5_png.png", generate_ducky_subject_5_png())
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
    save_if_missing("malice_bug.png", generate_malice_bug())
    save_if_missing("malice_bones.png", generate_malice_bones())
    save_if_missing("malice_robotic.png", generate_malice_robotic())
    for frame in range(3):
        save_if_missing(f"malice_tiger_{frame}.png", generate_malice_tiger(frame))
        save_if_missing(f"malice_bird_{frame}.png", generate_malice_bird(frame))
        save_if_missing(f"malice_dinosaur_{frame}.png", generate_malice_dinosaur(frame))
        save_animation_if_missing(
            f"malice_bug_dinosaur_{frame}.png",
            generate_malice_bug_dinosaur(frame),
        )
        save_animation_if_missing(
            f"malice_bones_dinosaur_{frame}.png",
            generate_malice_bones_dinosaur(frame),
        )
        save_animation_if_missing(
            f"malice_robotic_dinosaur_{frame}.png",
            generate_malice_robotic_dinosaur(frame),
        )
    save_if_missing("vengance_bot.png", generate_vengance_bot())
    save_if_missing("vengance_wick_wonalds.png", generate_vengance_wick_wonalds())
    save_if_missing("vengance_mlg.png", generate_vengance_mlg())
    save_if_missing("vengance_scoreboard.png", generate_vengance_scoreboard())
    save_if_missing("vengance_spinning.png", generate_vengance_spinning())
    save_if_missing("vengance_werewolf.png", generate_vengance_werewolf())
    save_if_missing("vengance_bot_mastery_1.png", generate_vengance_bot_mastery_1())
    save_if_missing("vengance_bot_mastery_2.png", generate_vengance_bot_mastery_2())
    save_if_missing("vengance_bot_mastery_3.png", generate_vengance_bot_mastery_3())
    save_if_missing("survivor.png", generate_survivor())
    save_if_missing("survivor_odd.png", generate_survivor_odd())
    save_if_missing("survivor_explorer.png", generate_survivor_explorer())
    save_if_missing("survivor_kitty.png", generate_survivor_kitty())
    save_if_missing("survivor_kevin.png", generate_survivor_kevin())
    save_if_missing("survivor_trashy.png", generate_survivor_trashy())
    save_if_missing("survivor_queen_goopy.png", generate_survivor_queen_goopy())
    generate_walk_animations()
    pygame.quit()


if __name__ == "__main__":
    main()

from __future__ import annotations

import pygame


def vector_from_keys(keys: pygame.key.ScancodeWrapper) -> pygame.Vector2:
    """Read WASD/arrow keys and return a normalized movement vector."""
    x = 0
    y = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x -= 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x += 1
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y += 1

    direction = pygame.Vector2(x, y)
    if direction.length_squared() > 0:
        direction = direction.normalize()
    return direction


def safe_normalize(vector: pygame.Vector2) -> pygame.Vector2:
    if vector.length_squared() == 0:
        return pygame.Vector2()
    return vector.normalize()


def facing_axis(facing: pygame.Vector2) -> pygame.Vector2:
    """Convert any facing direction into the strongest cardinal direction."""
    if facing.length_squared() == 0:
        return pygame.Vector2(0, 1)

    if abs(facing.x) > abs(facing.y):
        return pygame.Vector2(1 if facing.x > 0 else -1, 0)
    return pygame.Vector2(0, 1 if facing.y > 0 else -1)

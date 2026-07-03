from __future__ import annotations

import math
import random
from dataclasses import dataclass

import pygame

from tag.config.settings import *
from tag.data.content import KILLERS
from tag.ui.theme import COLORS, draw_button
from tag.utils.text import draw_text
from tag.utils.vector import facing_axis, safe_normalize


DIRECTIONAL_SPRITE_TILT_DEGREES = 35


@dataclass
class Wall:
    rect: pygame.Rect
    fill_color: tuple[int, int, int] = (67, 73, 85)
    border_color: tuple[int, int, int] = (126, 137, 151)
    drift: tuple[int, int] = (0, 0)
    drift_speed: float = 0.0
    drift_phase: float = 0.0
    spin_speed: float = 0.0
    spin_range: float = 0.0
    spin_phase: float = 0.0
    active_after: float = 0.0

    def __post_init__(self) -> None:
        self.home_rect = self.rect.copy()
        self.elapsed = 0.0
        self.angle = 0.0
        self.base_size = self.home_rect.size

    def update(self, dt: float) -> bool:
        self.elapsed += dt
        if self.elapsed < self.active_after:
            self.rect = self.home_rect.copy()
            self.angle = 0.0
            return False

        moving = self.drift != (0, 0) and abs(self.drift_speed) > 0
        rotating = abs(self.spin_speed) > 0 and self.spin_range > 0
        if not moving and not rotating:
            return False

        center = pygame.Vector2(self.home_rect.center)
        if moving:
            self.drift_phase += dt * self.drift_speed
            amount = math.sin(self.drift_phase)
            center.x += self.drift[0] * amount
            center.y += self.drift[1] * amount

        if rotating:
            self.spin_phase += dt * self.spin_speed
            self.angle = math.sin(self.spin_phase) * self.spin_range
        else:
            self.angle = 0.0

        radians = math.radians(self.angle)
        sin_angle = abs(math.sin(radians))
        cos_angle = abs(math.cos(radians))
        base_width, base_height = self.base_size
        self.rect.size = (
            max(1, round(base_width * cos_angle + base_height * sin_angle)),
            max(1, round(base_width * sin_angle + base_height * cos_angle)),
        )
        self.rect.center = (round(center.x), round(center.y))

        if not ARENA_RECT.contains(self.rect):
            self.rect.clamp_ip(ARENA_RECT)
            if moving:
                self.drift_speed *= -1
            if rotating:
                self.spin_speed *= -1
        return True

    def draw(self, surface: pygame.Surface) -> None:
        if abs(self.angle) < 0.5:
            pygame.draw.rect(surface, self.fill_color, self.rect, border_radius=6)
            pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=6)
            return

        wall_surface = pygame.Surface(self.base_size, pygame.SRCALPHA)
        base_rect = wall_surface.get_rect()
        pygame.draw.rect(wall_surface, self.fill_color, base_rect, border_radius=6)
        pygame.draw.rect(wall_surface, self.border_color, base_rect, 2, border_radius=6)
        rotated = pygame.transform.rotate(wall_surface, self.angle)
        rotated_rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rotated_rect)


class Button:
    def __init__(self, rect: pygame.Rect, text: str) -> None:
        self.rect = rect
        self.text = text

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        active: bool = False,
    ) -> None:
        draw_button(surface, font, self.rect, self.text, active)

    def contains(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)


class AttackHitbox:
    def __init__(
        self,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        alpha: int,
        label: str,
    ) -> None:
        self.rect = rect
        self.color = color
        self.alpha = alpha
        self.label = label

    def draw(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        overlay.fill((*self.color, self.alpha))
        pygame.draw.rect(overlay, (*self.color, 230), overlay.get_rect(), 3, border_radius=7)
        surface.blit(overlay, self.rect.topleft)


class IceProjectile:
    def __init__(
        self,
        pos: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float,
        lifetime: float,
        effect: str,
        homing: bool = False,
    ) -> None:
        self.pos = pygame.Vector2(pos)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, 1)

        self.speed = speed
        self.lifetime = lifetime
        self.effect = effect
        self.homing = homing
        self.rect = pygame.Rect(0, 0, 18 if not homing else 22, 18 if not homing else 22)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, target: Character | None, walls: list[Wall]) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False

        if self.homing and target is not None:
            desired = safe_normalize(target.pos - self.pos)
            if desired.length_squared() > 0:
                self.direction = desired

        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not ARENA_RECT.colliderect(self.rect):
            return False

        if not self.homing:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    return False

        return True

    def draw(self, surface: pygame.Surface) -> None:
        if self.homing:
            pygame.draw.rect(surface, (157, 219, 255), self.rect, border_radius=5)
            pygame.draw.rect(surface, (231, 247, 255), self.rect, 2, border_radius=5)
            return

        pygame.draw.polygon(
            surface,
            (173, 232, 255),
            [
                self.rect.midtop,
                self.rect.midright,
                self.rect.midbottom,
                self.rect.midleft,
            ],
        )
        pygame.draw.rect(surface, (231, 247, 255), self.rect, 2, border_radius=4)


class DuckyBelt:
    """A short-lived metal belt projectile with a mace hitbox at the end."""

    def __init__(
        self,
        origin: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float,
        lifetime: float,
        belt_only: bool = False,
    ) -> None:
        self.origin = pygame.Vector2(origin)
        self.pos = pygame.Vector2(origin)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, 1)

        self.speed = speed
        self.lifetime = lifetime
        self.belt_only = belt_only
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, walls: list[Wall]) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False

        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not ARENA_RECT.colliderect(self.rect):
            return False

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                return False

        return True

    def draw(self, surface: pygame.Surface) -> None:
        belt_color = (126, 87, 55) if self.belt_only else (170, 174, 184)
        belt_edge = (69, 45, 31) if self.belt_only else (58, 63, 73)
        buckle = (229, 198, 96) if self.belt_only else (226, 232, 240)

        pygame.draw.line(surface, belt_color, self.origin, self.pos, 8)
        pygame.draw.line(surface, belt_edge, self.origin, self.pos, 2)
        if self.belt_only:
            buckle_rect = pygame.Rect(0, 0, 22, 14)
            buckle_rect.center = self.rect.center
            pygame.draw.rect(surface, belt_color, buckle_rect, border_radius=3)
            pygame.draw.rect(surface, buckle, buckle_rect, 3, border_radius=3)
            pygame.draw.rect(surface, belt_edge, buckle_rect.inflate(-9, -6), 2, border_radius=2)
            return

        pygame.draw.circle(surface, (116, 122, 134), self.rect.center, 15)
        pygame.draw.circle(surface, buckle, self.rect.center, 15, 3)
        for angle in (0, math.pi / 2, math.pi, math.pi * 1.5):
            spike = pygame.Vector2(math.cos(angle), math.sin(angle))
            start = pygame.Vector2(self.rect.center) + spike * 10
            end = pygame.Vector2(self.rect.center) + spike * 19
            pygame.draw.line(surface, (226, 232, 240), start, end, 3)


class VenganceLandmine:
    """A visible mine that wins the round if the survivor steps on it."""

    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(0, 0, 42, 42)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, (88, 24, 24), self.rect.center, 21)
        pygame.draw.circle(surface, (248, 113, 113), self.rect.center, 21, 3)
        pygame.draw.circle(surface, (250, 204, 21), self.rect.center, 7)
        pygame.draw.line(surface, (15, 23, 42), self.rect.midleft, self.rect.midright, 2)
        pygame.draw.line(surface, (15, 23, 42), self.rect.midtop, self.rect.midbottom, 2)


class SurvivorShot:
    """Trashy's earned homing shot. It stuns a killer instead of ending the round."""

    def __init__(self, origin: pygame.Vector2, direction: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(origin)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, -1)
        self.lifetime = TRASHY_GUN_SHOT_LIFETIME
        self.rect = pygame.Rect(0, 0, 22, 12)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, target: Character | None) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False
        if target is not None:
            desired = safe_normalize(target.pos - self.pos)
            if desired.length_squared() > 0:
                turn_amount = min(1.0, TRASHY_GUN_HOMING_STRENGTH * dt)
                curved_direction = self.direction + (desired - self.direction) * turn_amount
                self.direction = safe_normalize(curved_direction)
                if self.direction.length_squared() == 0:
                    self.direction = desired
        self.pos += self.direction * TRASHY_GUN_SHOT_SPEED * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not ARENA_RECT.colliderect(self.rect):
            return False
        return True

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (239, 68, 68), self.rect, border_radius=6)
        pygame.draw.rect(surface, (254, 226, 226), self.rect, 2, border_radius=6)


class TrashyShockWave:
    """Trashy's cannon blast: stun, knock back, and burn down the timer."""

    def __init__(self, origin: pygame.Vector2, direction: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(origin)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, -1)
        self.lifetime = TRASHY_SHOCK_SHOT_LIFETIME
        self.rect = pygame.Rect(0, 0, 42, 30)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, walls: list[Wall]) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False
        self.pos += self.direction * TRASHY_SHOCK_SHOT_SPEED * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not ARENA_RECT.colliderect(self.rect):
            return False
        return not any(self.rect.colliderect(wall.rect) for wall in walls)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(surface, (248, 113, 113), self.rect)
        pygame.draw.ellipse(surface, (254, 226, 226), self.rect, 3)
        core = self.rect.inflate(-16, -10)
        pygame.draw.ellipse(surface, (251, 191, 36), core)


class TrashyTurretShot:
    """A small turret bullet that stuns the killer on contact."""

    def __init__(self, origin: pygame.Vector2, direction: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(origin)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, -1)
        self.lifetime = TRASHY_TURRET_SHOT_LIFETIME
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, walls: list[Wall]) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False
        self.pos += self.direction * TRASHY_TURRET_SHOT_SPEED * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not ARENA_RECT.colliderect(self.rect):
            return False
        return not any(self.rect.colliderect(wall.rect) for wall in walls)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, (125, 211, 252), self.rect.center, 8)
        pygame.draw.circle(surface, (224, 242, 254), self.rect.center, 8, 2)


class TrashyTurret:
    """Stationary turret placed by Trashy that fires when a killer enters range."""

    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(0, 0, 36, 36)
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.lifetime = TRASHY_TURRET_DURATION
        self.fire_cooldown = 0.25

    def update(self, dt: float, killers: list[Killer]) -> TrashyTurretShot | None:
        self.lifetime -= dt
        self.fire_cooldown = max(0.0, self.fire_cooldown - dt)
        if self.lifetime <= 0 or self.fire_cooldown > 0 or not killers:
            return None

        nearby = [
            killer
            for killer in killers
            if killer.pos.distance_to(self.pos) <= TRASHY_TURRET_RANGE
        ]
        if not nearby:
            return None

        target = min(nearby, key=lambda killer: killer.pos.distance_to(self.pos))
        self.fire_cooldown = TRASHY_TURRET_FIRE_COOLDOWN
        return TrashyTurretShot(self.pos, target.pos - self.pos)

    def alive(self) -> bool:
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, (30, 41, 59), self.rect.center, TRASHY_TURRET_RANGE, 1)
        pygame.draw.rect(surface, (55, 65, 81), self.rect, border_radius=8)
        pygame.draw.rect(surface, (203, 213, 225), self.rect, 2, border_radius=8)
        barrel = pygame.Rect(0, 0, 12, 30)
        barrel.center = (self.rect.centerx, self.rect.top + 4)
        pygame.draw.rect(surface, (239, 68, 68), barrel, border_radius=4)
        pygame.draw.circle(surface, (96, 165, 250), self.rect.center, 7)


class MaliceBirdPoop:
    """Bird-form projectile that briefly stuns the survivor on hit."""

    def __init__(self, origin: pygame.Vector2, direction: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(origin)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, 1)
        self.lifetime = MALICE_BIRD_POOP_LIFETIME
        self.rect = pygame.Rect(0, 0, 18, 18)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, walls: list[Wall]) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False

        self.pos += self.direction * MALICE_BIRD_POOP_SPEED * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not ARENA_RECT.colliderect(self.rect):
            return False
        return not any(self.rect.colliderect(wall.rect) for wall in walls)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, (248, 250, 252), self.rect.center, 9)
        pygame.draw.circle(surface, (148, 163, 184), self.rect.center, 9, 2)
        pygame.draw.circle(surface, (255, 255, 255), (self.rect.centerx - 3, self.rect.centery - 3), 3)


class MaliceHelperBird:
    """Small bird helper that flies randomly and slows the survivor on contact."""

    def __init__(self, pos: pygame.Vector2, offset: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(pos) + offset
        self.rect = pygame.Rect(0, 0, 28, 22)
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.lifetime = MALICE_HUNTER_RAGE_DURATION
        self.direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        self.turn_timer = random.uniform(0.35, 0.85)

    def update(self, dt: float) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False

        self.turn_timer -= dt
        if self.turn_timer <= 0:
            self.direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
            self.turn_timer = random.uniform(0.35, 0.85)

        self.pos += safe_normalize(self.direction) * 245 * dt
        if self.pos.x < ARENA_RECT.left or self.pos.x > ARENA_RECT.right:
            self.direction.x *= -1
        if self.pos.y < ARENA_RECT.top or self.pos.y > ARENA_RECT.bottom:
            self.direction.y *= -1
        self.pos.x = max(ARENA_RECT.left + 10, min(ARENA_RECT.right - 10, self.pos.x))
        self.pos.y = max(ARENA_RECT.top + 10, min(ARENA_RECT.bottom - 10, self.pos.y))
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        return True

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(surface, (57, 169, 216), self.rect)
        pygame.draw.ellipse(surface, (15, 23, 42), self.rect, 2)
        pygame.draw.polygon(
            surface,
            (201, 119, 63),
            [
                (self.rect.centerx - 4, self.rect.top),
                (self.rect.centerx - 18, self.rect.top - 10),
                (self.rect.centerx - 8, self.rect.centery),
            ],
        )
        pygame.draw.polygon(
            surface,
            (250, 204, 21),
            [
                self.rect.midright,
                (self.rect.right + 9, self.rect.centery - 4),
                (self.rect.right + 9, self.rect.centery + 4),
            ],
        )


class GoopyKnight:
    """Queen Goopy summon that runs to the nearest killer and stuns on contact."""

    def __init__(self, pos: pygame.Vector2, offset: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(pos) + offset
        self.rect = pygame.Rect(0, 0, 28, 34)
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.lifetime = 7.0

    def update(self, dt: float, killers: list[Killer]) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0 or not killers:
            return False

        nearest = min(killers, key=lambda killer: killer.pos.distance_to(self.pos))
        direction = safe_normalize(nearest.pos - self.pos)
        self.pos += direction * QUEEN_GOOPY_KNIGHT_SPEED * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        return ARENA_RECT.colliderect(self.rect)

    def draw(self, surface: pygame.Surface) -> None:
        body = pygame.Rect(0, 0, 22, 25)
        body.center = (self.rect.centerx, self.rect.centery + 5)
        pygame.draw.rect(surface, (148, 163, 184), body, border_radius=5)
        pygame.draw.rect(surface, (51, 65, 85), body, 2, border_radius=5)
        pygame.draw.circle(surface, (203, 213, 225), (self.rect.centerx, self.rect.top + 8), 9)
        pygame.draw.circle(surface, (51, 65, 85), (self.rect.centerx, self.rect.top + 8), 9, 2)


class Character:
    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        speed: float,
        color: tuple[int, int, int],
        sprite: pygame.Surface | None = None,
        walk_frames: list[pygame.Surface] | None = None,
    ) -> None:
        self.name = name
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.color = color
        self.sprite = sprite
        self.base_sprite = sprite
        self.walk_frames = walk_frames or []
        self.walk_animation_timer = 0.0
        self.walk_animation_index = 0
        self.is_moving = False
        self.sprite_alpha = 255
        self.facing = pygame.Vector2(0, 1)
        self.directional_sprite_cache: dict[tuple[int, bool, int], pygame.Surface] = {}
        self.rect = pygame.Rect(0, 0, CHARACTER_COLLISION_SIZE, CHARACTER_COLLISION_SIZE)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        self.ai_nudge = pygame.Vector2()
        self.ai_nudge_timer = 0.0

    def update_rect(self) -> None:
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def move(
        self,
        direction: pygame.Vector2,
        dt: float,
        walls: list[Wall],
        arena: pygame.Rect,
        speed: float | None = None,
    ) -> bool:
        if direction.length_squared() == 0:
            return False

        direction = direction.normalize()
        self.facing = direction
        self.is_moving = True
        self.advance_walk_animation(dt)

        move_speed = speed if speed is not None else self.speed
        delta = direction * move_speed * dt
        blocked_x = self._move_axis(delta.x, 0, walls, arena)
        blocked_y = self._move_axis(0, delta.y, walls, arena)
        return blocked_x or blocked_y

    def advance_walk_animation(self, dt: float) -> None:
        if not self.walk_frames:
            return

        self.walk_animation_timer += dt
        if self.walk_animation_timer < WALK_ANIMATION_SPEED:
            return

        self.walk_animation_timer = 0.0
        self.walk_animation_index = (self.walk_animation_index + 1) % len(self.walk_frames)

    def _move_axis(
        self,
        dx: float,
        dy: float,
        walls: list[Wall],
        arena: pygame.Rect,
    ) -> bool:
        if dx == 0 and dy == 0:
            return False

        self.pos.x += dx
        self.pos.y += dy
        self.update_rect()
        blocked = False

        if self.rect.left < arena.left:
            self.rect.left = arena.left
            blocked = True
        if self.rect.right > arena.right:
            self.rect.right = arena.right
            blocked = True
        if self.rect.top < arena.top:
            self.rect.top = arena.top
            blocked = True
        if self.rect.bottom > arena.bottom:
            self.rect.bottom = arena.bottom
            blocked = True

        if blocked:
            self.pos.update(self.rect.center)

        for wall in walls:
            if not self.rect.colliderect(wall.rect):
                continue

            blocked = True
            if dx > 0:
                self.rect.right = wall.rect.left
            elif dx < 0:
                self.rect.left = wall.rect.right
            elif dy > 0:
                self.rect.bottom = wall.rect.top
            elif dy < 0:
                self.rect.top = wall.rect.bottom
            self.pos.update(self.rect.center)

        return blocked

    def apply_ai_nudge(self, desired: pygame.Vector2, dt: float) -> pygame.Vector2:
        if self.ai_nudge_timer > 0:
            self.ai_nudge_timer = max(0.0, self.ai_nudge_timer - dt)
            desired += self.ai_nudge * 0.85
        return desired

    def choose_ai_nudge(self) -> None:
        angle = random.uniform(0, math.tau)
        self.ai_nudge = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.ai_nudge_timer = random.uniform(0.25, 0.55)

    def directional_sprite_bucket(self) -> tuple[bool, int]:
        facing = safe_normalize(self.facing)
        if facing.length_squared() == 0:
            return False, 0

        mirrored = facing.x < -0.01
        angle = 0
        if facing.y < -0.01:
            angle = -DIRECTIONAL_SPRITE_TILT_DEGREES if mirrored else DIRECTIONAL_SPRITE_TILT_DEGREES
        elif facing.y > 0.01:
            angle = DIRECTIONAL_SPRITE_TILT_DEGREES if mirrored else -DIRECTIONAL_SPRITE_TILT_DEGREES
        return mirrored, angle

    def directional_sprite(self, sprite: pygame.Surface) -> pygame.Surface:
        mirrored, angle = self.directional_sprite_bucket()
        cache_key = (id(sprite), mirrored, angle)
        cached = self.directional_sprite_cache.get(cache_key)
        if cached is not None:
            return cached

        transformed = pygame.transform.flip(sprite, True, False) if mirrored else sprite
        if angle != 0:
            transformed = pygame.transform.rotozoom(transformed, angle, 1.0)
        self.directional_sprite_cache[cache_key] = transformed
        return transformed

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, label_alpha: int = 255) -> None:
        draw_rect = pygame.Rect(0, 0, SPRITE_DRAW_SIZE, SPRITE_DRAW_SIZE)
        draw_rect.center = self.rect.center

        sprite = self.sprite
        if self.walk_frames and self.is_moving and self.sprite is self.base_sprite:
            sprite = self.walk_frames[self.walk_animation_index % len(self.walk_frames)]

        if sprite is not None:
            sprite = self.directional_sprite(sprite)
            sprite_rect = sprite.get_rect(center=draw_rect.center)
            if self.sprite_alpha < 255:
                faded = sprite.copy()
                faded.set_alpha(self.sprite_alpha)
                surface.blit(faded, sprite_rect)
            else:
                surface.blit(sprite, sprite_rect)
        else:
            pygame.draw.ellipse(surface, self.color, draw_rect)
            pygame.draw.ellipse(surface, (15, 23, 42), draw_rect, 3)

        self.draw_name_label(surface, font, label_alpha)
        self.is_moving = False

    def draw_name_label(self, surface: pygame.Surface, font: pygame.font.Font, alpha: int = 255) -> None:
        alpha = max(0, min(255, alpha))
        if alpha <= 0:
            return

        label = font.render(self.name, True, COLORS["text_soft"])
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.top - 11))
        backing = label_rect.inflate(12, 6)
        border_radius = backing.height // 2

        if alpha >= 255:
            pygame.draw.rect(surface, COLORS["bg"], backing, border_radius=border_radius)
            pygame.draw.rect(surface, COLORS["border_soft"], backing, 1, border_radius=border_radius)
            surface.blit(label, label_rect)
            return

        label_layer = pygame.Surface(backing.size, pygame.SRCALPHA)
        local_backing = label_layer.get_rect()
        pygame.draw.rect(label_layer, (*COLORS["bg"], alpha), local_backing, border_radius=border_radius)
        pygame.draw.rect(
            label_layer,
            (*COLORS["border_soft"], alpha),
            local_backing,
            1,
            border_radius=border_radius,
        )
        label.set_alpha(alpha)
        label_layer.blit(label, label_rect.move(-backing.left, -backing.top))
        surface.blit(label_layer, backing)


class Survivor(Character):
    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        sprite: pygame.Surface | None = None,
        survivor_id: str = "survivor",
        walk_frames: list[pygame.Surface] | None = None,
    ) -> None:
        super().__init__(name, pos, SURVIVOR_SPEED, (61, 145, 255), sprite, walk_frames)
        self.survivor_id = survivor_id
        self.odd_flash_used = False
        self.odd_flash_cooldown = 0.0
        self.explorer_adrenaline_used = False
        self.explorer_adrenaline_timer = 0.0
        self.explorer_ability_cooldown = 0.0
        self.kitty_marker: pygame.Vector2 | None = None
        self.kitty_teleport_used = False
        self.queen_knights_used = False
        self.queen_knights_cooldown = 0.0
        self.trashy_minigame_active = False
        self.trashy_gun_ready = False
        self.trashy_gun_used = False
        self.trashy_shock_cooldown = 0.0
        self.trashy_turret_cooldown = 0.0
        self.trashy_hits = 0
        self.trashy_target_x = float(TRASHY_MINIGAME_BAR.centerx)
        self.trashy_circle_x = float(TRASHY_MINIGAME_BAR.left + TRASHY_MINIGAME_CIRCLE_RADIUS)
        self.trashy_circle_direction = 1
        self.kevin_punch_used = False
        self.kevin_punch_timer = 0.0
        self.kevin_punch_cooldown = 0.0
        self.kevin_speed_used = False
        self.kevin_speed_timer = 0.0

    def update_abilities(self, dt: float) -> None:
        if self.odd_flash_cooldown > 0:
            self.odd_flash_cooldown = max(0.0, self.odd_flash_cooldown - dt)
        if self.explorer_adrenaline_timer > 0:
            self.explorer_adrenaline_timer = max(0.0, self.explorer_adrenaline_timer - dt)
        if self.explorer_ability_cooldown > 0:
            self.explorer_ability_cooldown = max(0.0, self.explorer_ability_cooldown - dt)
        if self.queen_knights_cooldown > 0:
            self.queen_knights_cooldown = max(0.0, self.queen_knights_cooldown - dt)
        if self.trashy_shock_cooldown > 0:
            self.trashy_shock_cooldown = max(0.0, self.trashy_shock_cooldown - dt)
        if self.trashy_turret_cooldown > 0:
            self.trashy_turret_cooldown = max(0.0, self.trashy_turret_cooldown - dt)
        if self.kevin_punch_timer > 0:
            self.kevin_punch_timer = max(0.0, self.kevin_punch_timer - dt)
        if self.kevin_punch_cooldown > 0:
            self.kevin_punch_cooldown = max(0.0, self.kevin_punch_cooldown - dt)
        if self.kevin_speed_timer > 0:
            self.kevin_speed_timer = max(0.0, self.kevin_speed_timer - dt)

        if self.trashy_minigame_active:
            self.trashy_circle_x += (
                self.trashy_circle_direction * TRASHY_MINIGAME_CIRCLE_SPEED * dt
            )
            left = TRASHY_MINIGAME_BAR.left + TRASHY_MINIGAME_CIRCLE_RADIUS
            right = TRASHY_MINIGAME_BAR.right - TRASHY_MINIGAME_CIRCLE_RADIUS
            if self.trashy_circle_x <= left:
                self.trashy_circle_x = float(left)
                self.trashy_circle_direction = 1
            elif self.trashy_circle_x >= right:
                self.trashy_circle_x = float(right)
                self.trashy_circle_direction = -1

    def current_speed(self) -> float:
        speed = self.speed
        if self.explorer_adrenaline_timer > 0:
            speed *= EXPLORER_ADRENALINE_SPEED_MULTIPLIER
        if self.kevin_speed_timer > 0:
            speed *= KEVIN_DOUBLE_SPEED_MULTIPLIER
        return speed

    def is_invincible(self) -> bool:
        return self.explorer_adrenaline_timer > 0

    def set_trashy_target(self) -> None:
        target_width = round(TRASHY_MINIGAME_TARGET_SIZE * 1.5)
        padding = target_width // 2 + 4
        self.trashy_target_x = float(
            random.randint(TRASHY_MINIGAME_BAR.left + padding, TRASHY_MINIGAME_BAR.right - padding)
        )

    def trashy_target_rect(self) -> pygame.Rect:
        target_width = round(TRASHY_MINIGAME_TARGET_SIZE * 1.5)
        rect = pygame.Rect(0, 0, target_width, TRASHY_MINIGAME_TARGET_SIZE)
        rect.center = (round(self.trashy_target_x), TRASHY_MINIGAME_BAR.centery)
        return rect

    def trashy_circle_rect(self) -> pygame.Rect:
        radius = TRASHY_MINIGAME_CIRCLE_RADIUS
        rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        rect.center = (round(self.trashy_circle_x), TRASHY_MINIGAME_BAR.centery)
        return rect


class Killer(Character):
    BASE_MALICE_FORMS = ("tiger", "bird", "dinosaur")
    MALICE_SKIN_DINOSAUR_FORMS = {
        "malice_bug": "bug_dinosaur",
        "malice_bones": "bones_dinosaur",
        "malice_robotic": "robotic_dinosaur",
    }
    MALICE_DINOSAUR_FORMS = (
        "dinosaur",
        *MALICE_SKIN_DINOSAUR_FORMS.values(),
    )

    def __init__(
        self,
        killer_id: str,
        name: str,
        pos: tuple[int, int],
        sprite: pygame.Surface | None = None,
        skin_id: str = "classic",
        walk_frames: list[pygame.Surface] | None = None,
    ) -> None:
        self.killer_id = killer_id
        self.data = KILLERS[killer_id]
        self.skin_id = skin_id
        super().__init__(name, pos, self.data["speed"], self.data["color"], sprite, walk_frames)
        self.attack_phase: str | None = None
        self.attack_timer = 0.0
        self.cooldown_remaining = 0.0
        self.wall_phase_timer = 0.0
        self.wall_phase_cooldown = 0.0
        self.show_power_timer = 0.0
        self.show_power_cooldown = 0.0
        self.show_slow_cooldown = 0.0
        self.show_hook_cooldown = 0.0
        self.subslasher_freeze_cooldown = 0.0
        self.subslasher_kill_cooldown = 0.0
        self.subslasher_subzero_cooldown = 0.0
        self.ducky_swing_cooldown = 0.0
        self.ducky_hg_timer = 0.0
        self.ducky_hg_cooldown = 0.0
        self.vengance_dash_timer = 0.0
        self.vengance_dash_cooldown = 0.0
        self.vengance_dash_direction = pygame.Vector2(0, 1)
        self.vengance_mine_cooldown = 0.0
        self.ai_stun_timer = 0.0
        self.malice_form: str | None = None
        self.malice_form_timer = 0.0
        self.malice_hunter_cooldown = 0.0
        self.malice_animation_index = 0
        self.malice_animation_timer = 0.0
        self.tiger_invisible_timer = 0.0
        self.tiger_invisible_cooldown = 0.0
        self.bird_summon_cooldown = 0.0
        self.bird_poop_cooldown = 0.0
        self.dinosaur_stomp_cooldown = 0.0
        self.dinosaur_roar_cooldown = 0.0

    def can_attack(self) -> bool:
        return self.attack_phase is None and self.cooldown_remaining <= 0

    def is_ducky(self) -> bool:
        return self.killer_id == "revenge_bot"

    def is_malice(self) -> bool:
        return self.killer_id == "malice"

    def is_hunter_rage_active(self) -> bool:
        return self.is_malice() and self.malice_form is not None and self.malice_form_timer > 0

    def is_malice_tiger(self) -> bool:
        return self.is_hunter_rage_active() and self.malice_form == "tiger"

    def is_malice_bird(self) -> bool:
        return self.is_hunter_rage_active() and self.malice_form == "bird"

    def is_malice_dinosaur(self) -> bool:
        return self.is_hunter_rage_active() and self.malice_form in self.MALICE_DINOSAUR_FORMS

    def is_subslasher(self) -> bool:
        return self.killer_id == "subslasher"

    def is_show_runner(self) -> bool:
        return self.killer_id == "show_runner"

    def is_vengance_bot(self) -> bool:
        return self.killer_id == "vengance_bot"

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, label_alpha: int = 255) -> None:
        if self.skin_id != "vengance_spinning" or self.sprite is None:
            super().draw(surface, font, label_alpha)
            self.draw_stun_effect(surface, font)
            return

        draw_rect = pygame.Rect(0, 0, SPRITE_DRAW_SIZE, SPRITE_DRAW_SIZE)
        draw_rect.center = self.rect.center
        angle = (pygame.time.get_ticks() * 0.36) % 360
        rotated = pygame.transform.rotozoom(self.sprite, angle, 1.0)
        rotated_rect = rotated.get_rect(center=draw_rect.center)
        surface.blit(rotated, rotated_rect)

        pygame.draw.circle(surface, (226, 232, 240), self.rect.center, 34, 2)
        for spin_angle in (angle, angle + 120, angle + 240):
            direction = pygame.Vector2(1, 0).rotate(spin_angle)
            start = pygame.Vector2(self.rect.center) + direction * 24
            end = pygame.Vector2(self.rect.center) + direction * 35
            pygame.draw.line(surface, (226, 232, 240), start, end, 3)

        self.draw_name_label(surface, font, label_alpha)
        self.draw_stun_effect(surface, font)

    def draw_stun_effect(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        if self.ai_stun_timer <= 0:
            return
        pygame.draw.circle(surface, (250, 204, 21), self.rect.center, 38, 3)
        text = font.render(f"STUN {self.ai_stun_timer:.1f}", True, (254, 240, 138))
        surface.blit(text, text.get_rect(center=(self.rect.centerx, self.rect.bottom + 14)))

    def is_wall_phasing(self) -> bool:
        return self.is_malice() and self.wall_phase_timer > 0

    def start_wall_phase(self) -> bool:
        if not self.is_malice() or self.wall_phase_timer > 0 or self.wall_phase_cooldown > 0:
            return False

        self.wall_phase_timer = MALICE_WALL_PHASE_DURATION
        return True

    def update_abilities(self, dt: float) -> None:
        if self.malice_hunter_cooldown > 0:
            self.malice_hunter_cooldown = max(0.0, self.malice_hunter_cooldown - dt)

        if self.malice_form_timer > 0:
            self.malice_form_timer = max(0.0, self.malice_form_timer - dt)
            if self.malice_form_timer == 0:
                self.end_hunter_rage()

        if self.tiger_invisible_timer > 0:
            self.tiger_invisible_timer = max(0.0, self.tiger_invisible_timer - dt)
            if self.tiger_invisible_timer == 0:
                self.tiger_invisible_cooldown = MALICE_FORM_ABILITY_COOLDOWN
                self.sprite_alpha = 255
        elif self.tiger_invisible_cooldown > 0:
            self.tiger_invisible_cooldown = max(0.0, self.tiger_invisible_cooldown - dt)

        if self.bird_summon_cooldown > 0:
            self.bird_summon_cooldown = max(0.0, self.bird_summon_cooldown - dt)
        if self.bird_poop_cooldown > 0:
            self.bird_poop_cooldown = max(0.0, self.bird_poop_cooldown - dt)
        if self.dinosaur_stomp_cooldown > 0:
            self.dinosaur_stomp_cooldown = max(0.0, self.dinosaur_stomp_cooldown - dt)
        if self.dinosaur_roar_cooldown > 0:
            self.dinosaur_roar_cooldown = max(0.0, self.dinosaur_roar_cooldown - dt)

        if self.wall_phase_timer > 0:
            self.wall_phase_timer = max(0.0, self.wall_phase_timer - dt)
            if self.wall_phase_timer == 0:
                self.wall_phase_cooldown = MALICE_WALL_PHASE_COOLDOWN
        elif self.wall_phase_cooldown > 0:
            self.wall_phase_cooldown = max(0.0, self.wall_phase_cooldown - dt)

        if self.show_power_timer > 0:
            self.show_power_timer = max(0.0, self.show_power_timer - dt)
            if self.show_power_timer == 0:
                self.show_power_cooldown = SHOW_RUNNER_SPEED_COOLDOWN
        elif self.show_power_cooldown > 0:
            self.show_power_cooldown = max(0.0, self.show_power_cooldown - dt)
        if self.show_slow_cooldown > 0:
            self.show_slow_cooldown = max(0.0, self.show_slow_cooldown - dt)
        if self.show_hook_cooldown > 0:
            self.show_hook_cooldown = max(0.0, self.show_hook_cooldown - dt)
        if self.subslasher_freeze_cooldown > 0:
            self.subslasher_freeze_cooldown = max(0.0, self.subslasher_freeze_cooldown - dt)
        if self.subslasher_kill_cooldown > 0:
            self.subslasher_kill_cooldown = max(0.0, self.subslasher_kill_cooldown - dt)
        if self.subslasher_subzero_cooldown > 0:
            self.subslasher_subzero_cooldown = max(0.0, self.subslasher_subzero_cooldown - dt)

        if self.ducky_swing_cooldown > 0:
            self.ducky_swing_cooldown = max(0.0, self.ducky_swing_cooldown - dt)

        if self.ducky_hg_timer > 0:
            self.ducky_hg_timer = max(0.0, self.ducky_hg_timer - dt)
            if self.ducky_hg_timer == 0:
                self.ducky_hg_cooldown = DUCKY_HG_COOLDOWN
        elif self.ducky_hg_cooldown > 0:
            self.ducky_hg_cooldown = max(0.0, self.ducky_hg_cooldown - dt)

        if self.vengance_dash_timer > 0:
            self.vengance_dash_timer = max(0.0, self.vengance_dash_timer - dt)
            if self.vengance_dash_timer == 0:
                self.vengance_dash_cooldown = VENGANCE_DASH_COOLDOWN
        elif self.vengance_dash_cooldown > 0:
            self.vengance_dash_cooldown = max(0.0, self.vengance_dash_cooldown - dt)

        if self.vengance_mine_cooldown > 0:
            self.vengance_mine_cooldown = max(0.0, self.vengance_mine_cooldown - dt)

    def wall_phase_status(self) -> str:
        if not self.is_malice():
            return ""
        if self.wall_phase_timer > 0:
            return f"I: phasing {self.wall_phase_timer:.1f}s"
        if self.wall_phase_cooldown > 0:
            return f"I: cooldown {self.wall_phase_cooldown:.0f}s"
        return "I: phase ready"

    def hunter_rage_forms(self, selected_skin: str | None = None) -> tuple[str, ...]:
        forms = list(self.BASE_MALICE_FORMS)
        skin_id = selected_skin if selected_skin is not None else self.skin_id
        skin_form = self.MALICE_SKIN_DINOSAUR_FORMS.get(skin_id)
        if skin_form is not None:
            forms.append(skin_form)
        return tuple(forms)

    def start_hunter_rage(self, selected_skin: str | None = None) -> str | None:
        if not self.is_malice() or self.is_hunter_rage_active() or self.malice_hunter_cooldown > 0:
            return None

        self.malice_form = random.choice(self.hunter_rage_forms(selected_skin))
        self.malice_form_timer = MALICE_HUNTER_RAGE_DURATION
        self.malice_animation_index = 0
        self.malice_animation_timer = 0.0
        self.sprite_alpha = 255
        self.tiger_invisible_timer = 0.0
        self.tiger_invisible_cooldown = 0.0
        self.bird_summon_cooldown = 0.0
        self.bird_poop_cooldown = 0.0
        self.dinosaur_stomp_cooldown = 0.0
        self.dinosaur_roar_cooldown = 0.0
        return self.malice_form

    def end_hunter_rage(self) -> None:
        if self.malice_form is None:
            return

        self.malice_form = None
        self.malice_form_timer = 0.0
        self.malice_hunter_cooldown = MALICE_HUNTER_RAGE_COOLDOWN
        self.sprite_alpha = 255
        self.tiger_invisible_timer = 0.0

    def start_tiger_invisibility(self) -> bool:
        if not self.is_malice_tiger() or self.tiger_invisible_timer > 0 or self.tiger_invisible_cooldown > 0:
            return False

        self.tiger_invisible_timer = MALICE_TIGER_INVISIBLE_DURATION
        self.sprite_alpha = 78
        return True

    def start_show_power(self) -> bool:
        if not self.is_show_runner() or self.show_power_timer > 0 or self.show_power_cooldown > 0:
            return False

        self.show_power_timer = SHOW_RUNNER_SPEED_DURATION
        return True

    def is_show_power_active(self) -> bool:
        return self.is_show_runner() and self.show_power_timer > 0

    def can_use_ducky_swing(self) -> bool:
        return self.is_ducky() and self.ducky_swing_cooldown <= 0

    def start_ducky_swing_cooldown(self) -> None:
        self.ducky_swing_cooldown = DUCKY_CRYING_SWING_COOLDOWN

    def start_ducky_hg(self) -> bool:
        if not self.is_ducky() or self.ducky_hg_timer > 0 or self.ducky_hg_cooldown > 0:
            return False

        self.ducky_hg_timer = DUCKY_HG_DURATION
        return True

    def is_ducky_hg_active(self) -> bool:
        return self.is_ducky() and self.ducky_hg_timer > 0

    def start_vengance_dash(self) -> bool:
        if not self.is_vengance_bot() or self.vengance_dash_timer > 0 or self.vengance_dash_cooldown > 0:
            return False

        self.vengance_dash_direction = safe_normalize(self.facing)
        if self.vengance_dash_direction.length_squared() == 0:
            self.vengance_dash_direction = pygame.Vector2(0, 1)
        self.vengance_dash_timer = VENGANCE_DASH_DURATION
        return True

    def stop_vengance_dash(self) -> None:
        if self.vengance_dash_timer <= 0:
            return

        self.vengance_dash_timer = 0.0
        self.vengance_dash_cooldown = VENGANCE_DASH_COOLDOWN

    def is_vengance_dash_active(self) -> bool:
        return self.is_vengance_bot() and self.vengance_dash_timer > 0

    def can_place_vengance_mine(self) -> bool:
        return self.is_vengance_bot() and self.vengance_mine_cooldown <= 0

    def start_vengance_mine_cooldown(self) -> None:
        self.vengance_mine_cooldown = VENGANCE_MINE_COOLDOWN

    def start_attack(self) -> bool:
        if not self.can_attack():
            return False

        self.attack_phase = "windup"
        self.attack_timer = self.data["windup"]
        return True

    def update_attack(self, dt: float, walls: list[Wall], arena: pygame.Rect) -> None:
        if self.cooldown_remaining > 0:
            self.cooldown_remaining = max(0.0, self.cooldown_remaining - dt)

        if self.attack_phase == "windup":
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attack_phase = "active"
                self.attack_timer = self.data["active"]

        elif self.attack_phase == "active":
            if self.data["attack_style"] == "lunge":
                self.move(self.facing, dt, walls, arena, self.data["lunge_speed"])

            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attack_phase = None
                self.cooldown_remaining = self.data["cooldown"]

    def current_hitbox(self) -> AttackHitbox | None:
        if self.attack_phase != "active":
            return None

        direction = facing_axis(self.facing)
        front = pygame.Vector2(self.rect.center) + direction * 43

        if self.data["attack_style"] == "lunge":
            if direction.x != 0:
                size = (64, 38)
            else:
                size = (38, 64)
            color = self.data["attack_color"]
        else:
            if direction.x != 0:
                size = (56, 86)
            else:
                size = (88, 56)
            color = self.data["attack_color"]

        rect = pygame.Rect(0, 0, *size)
        rect.center = (round(front.x), round(front.y))
        return AttackHitbox(rect, color, 115, self.data["attack_name"])

    def cooldown_status(self) -> str:
        if self.attack_phase == "windup":
            return "Winding up"
        if self.attack_phase == "active":
            return "Attack active"
        if self.cooldown_remaining > 0:
            return f"Cooling down {self.cooldown_remaining:.1f}s"
        return "Attack ready"

from __future__ import annotations

import json
import math
import random
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pygame


WIDTH = 1000
HEIGHT = 700
FPS = 60
ROUND_DURATION = 60.0
SURVIVOR_TOTAL_LIVES = 2

ROOT_DIR = Path(__file__).resolve().parent
ASSET_DIR = ROOT_DIR / "assets"
SPRITE_DIR = ASSET_DIR / "sprites"
SAVE_FILE = ROOT_DIR / "save_data.json"

ARENA_RECT = pygame.Rect(30, 100, 940, 570)
CHARACTER_COLLISION_SIZE = 44
SPRITE_DRAW_SIZE = 64

SURVIVOR_SPEED = 260
AI_KILLER_SPEED_MULTIPLIER = 0.90
MALICE_WALL_PHASE_DURATION = 4.0
MALICE_WALL_PHASE_COOLDOWN = 20.0
MALICE_ROAR_STUN_DURATION = 2.1
SUBSLASHER_FREEZE_DURATION = 3.0
SUBSLASHER_SPIKE_SPEED = 540
SUBSLASHER_SPIKE_LIFETIME = 1.6
SUBSLASHER_SUBZERO_SPEED = 300
SUBSLASHER_SUBZERO_LIFETIME = 5.0
SHOW_RUNNER_SLOW_DURATION = 5.2
SHOW_RUNNER_SLOW_MULTIPLIER = 0.50
SHOW_RUNNER_HOOK_PULL_RATIO = 0.50
SHOW_RUNNER_SPEED_DURATION = 12.5
SHOW_RUNNER_SPEED_MULTIPLIER = 1.69
DUCKY_CRYING_SWING_SPEED = 610
DUCKY_CRYING_SWING_LIFETIME = 0.65
DUCKY_CRYING_SWING_COOLDOWN = 1.6
DUCKY_HG_DURATION = 8.0
DUCKY_HG_COOLDOWN = 18.0
DUCKY_HG_KILLER_SPEED_MULTIPLIER = 1.40
DUCKY_HG_SURVIVOR_SPEED_MULTIPLIER = 0.70
VENGANCE_DASH_DURATION = 5.0
VENGANCE_DASH_SPEED = 440
VENGANCE_DASH_COOLDOWN = 8.0
VENGANCE_MINE_COOLDOWN = 5.0
VENGANCE_MINE_AVOID_RADIUS = 160
VENGANCE_MINE_AVOID_WEIGHT = 2.8
VENGANCE_TELEPORT_MIN_DISTANCE = 190
FRIED_CHICKEN_UNLOCK_WINS = 5
OCEAN_RUNNER_UNLOCK_WINS = 3
WICK_WONALDS_SURVIVES = 2
DUCKY_INVERTED_LOSSES = 2
DUCKY_OGEL_LOSSES = 4
SHOW_RUNNER_MASTERY_1_KILLS = 20
SHOW_RUNNER_MASTERY_2_KILLS = 40
SHOW_RUNNER_MASTERY_3_KILLS = 61
VENGANCE_BOT_MASTERY_1_WINS = 20
VENGANCE_BOT_MASTERY_2_WINS = 50
VENGANCE_BOT_MASTERY_3_WINS = 79
PACK_RUNNER_LAPS = 3
PERIMETER_MARGIN = 58

SKINS = {
    "fried_chicken": {
        "killer_id": "revenge_bot",
        "name": "Fried Chicken",
        "sprite_key": "ducky_fried_chicken",
        "challenge": "Win 5 rounds.",
    },
    "ducky_inverted": {
        "killer_id": "revenge_bot",
        "name": "Inverted",
        "sprite_key": "ducky_inverted",
        "challenge": "Lose 2 rounds as Ducky.",
    },
    "ducky_ogel": {
        "killer_id": "revenge_bot",
        "name": "Ogel",
        "sprite_key": "ducky_ogel",
        "challenge": "Lose 4 rounds as Ducky.",
    },
    "tennis_dude": {
        "killer_id": "subslasher",
        "name": "Tennis Dude",
        "sprite_key": "subslasher_tennis_dude",
        "challenge": "Hit the survivor with Perpelling Shootdown.",
    },
    "pickle_ball_bro": {
        "killer_id": "subslasher",
        "name": "Pickle Ball Bro",
        "sprite_key": "subslasher_pickle_ball_bro",
        "challenge": "Win a round using the Tennis Dude skin.",
    },
    "pack_runner": {
        "killer_id": "show_runner",
        "name": "Pack Runner",
        "sprite_key": "show_runner_pack_runner",
        "challenge": "Run around the arena perimeter 3 times in a row.",
    },
    "maldin_inverted": {
        "killer_id": "show_runner",
        "name": "Maldin Inverted",
        "sprite_key": "show_runner_maldin_inverted",
        "challenge": "Win a round using the Pack Runner skin.",
    },
    "ocean_runner": {
        "killer_id": "show_runner",
        "name": "Ocean Runner",
        "sprite_key": "show_runner_ocean_runner",
        "challenge": "Win 3 rounds as Show Runner.",
    },
    "show_runner_mastery_1": {
        "killer_id": "show_runner",
        "name": "Mastery 1",
        "sprite_key": "show_runner_mastery_1",
        "challenge": "Kill 20 survivors as Show Runner.",
        "type": "mastery",
    },
    "show_runner_mastery_2": {
        "killer_id": "show_runner",
        "name": "Mastery 2",
        "sprite_key": "show_runner_mastery_2",
        "challenge": "Kill 40 survivors as Show Runner.",
        "type": "mastery",
    },
    "show_runner_mastery_3": {
        "killer_id": "show_runner",
        "name": "Mastery 3",
        "sprite_key": "show_runner_mastery_3",
        "challenge": "Kill 61 survivors as Show Runner.",
        "type": "mastery",
    },
    "wick_wonalds": {
        "killer_id": "vengance_bot",
        "name": "Wick Wonalds",
        "sprite_key": "vengance_wick_wonalds",
        "challenge": "Survive Vengance Bot 2 times.",
    },
    "mlg": {
        "killer_id": "vengance_bot",
        "name": "MLG",
        "sprite_key": "vengance_mlg",
        "challenge": "Kill the survivor with a landmine after placing 2 or fewer mines that round.",
    },
    "vengance_bot_mastery_1": {
        "killer_id": "vengance_bot",
        "name": "Mastery 1",
        "sprite_key": "vengance_bot_mastery_1",
        "challenge": "Win 20 rounds as Vengance Bot.",
        "type": "mastery",
    },
    "vengance_bot_mastery_2": {
        "killer_id": "vengance_bot",
        "name": "Mastery 2",
        "sprite_key": "vengance_bot_mastery_2",
        "challenge": "Win 50 rounds as Vengance Bot.",
        "type": "mastery",
    },
    "vengance_bot_mastery_3": {
        "killer_id": "vengance_bot",
        "name": "Mastery 3",
        "sprite_key": "vengance_bot_mastery_3",
        "challenge": "Win 79 rounds as Vengance Bot.",
        "type": "mastery",
    },
}

KILLERS = {
    "revenge_bot": {
        "name": "Ducky",
        "alias": "Lab Duck",
        "sprite": "revenge_bot.png",
        "speed": 230,
        "lunge_speed": 520,
        "cooldown": 1.5,
        "windup": 0.15,
        "active": 0.20,
        "attack_name": "Lunge Swing",
        "attack_style": "lunge",
        "attack_range": 150,
        "attack_color": (255, 82, 70),
        "color": (238, 205, 44),
        "accent": (236, 74, 55),
        "description": "Lab duck with a fast lunge.",
    },
    "subslasher": {
        "name": "Subslasher",
        "alias": "Popsicle Sword",
        "sprite": "subslasher.png",
        "speed": 210,
        "lunge_speed": 0,
        "cooldown": 1.2,
        "windup": 0.10,
        "active": 0.25,
        "attack_name": "Popsicle Sword Swing",
        "attack_style": "wide",
        "attack_range": 118,
        "attack_color": (245, 130, 185),
        "color": (113, 86, 201),
        "accent": (248, 121, 164),
        "description": "Wide popsicle sword swing.",
    },
    "show_runner": {
        "name": "Show Runner",
        "alias": "Crowned Split-Face",
        "sprite": "show_runner.png",
        "speed": 225,
        "lunge_speed": 0,
        "cooldown": 1.25,
        "windup": 0.12,
        "active": 0.23,
        "attack_name": "Curtain Slash",
        "attack_style": "wide",
        "attack_range": 124,
        "attack_color": (230, 230, 230),
        "color": (220, 220, 210),
        "accent": (35, 35, 38),
        "description": "Crowned black-and-white slasher.",
    },
    "malice": {
        "name": "Malice",
        "alias": "Clawed Shark",
        "sprite": "malice.png",
        "speed": 235,
        "lunge_speed": 0,
        "cooldown": 1.35,
        "windup": 0.12,
        "active": 0.24,
        "attack_name": "Malice Bite",
        "attack_style": "wide",
        "attack_range": 132,
        "attack_color": (87, 191, 232),
        "color": (77, 153, 196),
        "accent": (210, 54, 45),
        "description": "Blue claws and a shark bite.",
    },
    "vengance_bot": {
        "name": "Vengance Bot",
        "alias": "Box-Head Bot",
        "sprite": "vengance_bot.png",
        "speed": 220,
        "lunge_speed": 500,
        "cooldown": 1.45,
        "windup": 0.16,
        "active": 0.20,
        "attack_name": "Vengance Lunge",
        "attack_style": "lunge",
        "attack_range": 145,
        "attack_color": (236, 63, 54),
        "color": (128, 128, 122),
        "accent": (34, 139, 72),
        "description": "Gray bot with red eyes.",
    },
}

KILLER_IDS = tuple(KILLERS.keys())


class GameState(Enum):
    TITLE = "TITLE"
    ROUND_SETUP = "ROUND_SETUP"
    ROLE_REVEAL = "ROLE_REVEAL"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"


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


@dataclass
class Wall:
    rect: pygame.Rect

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (67, 73, 85), self.rect, border_radius=6)
        pygame.draw.rect(surface, (126, 137, 151), self.rect, 2, border_radius=6)


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
        fill = (234, 240, 248) if active else (31, 41, 55)
        text_color = (15, 23, 42) if active else (241, 245, 249)
        outline = (248, 199, 88) if active else (90, 101, 117)

        pygame.draw.rect(surface, fill, self.rect, border_radius=8)
        pygame.draw.rect(surface, outline, self.rect, 3, border_radius=8)
        draw_text(surface, font, self.text, text_color, self.rect.center, center=True)

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
    ) -> None:
        self.origin = pygame.Vector2(origin)
        self.pos = pygame.Vector2(origin)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, 1)

        self.speed = speed
        self.lifetime = lifetime
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
        pygame.draw.line(surface, (170, 174, 184), self.origin, self.pos, 8)
        pygame.draw.line(surface, (58, 63, 73), self.origin, self.pos, 2)
        pygame.draw.circle(surface, (116, 122, 134), self.rect.center, 15)
        pygame.draw.circle(surface, (226, 232, 240), self.rect.center, 15, 3)
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


class Character:
    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        speed: float,
        color: tuple[int, int, int],
        sprite: pygame.Surface | None = None,
    ) -> None:
        self.name = name
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.color = color
        self.sprite = sprite
        self.facing = pygame.Vector2(0, 1)
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

        move_speed = speed if speed is not None else self.speed
        delta = direction * move_speed * dt
        blocked_x = self._move_axis(delta.x, 0, walls, arena)
        blocked_y = self._move_axis(0, delta.y, walls, arena)
        return blocked_x or blocked_y

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

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        draw_rect = pygame.Rect(0, 0, SPRITE_DRAW_SIZE, SPRITE_DRAW_SIZE)
        draw_rect.center = self.rect.center

        if self.sprite is not None:
            surface.blit(self.sprite, draw_rect)
        else:
            pygame.draw.ellipse(surface, self.color, draw_rect)
            pygame.draw.ellipse(surface, (15, 23, 42), draw_rect, 3)

        # Sprites stay readable when fixed; this arrow shows current facing.
        facing = safe_normalize(self.facing)
        if facing.length_squared() > 0:
            start = pygame.Vector2(self.rect.center)
            end = start + facing * 31
            pygame.draw.line(surface, (255, 255, 255), start, end, 3)
            pygame.draw.circle(surface, (255, 255, 255), end, 4)

        label = font.render(self.name, True, (226, 232, 240))
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.top - 11))
        surface.blit(label, label_rect)


class Survivor(Character):
    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        sprite: pygame.Surface | None = None,
    ) -> None:
        super().__init__(name, pos, SURVIVOR_SPEED, (61, 145, 255), sprite)


class Killer(Character):
    def __init__(
        self,
        killer_id: str,
        name: str,
        pos: tuple[int, int],
        sprite: pygame.Surface | None = None,
    ) -> None:
        self.killer_id = killer_id
        self.data = KILLERS[killer_id]
        super().__init__(name, pos, self.data["speed"], self.data["color"], sprite)
        self.attack_phase: str | None = None
        self.attack_timer = 0.0
        self.cooldown_remaining = 0.0
        self.wall_phase_timer = 0.0
        self.wall_phase_cooldown = 0.0
        self.show_power_timer = 0.0
        self.ducky_swing_cooldown = 0.0
        self.ducky_hg_timer = 0.0
        self.ducky_hg_cooldown = 0.0
        self.vengance_dash_timer = 0.0
        self.vengance_dash_cooldown = 0.0
        self.vengance_dash_direction = pygame.Vector2(0, 1)
        self.vengance_mine_cooldown = 0.0

    def can_attack(self) -> bool:
        return self.attack_phase is None and self.cooldown_remaining <= 0

    def is_ducky(self) -> bool:
        return self.killer_id == "revenge_bot"

    def is_malice(self) -> bool:
        return self.killer_id == "malice"

    def is_subslasher(self) -> bool:
        return self.killer_id == "subslasher"

    def is_show_runner(self) -> bool:
        return self.killer_id == "show_runner"

    def is_vengance_bot(self) -> bool:
        return self.killer_id == "vengance_bot"

    def is_wall_phasing(self) -> bool:
        return self.is_malice() and self.wall_phase_timer > 0

    def start_wall_phase(self) -> bool:
        if not self.is_malice() or self.wall_phase_timer > 0 or self.wall_phase_cooldown > 0:
            return False

        self.wall_phase_timer = MALICE_WALL_PHASE_DURATION
        return True

    def update_abilities(self, dt: float) -> None:
        if self.wall_phase_timer > 0:
            self.wall_phase_timer = max(0.0, self.wall_phase_timer - dt)
            if self.wall_phase_timer == 0:
                self.wall_phase_cooldown = MALICE_WALL_PHASE_COOLDOWN
        elif self.wall_phase_cooldown > 0:
            self.wall_phase_cooldown = max(0.0, self.wall_phase_cooldown - dt)

        if self.show_power_timer > 0:
            self.show_power_timer = max(0.0, self.show_power_timer - dt)

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

    def start_show_power(self) -> bool:
        if not self.is_show_runner():
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


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tag 2.0")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fullscreen = False

        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_medium = pygame.font.SysFont("arial", 26)
        self.font_large = pygame.font.SysFont("arial", 48, bold=True)
        self.font_title = pygame.font.SysFont("arial", 76, bold=True)

        self.state = GameState.TITLE
        self.running = True
        self.round_killer = "revenge_bot"
        self.selected_player_killer = "revenge_bot"
        self.save_data = self.load_save_data()
        self.total_wins = self.save_data["total_wins"]
        self.unlocked_skins: set[str] = set(self.save_data["unlocked_skins"])
        self.challenge_progress: dict[str, int] = dict(self.save_data["challenge_progress"])
        self.selected_skins = {killer_id: "classic" for killer_id in KILLER_IDS}
        self.skin_notice = ""
        self.show_runner_perimeter_next = 0
        self.show_runner_perimeter_laps = 0
        self.last_perimeter_edge: str | None = None
        self.vengance_mines_placed_this_round = 0
        self.player_role = "Survivor"
        self.round_time = ROUND_DURATION
        self.survivor_life_number = 1
        self.survivor_status_message = ""
        self.survivor_stun_timer = 0.0
        self.survivor_slow_timer = 0.0
        self.player_won = False
        self.end_reason = ""

        self.sprites = self.load_sprites()
        self.walls = self.create_walls()
        self.player: Character | None = None
        self.survivor: Survivor | None = None
        self.killers: list[Killer] = []
        self.active_hitboxes: list[AttackHitbox] = []
        self.projectiles: list[IceProjectile] = []
        self.ducky_belts: list[DuckyBelt] = []
        self.landmines: list[VenganceLandmine] = []

        self.menu_buttons = {
            "play": Button(pygame.Rect(390, 450, 220, 58), "Start"),
            "reveal": Button(pygame.Rect(390, 585, 220, 58), "Reveal Role"),
            "begin": Button(pygame.Rect(390, 622, 220, 58), "Begin Round"),
        }
        self.fullscreen_button = Button(pygame.Rect(WIDTH - 78, 10, 58, 28), "Full")

        self.audio_enabled = False
        self.music_tracks: dict[str, Path] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.setup_audio()

    def load_sprites(self) -> dict[str, pygame.Surface]:
        sprites: dict[str, pygame.Surface] = {}
        paths = {"survivor": SPRITE_DIR / "survivor.png"}
        for killer_id, data in KILLERS.items():
            paths[killer_id] = SPRITE_DIR / data["sprite"]
        for skin in SKINS.values():
            paths[skin["sprite_key"]] = SPRITE_DIR / f"{skin['sprite_key']}.png"

        for key, path in paths.items():
            if not path.exists():
                continue
            try:
                image = pygame.image.load(str(path)).convert_alpha()
                image = pygame.transform.smoothscale(
                    image,
                    (SPRITE_DRAW_SIZE, SPRITE_DRAW_SIZE),
                )
                sprites[key] = image
            except pygame.error:
                # Missing or broken images should never stop the prototype.
                continue

        return sprites

    def load_save_data(self) -> dict[str, object]:
        default_data = {
            "total_wins": 0,
            "unlocked_skins": [],
            "challenge_progress": {
                "show_runner_wins": 0,
                "show_runner_kills": 0,
                "vengance_bot_wins": 0,
                "vengance_bot_survives": 0,
                "ducky_losses": 0,
            },
        }

        if not SAVE_FILE.exists():
            return default_data

        try:
            data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default_data

        wins = data.get("total_wins", 0)
        if not isinstance(wins, int):
            wins = 0

        unlocked = data.get("unlocked_skins", [])
        if not isinstance(unlocked, list):
            unlocked = []

        progress = data.get("challenge_progress", {})
        if not isinstance(progress, dict):
            progress = {}

        clean_progress = dict(default_data["challenge_progress"])
        for key, value in progress.items():
            if isinstance(key, str) and isinstance(value, int):
                clean_progress[key] = max(0, value)

        clean_unlocked = {skin_id for skin_id in unlocked if skin_id in SKINS}
        if wins >= FRIED_CHICKEN_UNLOCK_WINS:
            clean_unlocked.add("fried_chicken")
        show_runner_kills = clean_progress.get("show_runner_kills", 0)
        if show_runner_kills >= SHOW_RUNNER_MASTERY_1_KILLS:
            clean_unlocked.add("show_runner_mastery_1")
        if show_runner_kills >= SHOW_RUNNER_MASTERY_2_KILLS:
            clean_unlocked.add("show_runner_mastery_2")
        if show_runner_kills >= SHOW_RUNNER_MASTERY_3_KILLS:
            clean_unlocked.add("show_runner_mastery_3")
        vengance_bot_wins = clean_progress.get("vengance_bot_wins", 0)
        if vengance_bot_wins >= VENGANCE_BOT_MASTERY_1_WINS:
            clean_unlocked.add("vengance_bot_mastery_1")
        if vengance_bot_wins >= VENGANCE_BOT_MASTERY_2_WINS:
            clean_unlocked.add("vengance_bot_mastery_2")
        if vengance_bot_wins >= VENGANCE_BOT_MASTERY_3_WINS:
            clean_unlocked.add("vengance_bot_mastery_3")

        return {
            "total_wins": max(0, wins),
            "unlocked_skins": sorted(clean_unlocked),
            "challenge_progress": clean_progress,
        }

    def save_progress(self) -> None:
        try:
            SAVE_FILE.write_text(
                json.dumps(
                    {
                        "total_wins": self.total_wins,
                        "unlocked_skins": sorted(self.unlocked_skins),
                        "challenge_progress": self.challenge_progress,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        except OSError:
            pass

    def fried_chicken_unlocked(self) -> bool:
        return self.skin_unlocked("fried_chicken")

    def skin_unlocked(self, skin_id: str) -> bool:
        return skin_id in self.unlocked_skins

    def unlock_skin(self, skin_id: str, reason: str) -> None:
        if skin_id not in SKINS or skin_id in self.unlocked_skins:
            return

        self.unlocked_skins.add(skin_id)
        self.skin_notice = f"{SKINS[skin_id]['name']} unlocked: {reason}"
        self.save_progress()

    def setup_audio(self) -> None:
        try:
            pygame.mixer.init()
        except pygame.error:
            return

        self.audio_enabled = True

        show_runner_music = ASSET_DIR / "show_runner_chase_music.wav"
        if show_runner_music.exists():
            self.music_tracks["show_runner"] = show_runner_music

        ducky_music = ASSET_DIR / "ducky_chase_music.wav"
        if ducky_music.exists():
            self.music_tracks["revenge_bot"] = ducky_music

        subslasher_music = ASSET_DIR / "subslasher_chase_music.wav"
        if subslasher_music.exists():
            self.music_tracks["subslasher"] = subslasher_music

        malice_music = ASSET_DIR / "malice_chase_music.wav"
        if malice_music.exists():
            self.music_tracks["malice"] = malice_music

        vengance_base_music = ASSET_DIR / "vengance_bot_base_chase_music.wav"
        if vengance_base_music.exists():
            self.music_tracks["vengance_bot"] = vengance_base_music

        vengance_music = ASSET_DIR / "vengance_bot_chase_music.wav"
        if vengance_music.exists():
            self.music_tracks["skin:mlg"] = vengance_music

        pack_runner_music = ASSET_DIR / "pack_runner_chase_music.wav"
        if pack_runner_music.exists():
            self.music_tracks["skin:pack_runner"] = pack_runner_music

        mastery_3_music = ASSET_DIR / "show_runner_mastery_3_music.wav"
        if mastery_3_music.exists():
            self.music_tracks["skin:show_runner_mastery_3"] = mastery_3_music

        vengance_mastery_3_music = ASSET_DIR / "vengance_bot_mastery_3_music.wav"
        if vengance_mastery_3_music.exists():
            self.music_tracks["skin:vengance_bot_mastery_3"] = vengance_mastery_3_music

        for sound_name in ("attack", "win", "lose", "malice_roar"):
            path = ASSET_DIR / f"{sound_name}.wav"
            if not path.exists():
                continue
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(str(path))
            except pygame.error:
                pass

    def play_sound(self, name: str) -> None:
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def start_round_music(self) -> None:
        if not self.audio_enabled:
            return

        pygame.mixer.music.stop()
        music_path = self.music_tracks.get(self.round_killer)
        if self.player_role == "Killer":
            selected_skin = self.selected_skins.get(self.round_killer, "classic")
            skin_music = self.music_tracks.get(f"skin:{selected_skin}")
            if skin_music is not None:
                music_path = skin_music

        if music_path is None:
            return

        try:
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def stop_music(self) -> None:
        if self.audio_enabled:
            pygame.mixer.music.stop()

    def create_walls(self) -> list[Wall]:
        wall_rects = [
            pygame.Rect(145, 205, 245, 30),
            pygame.Rect(610, 185, 250, 30),
            pygame.Rect(475, 295, 44, 190),
            pygame.Rect(160, 505, 205, 32),
            pygame.Rect(665, 490, 205, 32),
            pygame.Rect(315, 385, 118, 30),
            pygame.Rect(565, 370, 110, 30),
            pygame.Rect(865, 300, 34, 125),
            pygame.Rect(90, 325, 34, 135),
        ]
        return [Wall(rect) for rect in wall_rects]

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def smoke_test(self) -> None:
        self.round_killer = "revenge_bot"
        self.player_role = "Killer"
        self.begin_round()
        for _ in range(12):
            self.update(1 / FPS)
            self.draw()
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self.running = False
            return

        if self.state == GameState.TITLE:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = GameState.ROUND_SETUP

        elif self.state == GameState.ROUND_SETUP:
            selected_index = self.killer_index_from_key(key)
            if selected_index is not None:
                self.selected_player_killer = KILLER_IDS[selected_index]
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.reveal_role()

        elif self.state == GameState.ROLE_REVEAL:
            selected_skin = self.skin_index_from_key(key)
            if self.player_role == "Killer" and selected_skin is not None:
                self.select_skin_for_round(selected_skin)
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.begin_round()

        elif self.state == GameState.PLAYING:
            if self.player_role != "Killer" or not isinstance(self.player, Killer):
                return

            if key == pygame.K_SPACE:
                if self.player.start_attack():
                    self.play_sound("attack")
            elif key == pygame.K_i:
                if self.player.is_malice():
                    self.player.start_wall_phase()
                elif self.player.is_subslasher():
                    self.fire_subslasher_spike("freeze")
            elif key == pygame.K_h:
                self.use_malice_roar()
            elif key == pygame.K_e:
                if self.player.is_subslasher():
                    self.fire_subslasher_spike("kill")
            elif key == pygame.K_q:
                if self.player.is_subslasher():
                    self.use_subslasher_subzero()
            elif key == pygame.K_c:
                if self.player.is_ducky():
                    self.use_ducky_crying_swing()
                elif self.player.is_vengance_bot():
                    self.use_vengance_explosion()
            elif key == pygame.K_y:
                if self.player.is_ducky():
                    self.player.start_ducky_hg()
            elif key == pygame.K_r:
                if self.player.is_vengance_bot():
                    self.player.start_vengance_dash()
            elif key == pygame.K_9:
                if self.player.is_show_runner():
                    self.use_show_runner_laugh()
            elif key == pygame.K_u:
                if self.player.is_show_runner():
                    self.use_show_runner_hook()
            elif key == pygame.K_a:
                if self.player.is_show_runner():
                    self.player.start_show_power()

        elif self.state == GameState.GAME_OVER:
            if key == pygame.K_r:
                self.reset_to_title()

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.fullscreen_button.contains(pos):
            self.toggle_fullscreen()
            return

        if self.state == GameState.TITLE:
            if self.menu_buttons["play"].contains(pos):
                self.state = GameState.ROUND_SETUP

        elif self.state == GameState.ROUND_SETUP:
            clicked_killer = self.killer_from_card_click(pos)
            if clicked_killer is not None:
                self.selected_player_killer = clicked_killer
                return

            if self.menu_buttons["reveal"].contains(pos):
                self.reveal_role()

        elif self.state == GameState.ROLE_REVEAL:
            clicked_skin = self.skin_from_card_click(pos)
            if self.player_role == "Killer" and clicked_skin is not None:
                self.select_skin_for_round(clicked_skin)
                return

            if self.menu_buttons["begin"].contains(pos):
                self.begin_round()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

    def reveal_role(self) -> None:
        self.player_role = random.choice(["Survivor", "Killer"])
        if self.player_role == "Killer":
            self.round_killer = self.selected_player_killer
        else:
            self.round_killer = random.choice(KILLER_IDS)
        self.survivor_life_number = 1
        self.survivor_status_message = ""
        self.survivor_stun_timer = 0.0
        self.survivor_slow_timer = 0.0
        self.state = GameState.ROLE_REVEAL

    def skin_options_for_killer(self, killer_id: str) -> list[str]:
        skins = ["classic"]
        skins.extend(
            skin_id
            for skin_id, data in SKINS.items()
            if data["killer_id"] == killer_id
        )
        return skins

    def skin_name(self, killer_id: str, skin_id: str) -> str:
        if skin_id == "classic":
            return f"Classic {KILLERS[killer_id]['name']}"
        return SKINS[skin_id]["name"]

    def skin_sprite_key(self, killer_id: str, skin_id: str) -> str:
        if skin_id == "classic":
            return killer_id
        return SKINS[skin_id]["sprite_key"]

    def skin_index_from_key(self, key: int) -> str | None:
        number_keys = (
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
        )
        if key not in number_keys:
            return None

        options = self.skin_options_for_killer(self.round_killer)
        index = number_keys.index(key)
        if index >= len(options):
            return None
        return options[index]

    def select_skin_for_round(self, skin_id: str) -> None:
        if skin_id != "classic" and not self.skin_unlocked(skin_id):
            self.skin_notice = (
                f"{SKINS[skin_id]['name']} is locked. Challenge: "
                f"{self.skin_challenge_detail(skin_id)}"
            )
            return

        if skin_id != "classic" and SKINS[skin_id]["killer_id"] != self.round_killer:
            return

        self.selected_skins[self.round_killer] = skin_id
        self.skin_notice = f"{self.skin_name(self.round_killer, skin_id)} selected."

    def skin_card_rect(self, index: int) -> pygame.Rect:
        card_width = 210
        card_height = 70
        card_gap = 18
        row_gap = 8
        options = self.skin_options_for_killer(self.round_killer)
        columns = min(4, len(options))
        row = index // columns
        column = index % columns
        total_width = columns * card_width + (columns - 1) * card_gap
        start_x = (WIDTH - total_width) // 2
        return pygame.Rect(
            start_x + column * (card_width + card_gap),
            430 + row * (card_height + row_gap),
            card_width,
            card_height,
        )

    def skin_from_card_click(self, pos: tuple[int, int]) -> str | None:
        for index, skin_id in enumerate(self.skin_options_for_killer(self.round_killer)):
            if self.skin_card_rect(index).collidepoint(pos):
                return skin_id
        return None

    def killer_index_from_key(self, key: int) -> int | None:
        number_keys = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5)
        if key not in number_keys:
            return None

        index = number_keys.index(key)
        if index >= len(KILLER_IDS):
            return None
        return index

    def killer_card_rect(self, index: int) -> pygame.Rect:
        card_width = 172
        card_gap = 16
        start_x = 36
        return pygame.Rect(start_x + index * (card_width + card_gap), 170, card_width, 305)

    def killer_from_card_click(self, pos: tuple[int, int]) -> str | None:
        for index, killer_id in enumerate(KILLER_IDS):
            if self.killer_card_rect(index).collidepoint(pos):
                return killer_id
        return None

    def begin_round(self) -> None:
        self.round_time = ROUND_DURATION
        self.player_won = False
        self.end_reason = ""
        self.active_hitboxes = []
        self.projectiles = []
        self.ducky_belts = []
        self.landmines = []
        self.survivor_slow_timer = 0.0
        self.show_runner_perimeter_next = 0
        self.show_runner_perimeter_laps = 0
        self.last_perimeter_edge = None
        self.vengance_mines_placed_this_round = 0
        self.walls = self.create_walls()

        survivor_sprite = self.sprites.get("survivor")
        killer_sprite = self.sprite_for_round_killer()

        if self.player_role == "Survivor":
            self.survivor = Survivor("You", (500, 560), survivor_sprite)
            self.player = self.survivor
            self.killers = [
                Killer(
                    self.round_killer,
                    KILLERS[self.round_killer]["name"],
                    (820, 145),
                    killer_sprite,
                )
            ]
        else:
            self.player = Killer(
                self.round_killer,
                "You",
                (500, 555),
                killer_sprite,
            )
            self.survivor = Survivor("AI Survivor", (500, 150), survivor_sprite)
            self.killers = [self.player]

        self.state = GameState.PLAYING
        self.start_round_music()

    def sprite_for_round_killer(self) -> pygame.Surface | None:
        if self.player_role == "Killer":
            selected_skin = self.selected_skins.get(self.round_killer, "classic")
            if selected_skin != "classic" and self.skin_unlocked(selected_skin):
                skin_key = self.skin_sprite_key(self.round_killer, selected_skin)
                return self.sprites.get(skin_key) or self.sprites.get(self.round_killer)

        return self.sprites.get(self.round_killer)

    def reset_to_title(self) -> None:
        self.state = GameState.TITLE
        self.player = None
        self.survivor = None
        self.killers = []
        self.active_hitboxes = []
        self.projectiles = []
        self.ducky_belts = []
        self.landmines = []
        self.round_time = ROUND_DURATION
        self.survivor_life_number = 1
        self.survivor_status_message = ""
        self.survivor_stun_timer = 0.0
        self.survivor_slow_timer = 0.0
        self.stop_music()

    def update(self, dt: float) -> None:
        if self.state != GameState.PLAYING:
            return

        self.round_time = max(0.0, self.round_time - dt)

        keys = pygame.key.get_pressed()
        player_direction = vector_from_keys(keys)

        if isinstance(self.player, Killer):
            self.player.update_abilities(dt)

        if self.survivor_stun_timer > 0:
            self.survivor_stun_timer = max(0.0, self.survivor_stun_timer - dt)
        if self.survivor_slow_timer > 0:
            self.survivor_slow_timer = max(0.0, self.survivor_slow_timer - dt)

        if self.player is not None:
            player_walls = self.walls
            if isinstance(self.player, Killer) and self.player.is_wall_phasing():
                player_walls = []

            player_speed = None
            if isinstance(self.player, Killer) and self.player.is_show_power_active():
                player_speed = self.player.speed * SHOW_RUNNER_SPEED_MULTIPLIER
            elif isinstance(self.player, Killer) and self.player.is_ducky_hg_active():
                player_speed = self.player.speed * DUCKY_HG_KILLER_SPEED_MULTIPLIER
            elif isinstance(self.player, Killer) and self.player.is_vengance_dash_active():
                player_direction = self.player.vengance_dash_direction
                player_speed = VENGANCE_DASH_SPEED

            blocked = self.player.move(player_direction, dt, player_walls, ARENA_RECT, player_speed)
            if (
                blocked
                and isinstance(self.player, Killer)
                and self.player.is_vengance_dash_active()
            ):
                self.player.stop_vengance_dash()

            if isinstance(self.player, Killer) and not self.player.is_wall_phasing():
                self.resolve_wall_overlap(self.player)

            self.update_movement_challenges()

        if self.player_role == "Survivor":
            self.update_survivor_mode(dt)
        else:
            self.update_killer_mode(dt)

    def update_movement_challenges(self) -> None:
        if not isinstance(self.player, Killer):
            return
        if self.player_role != "Killer" or self.round_killer != "show_runner":
            return
        if self.skin_unlocked("pack_runner"):
            return

        edge = self.current_perimeter_edge(self.player.rect)
        if edge is None:
            self.last_perimeter_edge = None
            return
        if edge == self.last_perimeter_edge:
            return
        self.last_perimeter_edge = edge

        sequence = ("top", "right", "bottom", "left")
        expected = sequence[self.show_runner_perimeter_next]
        if edge != expected:
            if edge == "top":
                self.show_runner_perimeter_next = 1
                self.show_runner_perimeter_laps = 0
            return

        self.show_runner_perimeter_next = (self.show_runner_perimeter_next + 1) % len(sequence)
        if self.show_runner_perimeter_next == 0:
            self.show_runner_perimeter_laps += 1
            self.skin_notice = f"Pack Runner perimeter laps: {self.show_runner_perimeter_laps}/{PACK_RUNNER_LAPS}"
            if self.show_runner_perimeter_laps >= PACK_RUNNER_LAPS:
                self.unlock_skin("pack_runner", "3 perimeter laps completed")

    def current_perimeter_edge(self, rect: pygame.Rect) -> str | None:
        if rect.top <= ARENA_RECT.top + PERIMETER_MARGIN:
            return "top"
        if rect.right >= ARENA_RECT.right - PERIMETER_MARGIN:
            return "right"
        if rect.bottom >= ARENA_RECT.bottom - PERIMETER_MARGIN:
            return "bottom"
        if rect.left <= ARENA_RECT.left + PERIMETER_MARGIN:
            return "left"
        return None

    def use_malice_roar(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_malice():
            return
        if self.player_role != "Killer" or self.survivor is None:
            return

        self.survivor_stun_timer = MALICE_ROAR_STUN_DURATION
        self.play_sound("malice_roar")

    def fire_subslasher_spike(self, effect: str) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_subslasher():
            return
        if self.player_role != "Killer":
            return

        direction = safe_normalize(self.player.facing)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, 1)

        start_pos = self.player.pos + direction * 38
        self.projectiles.append(
            IceProjectile(
                start_pos,
                direction,
                SUBSLASHER_SPIKE_SPEED,
                SUBSLASHER_SPIKE_LIFETIME,
                effect,
            )
        )

    def use_subslasher_subzero(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_subslasher():
            return
        if self.player_role != "Killer":
            return

        direction = safe_normalize(self.player.facing)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, 1)

        perpendicular = pygame.Vector2(-direction.y, direction.x)
        for offset in (-22, 0, 22):
            start_pos = self.player.pos + direction * 34 + perpendicular * offset
            self.projectiles.append(
                IceProjectile(
                    start_pos,
                    direction,
                    SUBSLASHER_SUBZERO_SPEED,
                    SUBSLASHER_SUBZERO_LIFETIME,
                    "kill",
                    homing=True,
                )
            )

    def use_ducky_crying_swing(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.can_use_ducky_swing():
            return
        if self.player_role != "Killer":
            return

        direction = safe_normalize(self.player.facing)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, 1)

        start_pos = self.player.pos + direction * 38
        self.ducky_belts.append(
            DuckyBelt(
                start_pos,
                direction,
                DUCKY_CRYING_SWING_SPEED,
                DUCKY_CRYING_SWING_LIFETIME,
            )
        )
        self.player.start_ducky_swing_cooldown()
        self.play_sound("attack")

    def use_vengance_explosion(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.can_place_vengance_mine():
            return
        if self.player_role != "Killer" or self.survivor is None:
            return

        mine = VenganceLandmine(self.player.pos)
        self.landmines.append(mine)
        self.vengance_mines_placed_this_round += 1
        self.player.start_vengance_mine_cooldown()
        self.teleport_player_out_of_the_way()
        self.play_sound("attack")

    def use_show_runner_laugh(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_show_runner():
            return
        if self.player_role != "Killer" or self.survivor is None:
            return

        self.survivor_slow_timer = SHOW_RUNNER_SLOW_DURATION

    def use_show_runner_hook(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_show_runner():
            return
        if self.player_role != "Killer" or self.survivor is None:
            return

        self.survivor.pos = self.survivor.pos.lerp(
            self.player.pos,
            SHOW_RUNNER_HOOK_PULL_RATIO,
        )
        self.survivor.update_rect()
        self.resolve_wall_overlap(self.survivor)

    def resolve_wall_overlap(self, character: Character) -> None:
        for wall in self.walls:
            if not character.rect.colliderect(wall.rect):
                continue

            overlap = character.rect.clip(wall.rect)
            if overlap.width < overlap.height:
                if character.rect.centerx < wall.rect.centerx:
                    character.rect.right = wall.rect.left
                else:
                    character.rect.left = wall.rect.right
            else:
                if character.rect.centery < wall.rect.centery:
                    character.rect.bottom = wall.rect.top
                else:
                    character.rect.top = wall.rect.bottom

            character.pos.update(character.rect.center)

    def update_projectiles(self, dt: float) -> None:
        if self.survivor is None:
            self.projectiles = []
            return

        remaining: list[IceProjectile] = []
        for projectile in self.projectiles:
            if not projectile.update(dt, self.survivor, self.walls):
                continue

            if projectile.rect.colliderect(self.survivor.rect):
                if projectile.effect == "freeze":
                    self.survivor_stun_timer = max(
                        self.survivor_stun_timer,
                        SUBSLASHER_FREEZE_DURATION,
                    )
                    if self.round_killer == "subslasher" and self.player_role == "Killer":
                        self.unlock_skin("tennis_dude", "freeze shot hit the survivor")
                else:
                    self.end_round(True, "Subslasher's ice caught the survivor.")
                    return
            else:
                remaining.append(projectile)

        self.projectiles = remaining

    def update_ducky_belts(self, dt: float) -> None:
        if self.survivor is None:
            self.ducky_belts = []
            return

        remaining: list[DuckyBelt] = []
        for belt in self.ducky_belts:
            if not belt.update(dt, self.walls):
                continue

            if belt.rect.colliderect(self.survivor.rect):
                self.end_round(True, "Ducky's crying swing hit the survivor.")
                return

            remaining.append(belt)

        self.ducky_belts = remaining

    def update_landmines(self) -> None:
        if self.survivor is None:
            self.landmines = []
            return

        remaining: list[VenganceLandmine] = []
        for mine in self.landmines:
            if mine.rect.colliderect(self.survivor.rect):
                if (
                    self.round_killer == "vengance_bot"
                    and self.player_role == "Killer"
                    and self.vengance_mines_placed_this_round <= 2
                ):
                    self.unlock_skin("mlg", "landmine kill with 2 or fewer mines")
                self.end_round(True, "Vengance Bot's landmine exploded.")
                return

            remaining.append(mine)

        self.landmines = remaining

    def teleport_player_out_of_the_way(self) -> None:
        if not isinstance(self.player, Killer):
            return

        avoid_pos = self.survivor.pos if self.survivor is not None else None
        new_pos = self.random_open_position(avoid_pos, VENGANCE_TELEPORT_MIN_DISTANCE)
        if new_pos is None:
            return

        self.player.pos = new_pos
        self.player.update_rect()

    def random_open_position(
        self,
        avoid_pos: pygame.Vector2 | None,
        min_distance: float,
    ) -> pygame.Vector2 | None:
        half = CHARACTER_COLLISION_SIZE // 2

        for _ in range(100):
            x = random.randint(ARENA_RECT.left + half, ARENA_RECT.right - half)
            y = random.randint(ARENA_RECT.top + half, ARENA_RECT.bottom - half)
            rect = pygame.Rect(0, 0, CHARACTER_COLLISION_SIZE, CHARACTER_COLLISION_SIZE)
            rect.center = (x, y)

            if not ARENA_RECT.contains(rect):
                continue
            if any(rect.colliderect(wall.rect) for wall in self.walls):
                continue
            if avoid_pos is not None and pygame.Vector2(x, y).distance_to(avoid_pos) < min_distance:
                continue

            return pygame.Vector2(x, y)

        return None

    def update_survivor_mode(self, dt: float) -> None:
        if self.survivor is None:
            return

        self.active_hitboxes = []
        for killer in self.killers:
            self.update_ai_killer(killer, self.survivor, dt)
            hitbox = killer.current_hitbox()
            if hitbox is not None:
                self.active_hitboxes.append(hitbox)
                if hitbox.rect.colliderect(self.survivor.rect):
                    self.handle_survivor_hit(killer.data["name"])
                    return

        if self.round_time <= 0:
            self.handle_survivor_timer_success()

    def handle_survivor_hit(self, killer_name: str) -> None:
        if self.survivor_life_number >= SURVIVOR_TOTAL_LIVES:
            self.end_round(False, f"{killer_name} caught you on your final life.")
            return

        self.survivor_life_number += 1
        self.survivor_status_message = "Hit! Final life."
        self.round_killer = random.choice(KILLER_IDS)
        self.begin_round()

    def handle_survivor_timer_success(self) -> None:
        if self.survivor_life_number >= SURVIVOR_TOTAL_LIVES:
            self.end_round(True, "You survived both survivor lives.")
            return

        if self.round_killer == "vengance_bot":
            self.record_vengance_bot_survive()

        self.survivor_life_number += 1
        self.survivor_status_message = "Final life - keep running!"
        self.round_killer = random.choice(KILLER_IDS)
        self.begin_round()

    def update_killer_mode(self, dt: float) -> None:
        if not isinstance(self.player, Killer) or self.survivor is None:
            return

        self.update_projectiles(dt)
        if self.state != GameState.PLAYING:
            return
        self.update_ducky_belts(dt)
        if self.state != GameState.PLAYING:
            return
        self.update_landmines()
        if self.state != GameState.PLAYING:
            return

        if self.player.is_vengance_dash_active() and self.player.rect.colliderect(self.survivor.rect):
            self.end_round(True, "Vengance Bot's robot slash hit the survivor.")
            return

        self.update_ai_survivor(self.survivor, self.killers, dt)
        self.player.update_attack(dt, self.walls, ARENA_RECT)

        self.active_hitboxes = []
        hitbox = self.player.current_hitbox()
        if hitbox is not None:
            self.active_hitboxes.append(hitbox)
            if hitbox.rect.colliderect(self.survivor.rect):
                self.end_round(True, "Your attack caught the survivor.")
                return

        if self.round_time <= 0:
            self.end_round(False, "The survivor escaped until the timer ended.")

    def update_ai_killer(self, killer: Killer, target: Survivor, dt: float) -> None:
        distance = killer.pos.distance_to(target.pos)

        if killer.attack_phase is None:
            if distance <= killer.data["attack_range"] and killer.can_attack():
                if killer.start_attack():
                    self.play_sound("attack")
            else:
                desired = safe_normalize(target.pos - killer.pos)
                desired += self.wall_avoidance(killer) * 0.95
                desired = killer.apply_ai_nudge(desired, dt)
                ai_speed = killer.speed * AI_KILLER_SPEED_MULTIPLIER
                blocked = killer.move(desired, dt, self.walls, ARENA_RECT, ai_speed)
                if blocked:
                    killer.choose_ai_nudge()

        killer.update_attack(dt, self.walls, ARENA_RECT)

    def update_ai_survivor(
        self,
        survivor: Survivor,
        threats: list[Killer],
        dt: float,
    ) -> None:
        if self.survivor_stun_timer > 0:
            return
        if not threats:
            return

        nearest = min(threats, key=lambda killer: killer.pos.distance_to(survivor.pos))
        flee = safe_normalize(survivor.pos - nearest.pos)

        # If the survivor has room, drift toward open space instead of a wall.
        center_pull = safe_normalize(pygame.Vector2(ARENA_RECT.center) - survivor.pos) * 0.25
        desired = (
            flee
            + center_pull
            + self.wall_avoidance(survivor) * 1.2
            + self.landmine_avoidance(survivor) * VENGANCE_MINE_AVOID_WEIGHT
        )

        survivor_speed = survivor.speed
        if self.survivor_slow_timer > 0:
            survivor_speed *= SHOW_RUNNER_SLOW_MULTIPLIER
        if isinstance(self.player, Killer) and self.player.is_ducky_hg_active():
            survivor_speed *= DUCKY_HG_SURVIVOR_SPEED_MULTIPLIER

        # If the next step would walk into a mine, prioritize the mine-escape vector.
        if self.landmines and self.projected_landmine_collision(survivor, desired, dt, survivor_speed):
            desired = (
                self.landmine_avoidance(survivor) * (VENGANCE_MINE_AVOID_WEIGHT + 1.5)
                + self.wall_avoidance(survivor)
                + center_pull
            )

        desired = survivor.apply_ai_nudge(desired, dt)

        blocked = survivor.move(desired, dt, self.walls, ARENA_RECT, survivor_speed)
        if blocked:
            survivor.choose_ai_nudge()

    def landmine_avoidance(self, character: Character) -> pygame.Vector2:
        avoid = pygame.Vector2()

        for mine in self.landmines:
            delta = character.pos - mine.pos
            distance = delta.length()
            if distance <= 0:
                delta = character.facing if character.facing.length_squared() > 0 else pygame.Vector2(1, 0)
                distance = 1
            if distance < VENGANCE_MINE_AVOID_RADIUS:
                danger = (VENGANCE_MINE_AVOID_RADIUS - distance) / VENGANCE_MINE_AVOID_RADIUS
                avoid += delta.normalize() * danger

        return avoid

    def projected_landmine_collision(
        self,
        character: Character,
        direction: pygame.Vector2,
        dt: float,
        speed: float,
    ) -> bool:
        if direction.length_squared() == 0:
            return False

        projected = character.rect.copy()
        step = direction.normalize() * speed * dt
        projected.center = (
            round(character.pos.x + step.x),
            round(character.pos.y + step.y),
        )
        return any(projected.colliderect(mine.rect.inflate(18, 18)) for mine in self.landmines)

    def wall_avoidance(self, character: Character) -> pygame.Vector2:
        avoid = pygame.Vector2()

        for wall in self.walls:
            nearest_x = max(wall.rect.left, min(character.pos.x, wall.rect.right))
            nearest_y = max(wall.rect.top, min(character.pos.y, wall.rect.bottom))
            delta = character.pos - pygame.Vector2(nearest_x, nearest_y)
            distance = delta.length()
            if 0 < distance < 86:
                avoid += delta.normalize() * ((86 - distance) / 86)

        margin = 76
        if character.rect.left - ARENA_RECT.left < margin:
            avoid.x += (margin - (character.rect.left - ARENA_RECT.left)) / margin
        if ARENA_RECT.right - character.rect.right < margin:
            avoid.x -= (margin - (ARENA_RECT.right - character.rect.right)) / margin
        if character.rect.top - ARENA_RECT.top < margin:
            avoid.y += (margin - (character.rect.top - ARENA_RECT.top)) / margin
        if ARENA_RECT.bottom - character.rect.bottom < margin:
            avoid.y -= (margin - (ARENA_RECT.bottom - character.rect.bottom)) / margin

        return avoid

    def end_round(self, player_won: bool, reason: str) -> None:
        self.player_won = player_won
        self.end_reason = reason
        if player_won:
            self.record_win()
        else:
            self.record_loss()
        self.state = GameState.GAME_OVER
        self.stop_music()
        self.play_sound("win" if player_won else "lose")

    def record_win(self) -> None:
        was_locked = not self.fried_chicken_unlocked()
        self.total_wins += 1
        if was_locked and self.total_wins >= FRIED_CHICKEN_UNLOCK_WINS:
            self.unlock_skin("fried_chicken", "5 wins completed")

        if self.player_role == "Killer" and self.round_killer == "show_runner":
            if self.selected_skins.get("show_runner") == "pack_runner":
                self.unlock_skin("maldin_inverted", "won with Pack Runner")
            wins = self.challenge_progress.get("show_runner_wins", 0) + 1
            self.challenge_progress["show_runner_wins"] = wins
            if wins >= OCEAN_RUNNER_UNLOCK_WINS:
                self.unlock_skin("ocean_runner", "3 Show Runner wins completed")

            kills = self.challenge_progress.get("show_runner_kills", 0) + 1
            self.challenge_progress["show_runner_kills"] = kills
            if kills >= SHOW_RUNNER_MASTERY_1_KILLS:
                self.unlock_skin("show_runner_mastery_1", "20 Show Runner kills completed")
            if kills >= SHOW_RUNNER_MASTERY_2_KILLS:
                self.unlock_skin("show_runner_mastery_2", "40 Show Runner kills completed")
            if kills >= SHOW_RUNNER_MASTERY_3_KILLS:
                self.unlock_skin("show_runner_mastery_3", "61 Show Runner kills completed")

        if (
            self.player_role == "Killer"
            and self.round_killer == "subslasher"
            and self.selected_skins.get("subslasher") == "tennis_dude"
        ):
            self.unlock_skin("pickle_ball_bro", "won with Tennis Dude")

        if self.player_role == "Killer" and self.round_killer == "vengance_bot":
            wins = self.challenge_progress.get("vengance_bot_wins", 0) + 1
            self.challenge_progress["vengance_bot_wins"] = wins
            if wins >= VENGANCE_BOT_MASTERY_1_WINS:
                self.unlock_skin("vengance_bot_mastery_1", "20 Vengance Bot wins completed")
            if wins >= VENGANCE_BOT_MASTERY_2_WINS:
                self.unlock_skin("vengance_bot_mastery_2", "50 Vengance Bot wins completed")
            if wins >= VENGANCE_BOT_MASTERY_3_WINS:
                self.unlock_skin("vengance_bot_mastery_3", "79 Vengance Bot wins completed")

        if self.player_role == "Survivor" and self.round_killer == "vengance_bot":
            self.record_vengance_bot_survive()

        self.save_progress()

    def record_loss(self) -> None:
        if self.player_role == "Killer" and self.round_killer == "revenge_bot":
            losses = self.challenge_progress.get("ducky_losses", 0) + 1
            self.challenge_progress["ducky_losses"] = losses
            if losses >= DUCKY_INVERTED_LOSSES:
                self.unlock_skin("ducky_inverted", "lost twice as Ducky")
            if losses >= DUCKY_OGEL_LOSSES:
                self.unlock_skin("ducky_ogel", "lost 4 times as Ducky")

        self.save_progress()

    def record_vengance_bot_survive(self) -> None:
        survives = self.challenge_progress.get("vengance_bot_survives", 0) + 1
        self.challenge_progress["vengance_bot_survives"] = survives
        if survives >= WICK_WONALDS_SURVIVES:
            self.unlock_skin("wick_wonalds", "survived Vengance Bot twice")

    def draw(self) -> None:
        if self.state == GameState.TITLE:
            self.draw_title()
        elif self.state == GameState.ROUND_SETUP:
            self.draw_round_setup()
        elif self.state == GameState.ROLE_REVEAL:
            self.draw_role_reveal()
        elif self.state == GameState.PLAYING:
            self.draw_gameplay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        self.draw_fullscreen_button()
        pygame.display.flip()

    def draw_fullscreen_button(self) -> None:
        self.fullscreen_button.text = "Exit" if self.fullscreen else "Full"
        self.fullscreen_button.draw(self.screen, self.font_small, self.fullscreen)

    def draw_title(self) -> None:
        self.screen.fill((10, 16, 30))
        self.draw_arena_preview()
        draw_text(self.screen, self.font_title, "Tag 2.0", (248, 250, 252), (WIDTH // 2, 160), True)
        draw_text(
            self.screen,
            self.font_medium,
            "Random role. Survive twice or catch.",
            (203, 213, 225),
            (WIDTH // 2, 245),
            True,
        )
        draw_text(
            self.screen,
            self.font_small,
            "WASD / Arrows move  |  Space attacks as killer  |  Escape quits",
            (148, 163, 184),
            (WIDTH // 2, 305),
            True,
        )
        self.menu_buttons["play"].draw(self.screen, self.font_medium, True)
        draw_text(
            self.screen,
            self.font_small,
            "Press Enter or click Start",
            (203, 213, 225),
            (WIDTH // 2, 528),
            True,
        )

    def draw_round_setup(self) -> None:
        self.screen.fill((13, 22, 36))
        draw_text(
            self.screen,
            self.font_large,
            "Round Setup",
            (248, 250, 252),
            (WIDTH // 2, 78),
            True,
        )
        draw_text(
            self.screen,
            self.font_small,
            "Choose your killer if your random role is Killer. Survivor rounds still use a random AI killer.",
            (203, 213, 225),
            (WIDTH // 2, 123),
            True,
        )

        for index, killer_id in enumerate(KILLER_IDS):
            data = KILLERS[killer_id]
            panel = self.killer_card_rect(index)
            is_selected = killer_id == self.selected_player_killer
            pygame.draw.rect(self.screen, (24, 34, 52), panel, border_radius=12)
            pygame.draw.rect(
                self.screen,
                (248, 199, 88) if is_selected else (77, 88, 106),
                panel,
                4 if is_selected else 3,
                border_radius=12,
            )
            draw_text(
                self.screen,
                self.font_small,
                str(index + 1),
                (248, 199, 88) if is_selected else (148, 163, 184),
                (panel.left + 13, panel.top + 10),
            )

            sprite = self.sprites.get(killer_id)
            preview_rect = pygame.Rect(0, 0, 82, 82)
            preview_rect.center = (panel.centerx, panel.top + 56)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, data["color"], preview_rect)

            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["name"],
                (248, 250, 252),
                pygame.Rect(panel.left + 10, panel.top + 106, panel.width - 20, 44),
            )
            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["attack_name"],
                (248, 199, 88),
                pygame.Rect(panel.left + 10, panel.top + 155, panel.width - 20, 48),
            )
            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["description"],
                (177, 188, 205),
                pygame.Rect(panel.left + 10, panel.top + 218, panel.width - 20, 58),
            )

        selected_name = KILLERS[self.selected_player_killer]["name"]
        draw_text(
            self.screen,
            self.font_small,
            f"Selected killer if you become Killer: {selected_name}",
            (248, 199, 88),
            (WIDTH // 2, 492),
            True,
        )
        self.menu_buttons["reveal"].draw(self.screen, self.font_medium, True)
        draw_text(
            self.screen,
            self.font_small,
            "Click a killer or press 1-5. Skin selection appears after you become Killer.",
            (203, 213, 225),
            (WIDTH // 2, 660),
            True,
        )

    def draw_role_reveal(self) -> None:
        self.screen.fill((10, 16, 30))
        selected = KILLERS[self.round_killer]
        role_color = (96, 165, 250) if self.player_role == "Survivor" else (248, 113, 113)

        draw_text(self.screen, self.font_large, "Role Reveal", (248, 250, 252), (WIDTH // 2, 125), True)
        draw_text(self.screen, self.font_title, self.player_role, role_color, (WIDTH // 2, 240), True)
        draw_text(
            self.screen,
            self.font_medium,
            f"Round killer: {selected['name']}",
            (226, 232, 240),
            (WIDTH // 2, 330),
            True,
        )

        if self.player_role == "Survivor":
            prompt = "Survive two 60-second lives while the random killer hunts you."
        else:
            prompt = "Catch the AI survivor with your selected killer before time runs out."
        draw_text(self.screen, self.font_medium, prompt, (203, 213, 225), (WIDTH // 2, 380), True)
        if self.player_role == "Killer":
            self.draw_skin_selection()
        self.menu_buttons["begin"].draw(self.screen, self.font_medium, True)

    def draw_skin_selection(self) -> None:
        draw_text(
            self.screen,
            self.font_medium,
            "Choose Skin",
            (248, 250, 252),
            (WIDTH // 2, 420),
            True,
        )

        for index, skin_id in enumerate(self.skin_options_for_killer(self.round_killer)):
            rect = self.skin_card_rect(index)
            selected = self.selected_skins.get(self.round_killer, "classic") == skin_id
            unlocked = skin_id == "classic" or self.skin_unlocked(skin_id)
            fill = (25, 42, 37) if unlocked else (35, 35, 42)
            outline = (248, 199, 88) if selected else (88, 100, 116)
            pygame.draw.rect(self.screen, fill, rect, border_radius=8)
            pygame.draw.rect(self.screen, outline, rect, 3 if selected else 2, border_radius=8)

            sprite_key = self.skin_sprite_key(self.round_killer, skin_id)
            sprite = self.sprites.get(sprite_key)
            preview_rect = pygame.Rect(rect.left + 8, rect.top + 13, 44, 44)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, KILLERS[self.round_killer]["color"], preview_rect)

            draw_text(
                self.screen,
                self.font_small,
                f"{index + 1}. {self.skin_name(self.round_killer, skin_id)}",
                (248, 250, 252) if unlocked else (148, 163, 184),
                (rect.left + 60, rect.top + 9),
            )

            status = "Unlocked" if unlocked else f"Locked: {self.skin_challenge_text(skin_id)}"
            draw_wrapped_text(
                self.screen,
                self.font_small,
                status,
                (134, 239, 172) if unlocked else (248, 199, 88),
                pygame.Rect(rect.left + 60, rect.top + 32, rect.width - 68, 30),
            )

        if self.skin_notice:
            draw_wrapped_text(
                self.screen,
                self.font_small,
                self.skin_notice,
                (203, 213, 225),
                pygame.Rect(150, 582, 700, 36),
            )

    def skin_challenge_text(self, skin_id: str) -> str:
        if skin_id == "fried_chicken":
            remaining = max(0, FRIED_CHICKEN_UNLOCK_WINS - self.total_wins)
            return f"win {remaining} more"
        if skin_id in ("ducky_inverted", "ducky_ogel"):
            target = DUCKY_INVERTED_LOSSES if skin_id == "ducky_inverted" else DUCKY_OGEL_LOSSES
            losses = self.challenge_progress.get("ducky_losses", 0)
            return f"Ducky losses {losses}/{target}"
        if skin_id == "ocean_runner":
            wins = self.challenge_progress.get("show_runner_wins", 0)
            return f"Show Runner wins {wins}/{OCEAN_RUNNER_UNLOCK_WINS}"
        if skin_id in ("show_runner_mastery_1", "show_runner_mastery_2", "show_runner_mastery_3"):
            target = self.show_runner_mastery_kill_target(skin_id)
            kills = self.challenge_progress.get("show_runner_kills", 0)
            return f"Show Runner kills {kills}/{target}"
        if skin_id == "wick_wonalds":
            survives = self.challenge_progress.get("vengance_bot_survives", 0)
            return f"survive Vengance Bot {survives}/{WICK_WONALDS_SURVIVES}"
        if skin_id in ("vengance_bot_mastery_1", "vengance_bot_mastery_2", "vengance_bot_mastery_3"):
            target = self.vengance_bot_mastery_win_target(skin_id)
            wins = self.challenge_progress.get("vengance_bot_wins", 0)
            return f"Vengance Bot wins {wins}/{target}"
        return SKINS[skin_id]["challenge"]

    def show_runner_mastery_kill_target(self, skin_id: str) -> int:
        if skin_id == "show_runner_mastery_1":
            return SHOW_RUNNER_MASTERY_1_KILLS
        if skin_id == "show_runner_mastery_2":
            return SHOW_RUNNER_MASTERY_2_KILLS
        return SHOW_RUNNER_MASTERY_3_KILLS

    def vengance_bot_mastery_win_target(self, skin_id: str) -> int:
        if skin_id == "vengance_bot_mastery_1":
            return VENGANCE_BOT_MASTERY_1_WINS
        if skin_id == "vengance_bot_mastery_2":
            return VENGANCE_BOT_MASTERY_2_WINS
        return VENGANCE_BOT_MASTERY_3_WINS

    def skin_challenge_detail(self, skin_id: str) -> str:
        if skin_id == "fried_chicken":
            remaining = max(0, FRIED_CHICKEN_UNLOCK_WINS - self.total_wins)
            return f"Win {remaining} more round{'s' if remaining != 1 else ''} to unlock Fried Chicken."
        if skin_id == "ducky_inverted":
            losses = self.challenge_progress.get("ducky_losses", 0)
            remaining = max(0, DUCKY_INVERTED_LOSSES - losses)
            return f"Play as Ducky and lose {remaining} more round{'s' if remaining != 1 else ''}."
        if skin_id == "ducky_ogel":
            losses = self.challenge_progress.get("ducky_losses", 0)
            remaining = max(0, DUCKY_OGEL_LOSSES - losses)
            return f"Play as Ducky and lose {remaining} more round{'s' if remaining != 1 else ''}."
        if skin_id == "tennis_dude":
            return "Play as Subslasher and hit the survivor with Perpelling Shootdown, the freeze ice spike."
        if skin_id == "pickle_ball_bro":
            return "Play as Subslasher, select the Tennis Dude skin, then win the round."
        if skin_id == "pack_runner":
            return "Play as Show Runner and run around the arena perimeter 3 times in a row."
        if skin_id == "maldin_inverted":
            return "Play as Show Runner, select the Pack Runner skin, then win the round."
        if skin_id == "ocean_runner":
            wins = self.challenge_progress.get("show_runner_wins", 0)
            remaining = max(0, OCEAN_RUNNER_UNLOCK_WINS - wins)
            return f"Win {remaining} more round{'s' if remaining != 1 else ''} as Show Runner."
        if skin_id in ("show_runner_mastery_1", "show_runner_mastery_2", "show_runner_mastery_3"):
            target = self.show_runner_mastery_kill_target(skin_id)
            kills = self.challenge_progress.get("show_runner_kills", 0)
            remaining = max(0, target - kills)
            return f"Kill {remaining} more survivor{'s' if remaining != 1 else ''} as Show Runner."
        if skin_id == "wick_wonalds":
            survives = self.challenge_progress.get("vengance_bot_survives", 0)
            remaining = max(0, WICK_WONALDS_SURVIVES - survives)
            return f"Survive Vengance Bot {remaining} more time{'s' if remaining != 1 else ''} as Survivor."
        if skin_id == "mlg":
            return "Play as Vengance Bot and kill the survivor with a landmine after placing 2 or fewer landmines that round."
        if skin_id in ("vengance_bot_mastery_1", "vengance_bot_mastery_2", "vengance_bot_mastery_3"):
            target = self.vengance_bot_mastery_win_target(skin_id)
            wins = self.challenge_progress.get("vengance_bot_wins", 0)
            remaining = max(0, target - wins)
            return f"Win {remaining} more round{'s' if remaining != 1 else ''} as Vengance Bot."
        return SKINS[skin_id]["challenge"]

    def draw_gameplay(self) -> None:
        self.screen.fill((12, 19, 32))
        self.draw_arena()

        for hitbox in self.active_hitboxes:
            hitbox.draw(self.screen)

        for projectile in self.projectiles:
            projectile.draw(self.screen)

        for belt in self.ducky_belts:
            belt.draw(self.screen)

        for mine in self.landmines:
            mine.draw(self.screen)

        if self.survivor is not None:
            self.survivor.draw(self.screen, self.font_small)

        for killer in self.killers:
            if killer is not self.survivor:
                killer.draw(self.screen, self.font_small)

        self.draw_hud()

    def draw_arena_preview(self) -> None:
        preview = pygame.Rect(145, 355, 710, 210)
        pygame.draw.rect(self.screen, (20, 31, 48), preview, border_radius=18)
        pygame.draw.rect(self.screen, (64, 77, 98), preview, 2, border_radius=18)
        for x in range(preview.left + 28, preview.right, 58):
            pygame.draw.line(self.screen, (28, 41, 62), (x, preview.top + 10), (x, preview.bottom - 10))
        for y in range(preview.top + 28, preview.bottom, 58):
            pygame.draw.line(self.screen, (28, 41, 62), (preview.left + 10, y), (preview.right - 10, y))

    def draw_arena(self) -> None:
        pygame.draw.rect(self.screen, (20, 31, 48), ARENA_RECT, border_radius=12)
        pygame.draw.rect(self.screen, (91, 106, 130), ARENA_RECT, 3, border_radius=12)

        for x in range(ARENA_RECT.left + 40, ARENA_RECT.right, 40):
            pygame.draw.line(
                self.screen,
                (28, 41, 62),
                (x, ARENA_RECT.top),
                (x, ARENA_RECT.bottom),
                1,
            )
        for y in range(ARENA_RECT.top + 40, ARENA_RECT.bottom, 40):
            pygame.draw.line(
                self.screen,
                (28, 41, 62),
                (ARENA_RECT.left, y),
                (ARENA_RECT.right, y),
                1,
            )

        for wall in self.walls:
            wall.draw(self.screen)

    def draw_hud(self) -> None:
        pygame.draw.rect(self.screen, (5, 10, 20), pygame.Rect(0, 0, WIDTH, 92))
        pygame.draw.line(self.screen, (51, 65, 85), (0, 92), (WIDTH, 92), 2)

        selected = KILLERS[self.round_killer]
        draw_text(self.screen, self.font_medium, "Tag 2.0", (248, 250, 252), (24, 14))
        draw_text(
            self.screen,
            self.font_small,
            self.hud_role_text(selected["name"]),
            (203, 213, 225),
            (24, 50),
        )

        draw_text(
            self.screen,
            self.font_large,
            f"{math.ceil(self.round_time):02d}",
            (248, 250, 252),
            (WIDTH // 2, 45),
            True,
        )

        if self.player_role == "Survivor":
            status = "Survive!"
            detail = self.survivor_status_message or "WASD / Arrows move"
        else:
            status = "Catch the survivor!"
            detail = "Space attacks"
            if isinstance(self.player, Killer):
                if self.player.is_ducky():
                    detail = self.ducky_ability_status(self.player)
                elif self.player.is_malice():
                    detail = self.malice_ability_status(self.player)
                elif self.player.is_subslasher():
                    detail = self.subslasher_ability_status()
                elif self.player.is_show_runner():
                    detail = self.show_runner_ability_status(self.player)
                elif self.player.is_vengance_bot():
                    detail = self.vengance_ability_status(self.player)

        draw_text(self.screen, self.font_small, status, (248, 199, 88), (760, 14))
        draw_text(self.screen, self.font_small, detail, (203, 213, 225), (760, 39))

        if isinstance(self.player, Killer):
            cooldown_status = self.player.cooldown_status()
            draw_text(self.screen, self.font_small, cooldown_status, (226, 232, 240), (760, 64))
            self.draw_cooldown_bar(self.player)

    def hud_role_text(self, killer_name: str) -> str:
        text = f"Role: {self.player_role}  |  Round killer: {killer_name}"
        if self.player_role == "Survivor":
            text += f"  |  Life: {self.survivor_life_number}/{SURVIVOR_TOTAL_LIVES}"
        return text

    def malice_ability_status(self, malice: Killer) -> str:
        roar = "H: roar"
        if self.survivor_stun_timer > 0:
            roar = f"Stun {self.survivor_stun_timer:.1f}s"
        return f"{malice.wall_phase_status()} | {roar}"

    def subslasher_ability_status(self) -> str:
        if self.survivor_stun_timer > 0:
            return f"Frozen {self.survivor_stun_timer:.1f}s | E kill | Q cubes"
        return "I freeze | E kill | Q cubes"

    def ducky_ability_status(self, ducky: Killer) -> str:
        swing = "C swing"
        hg = "Y HG"
        if ducky.ducky_swing_cooldown > 0:
            swing = f"C cooldown {ducky.ducky_swing_cooldown:.1f}s"
        if ducky.ducky_hg_timer > 0:
            hg = f"HG {ducky.ducky_hg_timer:.1f}s"
        elif ducky.ducky_hg_cooldown > 0:
            hg = f"Y cooldown {ducky.ducky_hg_cooldown:.0f}s"
        return f"{swing} | {hg}"

    def show_runner_ability_status(self, show_runner: Killer) -> str:
        slow = "9 slow"
        speed = "A speed"
        if self.survivor_slow_timer > 0:
            slow = f"Slow {self.survivor_slow_timer:.1f}s"
        if show_runner.show_power_timer > 0:
            speed = f"Speed {show_runner.show_power_timer:.1f}s"
        return f"{slow} | U hook | {speed}"

    def vengance_ability_status(self, vengance_bot: Killer) -> str:
        dash = "R dash"
        mine = "C mine"
        if vengance_bot.vengance_dash_timer > 0:
            dash = f"Dash {vengance_bot.vengance_dash_timer:.1f}s"
        elif vengance_bot.vengance_dash_cooldown > 0:
            dash = f"R cooldown {vengance_bot.vengance_dash_cooldown:.0f}s"
        if vengance_bot.vengance_mine_cooldown > 0:
            mine = f"C cooldown {vengance_bot.vengance_mine_cooldown:.0f}s"
        return f"{dash} | {mine}"

    def draw_cooldown_bar(self, killer: Killer) -> None:
        bar = pygame.Rect(592, 62, 140, 14)
        pygame.draw.rect(self.screen, (31, 41, 55), bar, border_radius=7)

        if killer.attack_phase is not None:
            progress = 1.0
        elif killer.cooldown_remaining <= 0:
            progress = 1.0
        else:
            progress = 1.0 - (killer.cooldown_remaining / killer.data["cooldown"])

        fill = bar.copy()
        fill.width = max(0, int(bar.width * progress))
        pygame.draw.rect(self.screen, (34, 197, 94), fill, border_radius=7)
        pygame.draw.rect(self.screen, (148, 163, 184), bar, 2, border_radius=7)

    def draw_game_over(self) -> None:
        self.screen.fill((10, 16, 30))
        self.draw_arena_preview()

        result = "YOU WIN" if self.player_won else "YOU LOSE"
        color = (74, 222, 128) if self.player_won else (248, 113, 113)
        draw_text(self.screen, self.font_title, result, color, (WIDTH // 2, 160), True)
        draw_text(self.screen, self.font_medium, self.end_reason, (226, 232, 240), (WIDTH // 2, 255), True)
        skin_text = self.skin_progress_text()
        draw_text(self.screen, self.font_small, skin_text, (248, 199, 88), (WIDTH // 2, 292), True)
        if self.skin_notice:
            draw_text(self.screen, self.font_small, self.skin_notice, (134, 239, 172), (WIDTH // 2, 320), True)
        draw_text(
            self.screen,
            self.font_small,
            "Press R to restart from the title screen. Press Escape to quit.",
            (203, 213, 225),
            (WIDTH // 2, 355),
            True,
        )

    def skin_progress_text(self) -> str:
        unlocked_count = len(self.unlocked_skins)
        total_count = len(SKINS)
        if unlocked_count == total_count:
            return "All killer cosmetics unlocked."
        return f"Killer cosmetics unlocked: {unlocked_count}/{total_count}. Keep clearing challenges."


def main() -> None:
    game = Game()
    if "--smoke-test" in sys.argv:
        game.smoke_test()
    else:
        game.run()


if __name__ == "__main__":
    main()

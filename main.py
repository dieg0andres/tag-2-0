from __future__ import annotations

import json
import math
import random
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pygame


WIDTH = 1280
HEIGHT = 800
FPS = 60
ROUND_DURATION = 60.0
SURVIVOR_TOTAL_LIVES = 2

ROOT_DIR = Path(__file__).resolve().parent
ASSET_DIR = ROOT_DIR / "assets"
SPRITE_DIR = ASSET_DIR / "sprites"
ANIMATION_DIR = SPRITE_DIR / "animations"
SAVE_FILE = ROOT_DIR / "save_data.json"

UI_MARGIN = 24
TOP_BAR_HEIGHT = 88
SIDE_PANEL_WIDTH = 330
PANEL_GAP = 18
PANEL_RADIUS = 8

ARENA_RECT = pygame.Rect(
    UI_MARGIN,
    TOP_BAR_HEIGHT + UI_MARGIN,
    WIDTH - SIDE_PANEL_WIDTH - PANEL_GAP - UI_MARGIN * 2,
    HEIGHT - TOP_BAR_HEIGHT - UI_MARGIN * 2,
)
SIDE_PANEL_RECT = pygame.Rect(
    ARENA_RECT.right + PANEL_GAP,
    ARENA_RECT.top,
    SIDE_PANEL_WIDTH,
    ARENA_RECT.height,
)
TIMER_PANEL_RECT = pygame.Rect(
    SIDE_PANEL_RECT.left,
    SIDE_PANEL_RECT.top,
    SIDE_PANEL_RECT.width,
    122,
)
STATUS_PANEL_RECT = pygame.Rect(
    SIDE_PANEL_RECT.left,
    TIMER_PANEL_RECT.bottom + 14,
    SIDE_PANEL_RECT.width,
    118,
)
ABILITY_PANEL_RECT = pygame.Rect(
    SIDE_PANEL_RECT.left,
    STATUS_PANEL_RECT.bottom + 14,
    SIDE_PANEL_RECT.width,
    258,
)
COMBAT_PANEL_RECT = pygame.Rect(
    SIDE_PANEL_RECT.left,
    ABILITY_PANEL_RECT.bottom + 14,
    SIDE_PANEL_RECT.width,
    SIDE_PANEL_RECT.bottom - (ABILITY_PANEL_RECT.bottom + 14),
)
CHARACTER_COLLISION_SIZE = 44
SPRITE_DRAW_SIZE = 64
WALK_ANIMATION_SPEED = 0.10

SURVIVOR_SPEED = 260
AI_KILLER_SPEED_MULTIPLIER = 0.90
MALICE_WALL_PHASE_DURATION = 4.0
MALICE_WALL_PHASE_COOLDOWN = 20.0
MALICE_HUNTER_RAGE_DURATION = 20.0
MALICE_HUNTER_RAGE_COOLDOWN = 5.0
MALICE_TIGER_SPEED_MULTIPLIER = 1.69
MALICE_TIGER_INVISIBLE_DURATION = 5.0
MALICE_FORM_ABILITY_COOLDOWN = 5.0
MALICE_BIRD_HELPER_SLOW_DURATION = 5.0
MALICE_BIRD_POOP_STUN_DURATION = 2.5
MALICE_BIRD_POOP_SPEED = 560
MALICE_BIRD_POOP_LIFETIME = 1.25
MALICE_DINOSAUR_SPEED_MULTIPLIER = 0.90
MALICE_DINOSAUR_SHOCKWAVE_RADIUS = 130
MALICE_DINOSAUR_SHOCKWAVE_VISUAL_DURATION = 0.45
MALICE_DINOSAUR_ROAR_STUN_DURATION = 16.0
MALICE_FORM_ANIMATION_SPEED = 0.16
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
ODD_FLASH_STUN_DURATION = 5.0
ODD_FLASH_VISUAL_DURATION = 0.55
ODD_FLASH_COOLDOWN = 5.0
EXPLORER_ADRENALINE_DURATION = 5.0
EXPLORER_ADRENALINE_SPEED_MULTIPLIER = 1.60
EXPLORER_TAMING_DURATION = 5.0
EXPLORER_TAMING_SPEED_MULTIPLIER = 0.50
KITTY_TELEPORT_MARKER_RADIUS = 24
QUEEN_GOOPY_KNIGHT_STUN_DURATION = 2.3
QUEEN_GOOPY_KNIGHT_SPEED = 330
QUEEN_GOOPY_KNIGHT_COOLDOWN = 10.0
KEVIN_PUNCH_DURATION = 5.0
KEVIN_PUNCH_COOLDOWN = 5.0
KEVIN_PUNCH_STUN_DURATION = 2.0
KEVIN_DOUBLE_SPEED_DURATION = 5.0
KEVIN_DOUBLE_SPEED_MULTIPLIER = 1.89
TRASHY_GUN_TARGET_HITS = 10
TRASHY_GUN_STUN_DURATION = 4.0
TRASHY_GUN_SHOT_SPEED = 720
TRASHY_GUN_SHOT_LIFETIME = 1.2
TRASHY_ABILITY_COOLDOWN = 5.0
TRASHY_SHOCK_STUN_DURATION = 5.0
TRASHY_SHOCK_SHOT_SPEED = 650
TRASHY_SHOCK_SHOT_LIFETIME = 1.0
TRASHY_SHOCK_KNOCKBACK = 120
TRASHY_SHOCK_TIMER_DROP = 10.0
TRASHY_TURRET_STUN_DURATION = 2.5
TRASHY_TURRET_RANGE = 170
TRASHY_TURRET_SHOT_SPEED = 520
TRASHY_TURRET_SHOT_LIFETIME = 0.9
TRASHY_TURRET_DURATION = 18.0
TRASHY_TURRET_FIRE_COOLDOWN = 1.4
TRASHY_MAX_TURRETS = 2
TRASHY_MINIGAME_BAR = pygame.Rect(
    ARENA_RECT.left + 170,
    ARENA_RECT.bottom - 42,
    ARENA_RECT.width - 340,
    28,
)
TRASHY_MINIGAME_TARGET_SIZE = 26
TRASHY_MINIGAME_CIRCLE_RADIUS = 12
TRASHY_MINIGAME_CIRCLE_SPEED = 280
SURVIVOR_ABILITY_COOLDOWN = 5.0
SHOW_RUNNER_SLOW_COOLDOWN = 5.0
SHOW_RUNNER_HOOK_COOLDOWN = 2.0
SHOW_RUNNER_SPEED_COOLDOWN = 3.0
SUBSLASHER_FREEZE_SPIKE_COOLDOWN = 5.0
SUBSLASHER_KILL_SPIKE_COOLDOWN = 3.0
SUBSLASHER_SUBZERO_COOLDOWN = 12.0

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
    "ducky_daddys_belt": {
        "killer_id": "revenge_bot",
        "name": "Daddy's Belt",
        "sprite_key": "ducky_daddys_belt",
        "challenge": "Kill the survivor with Ducky's C swing ability.",
    },
    "ducky_subject_5_png": {
        "killer_id": "revenge_bot",
        "name": "Subject 5 PNG",
        "sprite_key": "ducky_subject_5_png",
        "challenge": "Win with both the Daddy's Belt and Ogel skins.",
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
    "vengance_scoreboard": {
        "killer_id": "vengance_bot",
        "name": "Scoreboard",
        "sprite_key": "vengance_scoreboard",
        "challenge": "Win as Vengance Bot without placing a landmine.",
    },
    "vengance_spinning": {
        "killer_id": "vengance_bot",
        "name": "Spinning",
        "sprite_key": "vengance_spinning",
        "challenge": "Run one full lap around the arena perimeter with any player character.",
    },
    "vengance_werewolf": {
        "killer_id": "vengance_bot",
        "name": "Werewolf",
        "sprite_key": "vengance_werewolf",
        "challenge": "Win 2 rounds as Vengance Bot while placing 3 or fewer landmines each round.",
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

SURVIVORS = {
    "survivor": {
        "name": "Runner",
        "sprite": "survivor.png",
        "description": "Fast classic runner.",
    },
    "survivor_odd": {
        "name": "Odd 1 3 5 7 9",
        "sprite": "survivor_odd.png",
        "description": "F: flash the killer with Picture Taken.",
    },
    "survivor_explorer": {
        "name": "Explorer",
        "sprite": "survivor_explorer.png",
        "description": "A: adrenaline and tame the killer.",
    },
    "survivor_kitty": {
        "name": "Kitty",
        "sprite": "survivor_kitty.png",
        "description": "L then 2: place and use a teleport circle.",
    },
    "survivor_kevin": {
        "name": "Kevin",
        "sprite": "survivor_kevin.png",
        "description": "P: punch. S: spin into double speed.",
    },
    "survivor_trashy": {
        "name": "Trashy",
        "sprite": "survivor_trashy.png",
        "description": "G: Gun Maker. C: cannon. T: turret.",
    },
    "survivor_queen_goopy": {
        "name": "Queen Goopy",
        "sprite": "survivor_queen_goopy.png",
        "description": "K: summon 2 stunning gray knights.",
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
SURVIVOR_IDS = tuple(SURVIVORS.keys())


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
    """Trashy's earned gun shot. It stuns a killer instead of ending the round."""

    def __init__(self, origin: pygame.Vector2, direction: pygame.Vector2) -> None:
        self.pos = pygame.Vector2(origin)
        self.direction = safe_normalize(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(0, -1)
        self.lifetime = TRASHY_GUN_SHOT_LIFETIME
        self.rect = pygame.Rect(0, 0, 22, 12)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt: float, walls: list[Wall]) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False
        self.pos += self.direction * TRASHY_GUN_SHOT_SPEED * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not ARENA_RECT.colliderect(self.rect):
            return False
        return not any(self.rect.colliderect(wall.rect) for wall in walls)

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

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        draw_rect = pygame.Rect(0, 0, SPRITE_DRAW_SIZE, SPRITE_DRAW_SIZE)
        draw_rect.center = self.rect.center

        sprite = self.sprite
        if self.walk_frames and self.is_moving and self.sprite is self.base_sprite:
            sprite = self.walk_frames[self.walk_animation_index % len(self.walk_frames)]

        if sprite is not None:
            if self.sprite_alpha < 255:
                faded = sprite.copy()
                faded.set_alpha(self.sprite_alpha)
                surface.blit(faded, draw_rect)
            else:
                surface.blit(sprite, draw_rect)
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
        self.is_moving = False


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
        padding = TRASHY_MINIGAME_TARGET_SIZE // 2 + 4
        self.trashy_target_x = float(
            random.randint(TRASHY_MINIGAME_BAR.left + padding, TRASHY_MINIGAME_BAR.right - padding)
        )

    def trashy_target_rect(self) -> pygame.Rect:
        rect = pygame.Rect(0, 0, TRASHY_MINIGAME_TARGET_SIZE, TRASHY_MINIGAME_TARGET_SIZE)
        rect.center = (round(self.trashy_target_x), TRASHY_MINIGAME_BAR.centery)
        return rect

    def trashy_circle_rect(self) -> pygame.Rect:
        radius = TRASHY_MINIGAME_CIRCLE_RADIUS
        rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        rect.center = (round(self.trashy_circle_x), TRASHY_MINIGAME_BAR.centery)
        return rect


class Killer(Character):
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
        return self.is_hunter_rage_active() and self.malice_form == "dinosaur"

    def is_subslasher(self) -> bool:
        return self.killer_id == "subslasher"

    def is_show_runner(self) -> bool:
        return self.killer_id == "show_runner"

    def is_vengance_bot(self) -> bool:
        return self.killer_id == "vengance_bot"

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        if self.skin_id != "vengance_spinning" or self.sprite is None:
            super().draw(surface, font)
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

        facing = safe_normalize(self.facing)
        if facing.length_squared() > 0:
            start = pygame.Vector2(self.rect.center)
            end = start + facing * 31
            pygame.draw.line(surface, (255, 255, 255), start, end, 3)

        label = font.render(self.name, True, (226, 232, 240))
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.top - 11))
        surface.blit(label, label_rect)
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

    def start_hunter_rage(self) -> str | None:
        if not self.is_malice() or self.is_hunter_rage_active() or self.malice_hunter_cooldown > 0:
            return None

        self.malice_form = random.choice(("tiger", "bird", "dinosaur"))
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
        self.selected_player_survivor = "survivor"
        self.save_data = self.load_save_data()
        self.total_wins = self.save_data["total_wins"]
        self.unlocked_skins: set[str] = set(self.save_data["unlocked_skins"])
        self.challenge_progress: dict[str, int] = dict(self.save_data["challenge_progress"])
        self.selected_skins = {killer_id: "classic" for killer_id in KILLER_IDS}
        self.skin_notice = ""
        self.show_runner_perimeter_next = 0
        self.show_runner_perimeter_laps = 0
        self.last_perimeter_edge: str | None = None
        self.spinning_perimeter_next: int | None = None
        self.spinning_perimeter_edges = 0
        self.last_spinning_perimeter_edge: str | None = None
        self.vengance_mines_placed_this_round = 0
        self.player_role = "Survivor"
        self.round_time = ROUND_DURATION
        self.survivor_life_number = 1
        self.survivor_status_message = ""
        self.survivor_stun_timer = 0.0
        self.survivor_slow_timer = 0.0
        self.survivor_flash_timer = 0.0
        self.explorer_taming_timer = 0.0
        self.player_won = False
        self.end_reason = ""

        self.sprites = self.load_sprites()
        self.walk_sprites = self.load_walk_sprites()
        self.animation_sprites = self.load_animation_sprites()
        self.walls = self.create_walls()
        self.player: Character | None = None
        self.survivor: Survivor | None = None
        self.killers: list[Killer] = []
        self.active_hitboxes: list[AttackHitbox] = []
        self.projectiles: list[IceProjectile] = []
        self.ducky_belts: list[DuckyBelt] = []
        self.landmines: list[VenganceLandmine] = []
        self.survivor_shots: list[SurvivorShot] = []
        self.trashy_shockwaves: list[TrashyShockWave] = []
        self.trashy_turrets: list[TrashyTurret] = []
        self.trashy_turret_shots: list[TrashyTurretShot] = []
        self.goopy_knights: list[GoopyKnight] = []
        self.malice_bird_poops: list[MaliceBirdPoop] = []
        self.malice_helper_birds: list[MaliceHelperBird] = []
        self.dinosaur_shockwave_timer = 0.0
        self.dinosaur_shockwave_pos = pygame.Vector2()

        button_x = WIDTH // 2 - 110
        self.menu_buttons = {
            "play": Button(pygame.Rect(button_x, 450, 220, 58), "Start"),
            "reveal": Button(pygame.Rect(button_x, 585, 220, 58), "Reveal Role"),
            "begin": Button(pygame.Rect(button_x, 622, 220, 58), "Begin Round"),
        }
        self.fullscreen_button = Button(pygame.Rect(WIDTH - 78, 10, 58, 28), "Full")

        self.audio_enabled = False
        self.music_tracks: dict[str, Path] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.setup_audio()

    def load_sprites(self) -> dict[str, pygame.Surface]:
        sprites: dict[str, pygame.Surface] = {}
        for key, path in self.sprite_paths().items():
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

    def sprite_paths(self) -> dict[str, Path]:
        paths = {
            survivor_id: SPRITE_DIR / data["sprite"]
            for survivor_id, data in SURVIVORS.items()
        }
        for killer_id, data in KILLERS.items():
            paths[killer_id] = SPRITE_DIR / data["sprite"]
        for skin in SKINS.values():
            paths[skin["sprite_key"]] = SPRITE_DIR / f"{skin['sprite_key']}.png"
        return paths

    def load_walk_sprites(self) -> dict[str, list[pygame.Surface]]:
        animations: dict[str, list[pygame.Surface]] = {}
        for key in self.sprite_paths():
            frames: list[pygame.Surface] = []
            for index in range(4):
                path = ANIMATION_DIR / f"{key}_walk_{index}.png"
                if not path.exists():
                    continue
                try:
                    image = pygame.image.load(str(path)).convert_alpha()
                    frames.append(
                        pygame.transform.smoothscale(
                            image,
                            (SPRITE_DRAW_SIZE, SPRITE_DRAW_SIZE),
                        )
                    )
                except pygame.error:
                    continue
            if len(frames) >= 2:
                animations[key] = frames

        return animations

    def load_animation_sprites(self) -> dict[str, list[pygame.Surface]]:
        animations: dict[str, list[pygame.Surface]] = {}
        for form in ("tiger", "bird", "dinosaur"):
            frames: list[pygame.Surface] = []
            for index in range(3):
                path = SPRITE_DIR / f"malice_{form}_{index}.png"
                if not path.exists():
                    continue
                try:
                    image = pygame.image.load(str(path)).convert_alpha()
                    frames.append(
                        pygame.transform.smoothscale(
                            image,
                            (SPRITE_DRAW_SIZE, SPRITE_DRAW_SIZE),
                        )
                    )
                except pygame.error:
                    continue
            if frames:
                animations[f"malice_{form}"] = frames
        return animations

    def load_save_data(self) -> dict[str, object]:
        default_data = {
            "total_wins": 0,
            "unlocked_skins": [],
            "challenge_progress": {
                "show_runner_wins": 0,
                "show_runner_kills": 0,
                "vengance_bot_wins": 0,
                "vengance_bot_survives": 0,
                "vengance_bot_low_mine_wins": 0,
                "ducky_losses": 0,
                "ducky_daddys_belt_wins": 0,
                "ducky_ogel_wins": 0,
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
        if clean_progress.get("vengance_bot_low_mine_wins", 0) >= 2:
            clean_unlocked.add("vengance_werewolf")
        if (
            clean_progress.get("ducky_daddys_belt_wins", 0) >= 1
            and clean_progress.get("ducky_ogel_wins", 0) >= 1
        ):
            clean_unlocked.add("ducky_subject_5_png")

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

        for sound_name in ("attack", "win", "lose", "malice_roar", "dinosaur_roar"):
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
            if self.player_role == "Survivor":
                selected_survivor = self.survivor_index_from_key(key)
                if selected_survivor is not None:
                    self.selected_player_survivor = selected_survivor
            selected_skin = self.skin_index_from_key(key)
            if self.player_role == "Killer" and selected_skin is not None:
                self.select_skin_for_round(selected_skin)
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.begin_round()

        elif self.state == GameState.PLAYING:
            if self.player_role == "Survivor" and isinstance(self.player, Survivor):
                self.handle_survivor_keydown(key)
                return

            if self.player_role != "Killer" or not isinstance(self.player, Killer):
                return

            if key == pygame.K_SPACE:
                if self.player.start_attack():
                    self.play_sound("attack")
            elif key == pygame.K_i:
                if self.player.is_malice():
                    if self.player.is_malice_tiger():
                        self.use_malice_tiger_invisibility()
                    elif self.player.is_malice_bird():
                        self.use_malice_bird_summon()
                    elif not self.player.is_hunter_rage_active():
                        self.player.start_wall_phase()
                elif self.player.is_subslasher():
                    self.fire_subslasher_spike("freeze")
            elif key == pygame.K_h:
                if self.player.is_malice():
                    self.use_malice_hunters_rage()
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
                elif self.player.is_malice_dinosaur():
                    self.use_malice_dinosaur_roar()
            elif key == pygame.K_9:
                if self.player.is_show_runner():
                    self.use_show_runner_laugh()
            elif key == pygame.K_u:
                if self.player.is_show_runner():
                    self.use_show_runner_hook()
            elif key == pygame.K_a:
                if self.player.is_show_runner():
                    self.player.start_show_power()
                elif self.player.is_malice_bird():
                    self.fire_malice_bird_poop()
            elif key == pygame.K_s:
                if self.player.is_malice_dinosaur():
                    self.use_malice_dinosaur_stomp()

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
            clicked_survivor = self.survivor_from_card_click(pos)
            if self.player_role == "Survivor" and clicked_survivor is not None:
                self.selected_player_survivor = clicked_survivor
                return

            clicked_skin = self.skin_from_card_click(pos)
            if self.player_role == "Killer" and clicked_skin is not None:
                self.select_skin_for_round(clicked_skin)
                return

            if self.menu_buttons["begin"].contains(pos):
                self.begin_round()

        elif self.state == GameState.PLAYING:
            if self.player_role == "Survivor" and isinstance(self.player, Survivor):
                self.handle_survivor_click(pos)

    def handle_survivor_keydown(self, key: int) -> None:
        if not isinstance(self.player, Survivor):
            return

        survivor = self.player
        if survivor.survivor_id == "survivor_odd" and key == pygame.K_f:
            self.use_odd_picture_taken(survivor)
        elif survivor.survivor_id == "survivor_explorer" and key == pygame.K_a:
            self.use_explorer_adrenaline_and_taming(survivor)
        elif survivor.survivor_id == "survivor_kitty":
            if key == pygame.K_l:
                self.use_kitty_marker(survivor)
            elif key == pygame.K_2:
                self.use_kitty_teleport(survivor)
        elif survivor.survivor_id == "survivor_queen_goopy" and key == pygame.K_k:
            self.use_queen_goopy_knights(survivor)
        elif survivor.survivor_id == "survivor_trashy" and key == pygame.K_g:
            self.use_trashy_gun_maker(survivor)
        elif survivor.survivor_id == "survivor_trashy" and key == pygame.K_c:
            self.use_trashy_shock_wave_cannon(survivor)
        elif survivor.survivor_id == "survivor_trashy" and key == pygame.K_t:
            self.use_trashy_turret(survivor)
        elif survivor.survivor_id == "survivor_kevin":
            if key == pygame.K_p:
                self.use_kevin_punch(survivor)
            elif key == pygame.K_s:
                self.use_kevin_double_speed(survivor)

    def handle_survivor_click(self, pos: tuple[int, int]) -> None:
        if not isinstance(self.player, Survivor):
            return
        survivor = self.player
        if survivor.survivor_id == "survivor_trashy" and survivor.trashy_minigame_active:
            self.handle_trashy_minigame_click(survivor, pos)

    def use_odd_picture_taken(self, survivor: Survivor) -> None:
        if survivor.odd_flash_cooldown > 0:
            self.survivor_status_message = (
                f"Picture Taken cooldown {survivor.odd_flash_cooldown:.1f}s."
            )
            return

        survivor.odd_flash_used = True
        survivor.odd_flash_cooldown = ODD_FLASH_COOLDOWN
        self.survivor_flash_timer = ODD_FLASH_VISUAL_DURATION
        for killer in self.killers:
            self.stun_killer(killer, ODD_FLASH_STUN_DURATION)
        self.survivor_status_message = "Picture Taken! Killer stunned."

    def use_explorer_adrenaline_and_taming(self, survivor: Survivor) -> None:
        if survivor.explorer_ability_cooldown > 0:
            self.survivor_status_message = (
                f"Explorer ability cooldown {survivor.explorer_ability_cooldown:.1f}s."
            )
            return

        survivor.explorer_adrenaline_used = True
        survivor.explorer_adrenaline_timer = EXPLORER_ADRENALINE_DURATION
        survivor.explorer_ability_cooldown = SURVIVOR_ABILITY_COOLDOWN
        self.explorer_taming_timer = EXPLORER_TAMING_DURATION
        self.survivor_status_message = "Adrenaline and Taming! You speed up, killer slows."

    def use_kitty_marker(self, survivor: Survivor) -> None:
        if survivor.kitty_marker is not None or survivor.kitty_teleport_used:
            self.survivor_status_message = "Kitty marker already set."
            return

        survivor.kitty_marker = pygame.Vector2(survivor.pos)
        self.survivor_status_message = "Blue circle placed. Press 2 to teleport."

    def use_kitty_teleport(self, survivor: Survivor) -> None:
        if survivor.kitty_marker is None:
            self.survivor_status_message = "Press L first to place the blue circle."
            return
        if survivor.kitty_teleport_used:
            self.survivor_status_message = "Kitty teleport already used."
            return

        survivor.pos = pygame.Vector2(survivor.kitty_marker)
        survivor.update_rect()
        self.resolve_wall_overlap(survivor)
        survivor.kitty_teleport_used = True
        survivor.kitty_marker = None
        self.survivor_status_message = "Teleported to the blue circle."

    def use_queen_goopy_knights(self, survivor: Survivor) -> None:
        if survivor.queen_knights_cooldown > 0:
            self.survivor_status_message = (
                f"Knights cooldown {survivor.queen_knights_cooldown:.1f}s."
            )
            return

        survivor.queen_knights_used = True
        survivor.queen_knights_cooldown = QUEEN_GOOPY_KNIGHT_COOLDOWN
        self.goopy_knights.extend(
            [
                GoopyKnight(survivor.pos, pygame.Vector2(-24, 18)),
                GoopyKnight(survivor.pos, pygame.Vector2(24, 18)),
            ]
        )
        self.survivor_status_message = "Knights summoned."

    def use_trashy_gun_maker(self, survivor: Survivor) -> None:
        if survivor.trashy_gun_ready and not survivor.trashy_gun_used:
            self.fire_trashy_gun(survivor)
            return
        if survivor.trashy_gun_used:
            self.survivor_status_message = "Trashy's gun already fired."
            return
        if survivor.trashy_minigame_active:
            self.survivor_status_message = "Click when the white circle overlaps green."
            return

        survivor.trashy_minigame_active = True
        survivor.trashy_hits = 0
        survivor.trashy_circle_x = float(TRASHY_MINIGAME_BAR.left + TRASHY_MINIGAME_CIRCLE_RADIUS)
        survivor.trashy_circle_direction = 1
        survivor.set_trashy_target()
        self.survivor_status_message = "Gun Maker started. Click the overlap 10 times."

    def handle_trashy_minigame_click(self, survivor: Survivor, pos: tuple[int, int]) -> None:
        circle = survivor.trashy_circle_rect()
        target = survivor.trashy_target_rect()
        if circle.colliderect(target) and circle.collidepoint(pos):
            survivor.trashy_hits += 1
            if survivor.trashy_hits >= TRASHY_GUN_TARGET_HITS:
                survivor.trashy_minigame_active = False
                survivor.trashy_gun_ready = True
                self.survivor_status_message = "Gun ready. Press G to fire."
            else:
                survivor.set_trashy_target()
                self.survivor_status_message = f"Gun Maker {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}"
            return

        survivor.trashy_hits = 0
        survivor.set_trashy_target()
        self.survivor_status_message = "Missed. Gun Maker reset to 0."

    def fire_trashy_gun(self, survivor: Survivor) -> None:
        direction = safe_normalize(survivor.facing)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, -1)
        self.survivor_shots.append(SurvivorShot(survivor.pos + direction * 35, direction))
        survivor.trashy_gun_ready = False
        survivor.trashy_gun_used = True
        self.survivor_status_message = "Trashy fired the gun."

    def use_trashy_shock_wave_cannon(self, survivor: Survivor) -> None:
        if survivor.trashy_shock_cooldown > 0:
            self.survivor_status_message = (
                f"Shock Wave Cannon cooldown {survivor.trashy_shock_cooldown:.1f}s."
            )
            return

        direction = safe_normalize(survivor.facing)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, -1)

        self.trashy_shockwaves.append(TrashyShockWave(survivor.pos + direction * 42, direction))
        survivor.trashy_shock_cooldown = TRASHY_ABILITY_COOLDOWN
        self.survivor_status_message = "Shock Wave Cannon fired."

    def use_trashy_turret(self, survivor: Survivor) -> None:
        if len(self.trashy_turrets) >= TRASHY_MAX_TURRETS:
            self.survivor_status_message = "Devils Work limit reached: 2 turrets."
            return
        if survivor.trashy_turret_cooldown > 0:
            self.survivor_status_message = (
                f"Devils Work cooldown {survivor.trashy_turret_cooldown:.1f}s."
            )
            return

        turret = TrashyTurret(survivor.pos)
        if any(turret.rect.colliderect(wall.rect) for wall in self.walls):
            self.survivor_status_message = "Move away from the wall before placing a turret."
            return

        self.trashy_turrets.append(turret)
        survivor.trashy_turret_cooldown = TRASHY_ABILITY_COOLDOWN
        self.survivor_status_message = "Devils Work turret placed."

    def use_kevin_punch(self, survivor: Survivor) -> None:
        if survivor.kevin_punch_cooldown > 0:
            self.survivor_status_message = (
                f"Punch cooldown {survivor.kevin_punch_cooldown:.1f}s."
            )
            return

        survivor.kevin_punch_used = True
        survivor.kevin_punch_timer = KEVIN_PUNCH_DURATION
        survivor.kevin_punch_cooldown = KEVIN_PUNCH_COOLDOWN
        self.survivor_status_message = "Punch active. Face the killer."

    def use_kevin_double_speed(self, survivor: Survivor) -> None:
        if survivor.kevin_speed_used:
            self.survivor_status_message = "Double speed already used."
            return

        survivor.kevin_speed_used = True
        survivor.kevin_speed_timer = KEVIN_DOUBLE_SPEED_DURATION
        self.survivor_status_message = "Double speed!"

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
        self.explorer_taming_timer = 0.0
        self.state = GameState.ROLE_REVEAL

    def survivor_index_from_key(self, key: int) -> str | None:
        number_keys = (
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
        )
        if key not in number_keys:
            return None

        index = number_keys.index(key)
        if index >= len(SURVIVOR_IDS):
            return None
        return SURVIVOR_IDS[index]

    def survivor_card_rect(self, index: int) -> pygame.Rect:
        card_width = 210
        card_height = 70
        card_gap = 18
        row_gap = 8
        columns = min(4, len(SURVIVOR_IDS))
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

    def survivor_from_card_click(self, pos: tuple[int, int]) -> str | None:
        for index, survivor_id in enumerate(SURVIVOR_IDS):
            if self.survivor_card_rect(index).collidepoint(pos):
                return survivor_id
        return None

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
        total_width = len(KILLER_IDS) * card_width + (len(KILLER_IDS) - 1) * card_gap
        start_x = (WIDTH - total_width) // 2
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
        self.survivor_shots = []
        self.trashy_shockwaves = []
        self.trashy_turrets = []
        self.trashy_turret_shots = []
        self.goopy_knights = []
        self.malice_bird_poops = []
        self.malice_helper_birds = []
        self.dinosaur_shockwave_timer = 0.0
        self.dinosaur_shockwave_pos = pygame.Vector2()
        self.survivor_slow_timer = 0.0
        self.survivor_flash_timer = 0.0
        self.explorer_taming_timer = 0.0
        self.show_runner_perimeter_next = 0
        self.show_runner_perimeter_laps = 0
        self.last_perimeter_edge = None
        self.spinning_perimeter_next = None
        self.spinning_perimeter_edges = 0
        self.last_spinning_perimeter_edge = None
        self.vengance_mines_placed_this_round = 0
        self.walls = self.create_walls()

        killer_sprite_key = self.sprite_key_for_round_killer()
        killer_sprite = self.sprites.get(killer_sprite_key) or self.sprites.get(self.round_killer)
        killer_walk_frames = self.walk_sprites.get(killer_sprite_key) or self.walk_sprites.get(self.round_killer, [])
        player_killer_skin = self.selected_skins.get(self.round_killer, "classic")

        if self.player_role == "Survivor":
            survivor_key = self.selected_player_survivor if self.selected_player_survivor in self.sprites else "survivor"
            survivor_sprite = self.sprites.get(survivor_key)
            survivor_walk_frames = self.walk_sprites.get(survivor_key, [])
            self.survivor = Survivor(
                "You",
                (500, 560),
                survivor_sprite,
                self.selected_player_survivor,
                survivor_walk_frames,
            )
            self.player = self.survivor
            self.killers = [
                Killer(
                    self.round_killer,
                    KILLERS[self.round_killer]["name"],
                    (820, 145),
                    killer_sprite,
                    "classic",
                    killer_walk_frames,
                )
            ]
        else:
            ai_survivor_id = random.choice(SURVIVOR_IDS)
            ai_survivor_key = ai_survivor_id if ai_survivor_id in self.sprites else "survivor"
            survivor_sprite = self.sprites.get(ai_survivor_key)
            survivor_walk_frames = self.walk_sprites.get(ai_survivor_key, [])
            self.player = Killer(
                self.round_killer,
                "You",
                (500, 555),
                killer_sprite,
                player_killer_skin if self.skin_unlocked(player_killer_skin) else "classic",
                killer_walk_frames,
            )
            self.survivor = Survivor(
                "AI Survivor",
                (500, 150),
                survivor_sprite,
                ai_survivor_id,
                survivor_walk_frames,
            )
            self.killers = [self.player]

        self.state = GameState.PLAYING
        self.start_round_music()

    def sprite_for_round_killer(self) -> pygame.Surface | None:
        return self.sprites.get(self.sprite_key_for_round_killer()) or self.sprites.get(self.round_killer)

    def sprite_key_for_round_killer(self) -> str:
        if self.player_role == "Killer":
            selected_skin = self.selected_skins.get(self.round_killer, "classic")
            if selected_skin != "classic" and self.skin_unlocked(selected_skin):
                return self.skin_sprite_key(self.round_killer, selected_skin)

        return self.round_killer

    def reset_to_title(self) -> None:
        self.state = GameState.TITLE
        self.player = None
        self.survivor = None
        self.killers = []
        self.active_hitboxes = []
        self.projectiles = []
        self.ducky_belts = []
        self.landmines = []
        self.survivor_shots = []
        self.trashy_shockwaves = []
        self.trashy_turrets = []
        self.trashy_turret_shots = []
        self.goopy_knights = []
        self.malice_bird_poops = []
        self.malice_helper_birds = []
        self.dinosaur_shockwave_timer = 0.0
        self.dinosaur_shockwave_pos = pygame.Vector2()
        self.round_time = ROUND_DURATION
        self.survivor_life_number = 1
        self.survivor_status_message = ""
        self.survivor_stun_timer = 0.0
        self.survivor_slow_timer = 0.0
        self.survivor_flash_timer = 0.0
        self.explorer_taming_timer = 0.0
        self.spinning_perimeter_next = None
        self.spinning_perimeter_edges = 0
        self.last_spinning_perimeter_edge = None
        self.stop_music()

    def update(self, dt: float) -> None:
        if self.state != GameState.PLAYING:
            return

        self.round_time = max(0.0, self.round_time - dt)

        keys = pygame.key.get_pressed()
        player_direction = vector_from_keys(keys)

        if isinstance(self.player, Killer):
            self.player.update_abilities(dt)
            self.update_malice_transform_animation(dt)
        elif isinstance(self.player, Survivor):
            self.player.update_abilities(dt)

        if self.survivor_stun_timer > 0:
            self.survivor_stun_timer = max(0.0, self.survivor_stun_timer - dt)
        if self.survivor_slow_timer > 0:
            self.survivor_slow_timer = max(0.0, self.survivor_slow_timer - dt)
        if self.survivor_flash_timer > 0:
            self.survivor_flash_timer = max(0.0, self.survivor_flash_timer - dt)
        if self.explorer_taming_timer > 0:
            self.explorer_taming_timer = max(0.0, self.explorer_taming_timer - dt)
        if self.dinosaur_shockwave_timer > 0:
            self.dinosaur_shockwave_timer = max(0.0, self.dinosaur_shockwave_timer - dt)

        if self.player is not None:
            player_walls = self.walls
            if (
                isinstance(self.player, Killer)
                and (self.player.is_wall_phasing() or self.player.is_malice_bird())
            ):
                player_walls = []

            player_speed = None
            if isinstance(self.player, Killer) and self.player.is_show_power_active():
                player_speed = self.player.speed * SHOW_RUNNER_SPEED_MULTIPLIER
            elif isinstance(self.player, Killer) and self.player.is_ducky_hg_active():
                player_speed = self.player.speed * DUCKY_HG_KILLER_SPEED_MULTIPLIER
            elif isinstance(self.player, Killer) and self.player.is_malice_tiger():
                player_speed = self.player.speed * MALICE_TIGER_SPEED_MULTIPLIER
            elif isinstance(self.player, Killer) and self.player.is_malice_dinosaur():
                player_speed = self.player.speed * MALICE_DINOSAUR_SPEED_MULTIPLIER
            elif isinstance(self.player, Killer) and self.player.is_vengance_dash_active():
                player_direction = self.player.vengance_dash_direction
                player_speed = VENGANCE_DASH_SPEED
            elif isinstance(self.player, Survivor):
                player_speed = self.player.current_speed()

            blocked = self.player.move(player_direction, dt, player_walls, ARENA_RECT, player_speed)
            if (
                blocked
                and isinstance(self.player, Killer)
                and self.player.is_vengance_dash_active()
            ):
                self.player.stop_vengance_dash()

            if (
                isinstance(self.player, Killer)
                and not self.player.is_wall_phasing()
                and not self.player.is_malice_bird()
            ):
                self.resolve_wall_overlap(self.player)

            self.update_movement_challenges()

        if self.player_role == "Survivor":
            self.update_survivor_mode(dt)
        else:
            self.update_killer_mode(dt)

    def update_malice_transform_animation(self, dt: float) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_malice():
            return

        if not self.player.is_hunter_rage_active():
            self.player.sprite = self.sprites.get("malice")
            self.player.sprite_alpha = 255
            self.malice_bird_poops = []
            self.malice_helper_birds = []
            return

        form = self.player.malice_form
        frames = self.animation_sprites.get(f"malice_{form}") if form is not None else None
        if frames:
            self.player.malice_animation_timer += dt
            if self.player.malice_animation_timer >= MALICE_FORM_ANIMATION_SPEED:
                self.player.malice_animation_timer = 0.0
                self.player.malice_animation_index = (
                    self.player.malice_animation_index + 1
                ) % len(frames)
            self.player.sprite = frames[self.player.malice_animation_index % len(frames)]
        else:
            self.player.sprite = self.sprites.get("malice")

        if self.player.is_malice_tiger() and self.player.tiger_invisible_timer > 0:
            self.player.sprite_alpha = 78
        else:
            self.player.sprite_alpha = 255

    def update_movement_challenges(self) -> None:
        self.update_spinning_perimeter_challenge()

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

    def update_spinning_perimeter_challenge(self) -> None:
        if self.player is None or self.skin_unlocked("vengance_spinning"):
            return

        edge = self.current_perimeter_edge(self.player.rect)
        if edge is None:
            self.last_spinning_perimeter_edge = None
            return
        if edge == self.last_spinning_perimeter_edge:
            return
        self.last_spinning_perimeter_edge = edge

        sequence = ("top", "right", "bottom", "left")
        edge_index = sequence.index(edge)
        if self.spinning_perimeter_next is None:
            self.spinning_perimeter_next = (edge_index + 1) % len(sequence)
            self.spinning_perimeter_edges = 1
            self.skin_notice = "Spinning perimeter lap: 1/4 edges"
            return

        if edge_index != self.spinning_perimeter_next:
            self.spinning_perimeter_next = (edge_index + 1) % len(sequence)
            self.spinning_perimeter_edges = 1
            return

        self.spinning_perimeter_edges += 1
        self.spinning_perimeter_next = (edge_index + 1) % len(sequence)
        self.skin_notice = f"Spinning perimeter lap: {self.spinning_perimeter_edges}/4 edges"
        if self.spinning_perimeter_edges >= 4:
            self.unlock_skin("vengance_spinning", "one perimeter lap completed")

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

    def use_malice_hunters_rage(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_malice():
            return
        if self.player_role != "Killer" or self.survivor is None:
            return

        form = self.player.start_hunter_rage()
        if form is None:
            return

        self.malice_bird_poops = []
        self.malice_helper_birds = []
        self.dinosaur_shockwave_timer = 0.0
        self.play_sound("malice_roar")
        self.update_malice_transform_animation(0.0)

        if form == "bird":
            self.spawn_malice_helper_birds(set_cooldown=True)

    def use_malice_tiger_invisibility(self) -> None:
        if not isinstance(self.player, Killer):
            return
        if self.player.start_tiger_invisibility():
            self.play_sound("attack")

    def spawn_malice_helper_birds(self, set_cooldown: bool) -> bool:
        if not isinstance(self.player, Killer) or not self.player.is_malice_bird():
            return False
        if len(self.malice_helper_birds) >= 2:
            return False

        offsets = [pygame.Vector2(-44, -18), pygame.Vector2(44, -18)]
        while len(self.malice_helper_birds) < 2:
            offset = offsets[len(self.malice_helper_birds)]
            self.malice_helper_birds.append(MaliceHelperBird(self.player.pos, offset))

        if set_cooldown:
            self.player.bird_summon_cooldown = MALICE_FORM_ABILITY_COOLDOWN
        return True

    def use_malice_bird_summon(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_malice_bird():
            return
        if self.player.bird_summon_cooldown > 0:
            return
        if self.spawn_malice_helper_birds(set_cooldown=True):
            self.play_sound("attack")

    def fire_malice_bird_poop(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_malice_bird():
            return
        if self.player.bird_poop_cooldown > 0:
            return

        direction = safe_normalize(self.player.facing)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, 1)

        self.malice_bird_poops.append(MaliceBirdPoop(self.player.pos + direction * 36, direction))
        self.player.bird_poop_cooldown = MALICE_FORM_ABILITY_COOLDOWN
        self.play_sound("attack")

    def use_malice_dinosaur_stomp(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_malice_dinosaur():
            return
        if self.player.dinosaur_stomp_cooldown > 0 or self.survivor is None:
            return

        self.player.dinosaur_stomp_cooldown = MALICE_FORM_ABILITY_COOLDOWN
        self.dinosaur_shockwave_timer = MALICE_DINOSAUR_SHOCKWAVE_VISUAL_DURATION
        self.dinosaur_shockwave_pos = pygame.Vector2(self.player.pos)
        self.play_sound("attack")

        if self.survivor.pos.distance_to(self.player.pos) <= MALICE_DINOSAUR_SHOCKWAVE_RADIUS:
            self.end_round(True, "Dinosaur stomp shockwave crushed the survivor.")

    def use_malice_dinosaur_roar(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_malice_dinosaur():
            return
        if self.player.dinosaur_roar_cooldown > 0 or self.survivor is None:
            return

        self.player.dinosaur_roar_cooldown = MALICE_FORM_ABILITY_COOLDOWN
        self.survivor_stun_timer = max(
            self.survivor_stun_timer,
            MALICE_DINOSAUR_ROAR_STUN_DURATION,
        )
        self.play_sound("dinosaur_roar")

    def fire_subslasher_spike(self, effect: str) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_subslasher():
            return
        if self.player_role != "Killer":
            return
        if effect == "freeze":
            if self.player.subslasher_freeze_cooldown > 0:
                return
            self.player.subslasher_freeze_cooldown = SUBSLASHER_FREEZE_SPIKE_COOLDOWN
        elif effect == "kill":
            if self.player.subslasher_kill_cooldown > 0:
                return
            self.player.subslasher_kill_cooldown = SUBSLASHER_KILL_SPIKE_COOLDOWN

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
        if self.player.subslasher_subzero_cooldown > 0:
            return

        self.player.subslasher_subzero_cooldown = SUBSLASHER_SUBZERO_COOLDOWN

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
        belt_only = self.selected_skins.get("revenge_bot") == "ducky_daddys_belt"
        self.ducky_belts.append(
            DuckyBelt(
                start_pos,
                direction,
                DUCKY_CRYING_SWING_SPEED,
                DUCKY_CRYING_SWING_LIFETIME,
                belt_only,
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
        if self.player.show_slow_cooldown > 0:
            return

        self.survivor_slow_timer = SHOW_RUNNER_SLOW_DURATION
        self.player.show_slow_cooldown = SHOW_RUNNER_SLOW_COOLDOWN

    def use_show_runner_hook(self) -> None:
        if not isinstance(self.player, Killer) or not self.player.is_show_runner():
            return
        if self.player_role != "Killer" or self.survivor is None:
            return
        if self.player.show_hook_cooldown > 0:
            return

        self.survivor.pos = self.survivor.pos.lerp(
            self.player.pos,
            SHOW_RUNNER_HOOK_PULL_RATIO,
        )
        self.survivor.update_rect()
        self.resolve_wall_overlap(self.survivor)
        self.player.show_hook_cooldown = SHOW_RUNNER_HOOK_COOLDOWN

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

    def update_malice_bird_poops(self, dt: float) -> None:
        if self.survivor is None:
            self.malice_bird_poops = []
            return

        remaining: list[MaliceBirdPoop] = []
        for poop in self.malice_bird_poops:
            if not poop.update(dt, self.walls):
                continue

            if poop.rect.colliderect(self.survivor.rect):
                self.survivor_stun_timer = max(
                    self.survivor_stun_timer,
                    MALICE_BIRD_POOP_STUN_DURATION,
                )
                continue

            remaining.append(poop)

        self.malice_bird_poops = remaining

    def update_malice_helper_birds(self, dt: float) -> None:
        if self.survivor is None:
            self.malice_helper_birds = []
            return

        remaining: list[MaliceHelperBird] = []
        for bird in self.malice_helper_birds:
            if not bird.update(dt):
                continue

            if bird.rect.colliderect(self.survivor.rect):
                self.survivor_slow_timer = max(
                    self.survivor_slow_timer,
                    MALICE_BIRD_HELPER_SLOW_DURATION,
                )
                continue

            remaining.append(bird)

        self.malice_helper_birds = remaining

    def update_ducky_belts(self, dt: float) -> None:
        if self.survivor is None:
            self.ducky_belts = []
            return

        remaining: list[DuckyBelt] = []
        for belt in self.ducky_belts:
            if not belt.update(dt, self.walls):
                continue

            if belt.rect.colliderect(self.survivor.rect):
                if self.round_killer == "revenge_bot" and self.player_role == "Killer":
                    self.unlock_skin("ducky_daddys_belt", "C swing hit the survivor")
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

    def stun_killer(self, killer: Killer, duration: float) -> None:
        killer.ai_stun_timer = max(killer.ai_stun_timer, duration)
        killer.attack_phase = None
        killer.attack_timer = 0.0

    def knockback_killer(self, killer: Killer, direction: pygame.Vector2, distance: float) -> None:
        direction = safe_normalize(direction)
        if direction.length_squared() == 0:
            direction = safe_normalize(killer.pos - self.survivor.pos) if self.survivor else pygame.Vector2(1, 0)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)

        steps = 8
        for _ in range(steps):
            killer.move(direction, 1.0, self.walls, ARENA_RECT, distance / steps)
        self.resolve_wall_overlap(killer)

    def update_survivor_shots(self, dt: float) -> None:
        remaining: list[SurvivorShot] = []
        for shot in self.survivor_shots:
            if not shot.update(dt, self.walls):
                continue
            hit_killer = next((killer for killer in self.killers if shot.rect.colliderect(killer.rect)), None)
            if hit_killer is not None:
                self.stun_killer(hit_killer, TRASHY_GUN_STUN_DURATION)
                self.survivor_status_message = "Gun shot stunned the killer."
                continue
            remaining.append(shot)
        self.survivor_shots = remaining

    def update_trashy_shockwaves(self, dt: float) -> None:
        remaining: list[TrashyShockWave] = []
        for shockwave in self.trashy_shockwaves:
            if not shockwave.update(dt, self.walls):
                continue

            hit_killer = next(
                (killer for killer in self.killers if shockwave.rect.colliderect(killer.rect)),
                None,
            )
            if hit_killer is not None:
                self.stun_killer(hit_killer, TRASHY_SHOCK_STUN_DURATION)
                self.knockback_killer(hit_killer, shockwave.direction, TRASHY_SHOCK_KNOCKBACK)
                self.round_time = max(0.0, self.round_time - TRASHY_SHOCK_TIMER_DROP)
                self.survivor_status_message = "Shock Wave hit! Killer stunned and timer dropped."
                continue

            remaining.append(shockwave)

        self.trashy_shockwaves = remaining

    def update_trashy_turrets(self, dt: float) -> None:
        remaining: list[TrashyTurret] = []
        for turret in self.trashy_turrets:
            shot = turret.update(dt, self.killers)
            if shot is not None:
                self.trashy_turret_shots.append(shot)
            if turret.alive():
                remaining.append(turret)
        self.trashy_turrets = remaining

        remaining_shots: list[TrashyTurretShot] = []
        for shot in self.trashy_turret_shots:
            if not shot.update(dt, self.walls):
                continue

            hit_killer = next(
                (killer for killer in self.killers if shot.rect.colliderect(killer.rect)),
                None,
            )
            if hit_killer is not None:
                self.stun_killer(hit_killer, TRASHY_TURRET_STUN_DURATION)
                self.survivor_status_message = "Devils Work turret stunned the killer."
                continue

            remaining_shots.append(shot)
        self.trashy_turret_shots = remaining_shots

    def update_goopy_knights(self, dt: float) -> None:
        remaining: list[GoopyKnight] = []
        for knight in self.goopy_knights:
            if not knight.update(dt, self.killers):
                continue
            hit_killer = next((killer for killer in self.killers if knight.rect.colliderect(killer.rect)), None)
            if hit_killer is not None:
                self.stun_killer(hit_killer, QUEEN_GOOPY_KNIGHT_STUN_DURATION)
                self.survivor_status_message = "A knight stunned the killer."
                continue
            remaining.append(knight)
        self.goopy_knights = remaining

    def update_kevin_punch(self) -> None:
        if not isinstance(self.player, Survivor) or self.player.survivor_id != "survivor_kevin":
            return
        if self.player.kevin_punch_timer <= 0:
            return

        hitbox = self.kevin_punch_hitbox(self.player)
        for killer in self.killers:
            if hitbox.colliderect(killer.rect):
                self.stun_killer(killer, KEVIN_PUNCH_STUN_DURATION)
                self.survivor_status_message = "Kevin punched the killer."

    def kevin_punch_hitbox(self, survivor: Survivor) -> pygame.Rect:
        facing = safe_normalize(survivor.facing)
        if facing.length_squared() == 0:
            facing = pygame.Vector2(0, -1)
        center = survivor.pos + facing * 42
        rect = pygame.Rect(0, 0, 46, 46)
        rect.center = (round(center.x), round(center.y))
        return rect

    def update_survivor_mode(self, dt: float) -> None:
        if self.survivor is None:
            return

        self.update_survivor_shots(dt)
        self.update_trashy_shockwaves(dt)
        self.update_trashy_turrets(dt)
        self.update_goopy_knights(dt)
        self.update_kevin_punch()

        self.active_hitboxes = []
        for killer in self.killers:
            self.update_ai_killer(killer, self.survivor, dt)
            hitbox = killer.current_hitbox()
            if hitbox is not None:
                self.active_hitboxes.append(hitbox)
                if hitbox.rect.colliderect(self.survivor.rect) and not self.survivor.is_invincible():
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
        self.update_malice_bird_poops(dt)
        if self.state != GameState.PLAYING:
            return
        self.update_malice_helper_birds(dt)
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
        if killer.ai_stun_timer > 0:
            killer.ai_stun_timer = max(0.0, killer.ai_stun_timer - dt)
            killer.attack_phase = None
            killer.attack_timer = 0.0
            return

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
                if self.explorer_taming_timer > 0:
                    ai_speed *= EXPLORER_TAMING_SPEED_MULTIPLIER
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

        visible_threats = [
            killer
            for killer in threats
            if not (killer.is_malice_tiger() and killer.tiger_invisible_timer > 0)
        ]
        if not visible_threats:
            return

        nearest = min(visible_threats, key=lambda killer: killer.pos.distance_to(survivor.pos))
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

        if self.player_role == "Killer" and self.round_killer == "revenge_bot":
            selected_ducky_skin = self.selected_skins.get("revenge_bot")
            if selected_ducky_skin == "ducky_daddys_belt":
                self.challenge_progress["ducky_daddys_belt_wins"] = max(
                    1,
                    self.challenge_progress.get("ducky_daddys_belt_wins", 0),
                )
            elif selected_ducky_skin == "ducky_ogel":
                self.challenge_progress["ducky_ogel_wins"] = max(
                    1,
                    self.challenge_progress.get("ducky_ogel_wins", 0),
                )

            if (
                self.challenge_progress.get("ducky_daddys_belt_wins", 0) >= 1
                and self.challenge_progress.get("ducky_ogel_wins", 0) >= 1
            ):
                self.unlock_skin("ducky_subject_5_png", "won with Daddy's Belt and Ogel")

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
            if self.vengance_mines_placed_this_round <= 3:
                low_mine_wins = self.challenge_progress.get("vengance_bot_low_mine_wins", 0) + 1
                self.challenge_progress["vengance_bot_low_mine_wins"] = low_mine_wins
                if low_mine_wins >= 2:
                    self.unlock_skin("vengance_werewolf", "2 wins with 3 or fewer landmines")

            if self.vengance_mines_placed_this_round == 0:
                self.unlock_skin("vengance_scoreboard", "won without landmines")

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
        else:
            self.draw_survivor_selection()
        self.menu_buttons["begin"].draw(self.screen, self.font_medium, True)

    def draw_survivor_selection(self) -> None:
        draw_text(
            self.screen,
            self.font_medium,
            "Choose Survivor",
            (248, 250, 252),
            (WIDTH // 2, 420),
            True,
        )

        for index, survivor_id in enumerate(SURVIVOR_IDS):
            data = SURVIVORS[survivor_id]
            rect = self.survivor_card_rect(index)
            selected = survivor_id == self.selected_player_survivor
            fill = (24, 41, 58)
            outline = (96, 165, 250) if selected else (88, 100, 116)
            pygame.draw.rect(self.screen, fill, rect, border_radius=8)
            pygame.draw.rect(self.screen, outline, rect, 3 if selected else 2, border_radius=8)

            sprite = self.sprites.get(survivor_id)
            preview_rect = pygame.Rect(rect.left + 8, rect.top + 13, 44, 44)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, (96, 165, 250), preview_rect)

            draw_text(
                self.screen,
                self.font_small,
                f"{index + 1}. {data['name']}",
                (248, 250, 252),
                (rect.left + 60, rect.top + 9),
            )
            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["description"],
                (203, 213, 225),
                pygame.Rect(rect.left + 60, rect.top + 32, rect.width - 68, 30),
            )

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
                pygame.Rect(WIDTH // 2 - 350, 582, 700, 36),
            )

    def skin_challenge_text(self, skin_id: str) -> str:
        if skin_id == "fried_chicken":
            remaining = max(0, FRIED_CHICKEN_UNLOCK_WINS - self.total_wins)
            return f"win {remaining} more"
        if skin_id in ("ducky_inverted", "ducky_ogel"):
            target = DUCKY_INVERTED_LOSSES if skin_id == "ducky_inverted" else DUCKY_OGEL_LOSSES
            losses = self.challenge_progress.get("ducky_losses", 0)
            return f"Ducky losses {losses}/{target}"
        if skin_id == "ducky_daddys_belt":
            return "C swing survivor kill"
        if skin_id == "ducky_subject_5_png":
            belt_win = self.challenge_progress.get("ducky_daddys_belt_wins", 0)
            ogel_win = self.challenge_progress.get("ducky_ogel_wins", 0)
            return f"Belt win {belt_win}/1, Ogel win {ogel_win}/1"
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
        if skin_id == "vengance_spinning":
            return "one perimeter lap"
        if skin_id == "vengance_werewolf":
            wins = self.challenge_progress.get("vengance_bot_low_mine_wins", 0)
            return f"low-mine wins {wins}/2"
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
        if skin_id == "ducky_daddys_belt":
            return "Play as Ducky and kill the survivor with the C swing ability."
        if skin_id == "ducky_subject_5_png":
            belt_done = self.challenge_progress.get("ducky_daddys_belt_wins", 0) >= 1
            ogel_done = self.challenge_progress.get("ducky_ogel_wins", 0) >= 1
            missing = []
            if not belt_done:
                missing.append("win a round using Daddy's Belt")
            if not ogel_done:
                missing.append("win a round using Ogel")
            return "Unlock by completing: " + " and ".join(missing) + "."
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
        if skin_id == "vengance_scoreboard":
            return "Play as Vengance Bot and win the round without placing any landmines."
        if skin_id == "vengance_spinning":
            return "Run clockwise around all 4 arena edges once with any player character."
        if skin_id == "vengance_werewolf":
            wins = self.challenge_progress.get("vengance_bot_low_mine_wins", 0)
            remaining = max(0, 2 - wins)
            return f"Win {remaining} more Vengance Bot round{'s' if remaining != 1 else ''} while placing 3 or fewer landmines."
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

        for poop in self.malice_bird_poops:
            poop.draw(self.screen)

        for belt in self.ducky_belts:
            belt.draw(self.screen)

        for mine in self.landmines:
            mine.draw(self.screen)

        self.draw_survivor_ability_effects()

        for shot in self.survivor_shots:
            shot.draw(self.screen)

        for shockwave in self.trashy_shockwaves:
            shockwave.draw(self.screen)

        for turret in self.trashy_turrets:
            turret.draw(self.screen)

        for turret_shot in self.trashy_turret_shots:
            turret_shot.draw(self.screen)

        for knight in self.goopy_knights:
            knight.draw(self.screen)

        for bird in self.malice_helper_birds:
            bird.draw(self.screen)

        self.draw_dinosaur_shockwave()

        if self.survivor is not None:
            self.survivor.draw(self.screen, self.font_small)

        for killer in self.killers:
            if killer is not self.survivor:
                killer.draw(self.screen, self.font_small)

        self.draw_hud()
        self.draw_side_panel()
        self.draw_survivor_ability_ui()

    def draw_survivor_ability_effects(self) -> None:
        if not isinstance(self.player, Survivor):
            return

        survivor = self.player
        if survivor.kitty_marker is not None:
            pygame.draw.circle(
                self.screen,
                (59, 130, 246),
                (round(survivor.kitty_marker.x), round(survivor.kitty_marker.y)),
                KITTY_TELEPORT_MARKER_RADIUS,
                4,
            )
            pygame.draw.circle(
                self.screen,
                (191, 219, 254),
                (round(survivor.kitty_marker.x), round(survivor.kitty_marker.y)),
                8,
            )

        if self.survivor_flash_timer > 0:
            alpha = int(190 * (self.survivor_flash_timer / ODD_FLASH_VISUAL_DURATION))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(
                overlay,
                (255, 255, 210, alpha),
                survivor.rect.center,
                220,
            )
            self.screen.blit(overlay, (0, 0))

        if survivor.explorer_adrenaline_timer > 0:
            pygame.draw.circle(self.screen, (34, 197, 94), survivor.rect.center, 39, 3)

        if self.explorer_taming_timer > 0:
            for killer in self.killers:
                pygame.draw.circle(self.screen, (45, 212, 191), killer.rect.center, 43, 3)

        if survivor.kevin_speed_timer > 0:
            angle = (pygame.time.get_ticks() * 0.6) % 360
            for offset in (0, 120, 240):
                direction = pygame.Vector2(1, 0).rotate(angle + offset)
                pygame.draw.line(
                    self.screen,
                    (96, 165, 250),
                    pygame.Vector2(survivor.rect.center) + direction * 24,
                    pygame.Vector2(survivor.rect.center) + direction * 38,
                    3,
                )

        if survivor.kevin_punch_timer > 0:
            hitbox = self.kevin_punch_hitbox(survivor)
            pygame.draw.rect(self.screen, (250, 204, 21), hitbox, 3, border_radius=8)

    def draw_survivor_ability_ui(self) -> None:
        if not isinstance(self.player, Survivor) or not self.player.trashy_minigame_active:
            return

        survivor = self.player
        pygame.draw.rect(self.screen, (127, 29, 29), TRASHY_MINIGAME_BAR, border_radius=10)
        pygame.draw.rect(self.screen, (254, 202, 202), TRASHY_MINIGAME_BAR, 2, border_radius=10)
        target = survivor.trashy_target_rect()
        circle = survivor.trashy_circle_rect()
        pygame.draw.rect(self.screen, (34, 197, 94), target, border_radius=4)
        pygame.draw.circle(self.screen, (248, 250, 252), circle.center, TRASHY_MINIGAME_CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, (15, 23, 42), circle.center, TRASHY_MINIGAME_CIRCLE_RADIUS, 2)
        draw_text(
            self.screen,
            self.font_small,
            f"Gun Maker {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}",
            (248, 250, 252),
            (TRASHY_MINIGAME_BAR.centerx, TRASHY_MINIGAME_BAR.top - 20),
            True,
        )

    def draw_dinosaur_shockwave(self) -> None:
        if self.dinosaur_shockwave_timer <= 0:
            return

        elapsed_ratio = 1.0 - (
            self.dinosaur_shockwave_timer / MALICE_DINOSAUR_SHOCKWAVE_VISUAL_DURATION
        )
        radius = int(34 + MALICE_DINOSAUR_SHOCKWAVE_RADIUS * elapsed_ratio)
        alpha = int(190 * (self.dinosaur_shockwave_timer / MALICE_DINOSAUR_SHOCKWAVE_VISUAL_DURATION))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        center = (round(self.dinosaur_shockwave_pos.x), round(self.dinosaur_shockwave_pos.y))
        pygame.draw.circle(overlay, (248, 250, 252, alpha), center, radius, 5)
        pygame.draw.circle(overlay, (59, 130, 246, max(50, alpha // 2)), center, radius // 2, 2)
        self.screen.blit(overlay, (0, 0))

    def draw_panel_shell(self, rect: pygame.Rect, title: str) -> None:
        pygame.draw.rect(self.screen, (12, 19, 32), rect, border_radius=PANEL_RADIUS)
        pygame.draw.rect(self.screen, (51, 65, 85), rect, 2, border_radius=PANEL_RADIUS)
        draw_text(self.screen, self.font_small, title, (248, 250, 252), (rect.left + 16, rect.top + 12))
        pygame.draw.line(
            self.screen,
            (51, 65, 85),
            (rect.left + 14, rect.top + 37),
            (rect.right - 14, rect.top + 37),
            1,
        )

    def draw_side_panel(self) -> None:
        pygame.draw.rect(self.screen, (8, 13, 24), SIDE_PANEL_RECT, border_radius=10)
        self.draw_timer_panel()
        self.draw_status_panel()
        self.draw_ability_guide_panel()
        self.draw_combat_panel()

    def draw_timer_panel(self) -> None:
        self.draw_panel_shell(TIMER_PANEL_RECT, "Time")
        draw_text(
            self.screen,
            self.font_large,
            f"{math.ceil(self.round_time):02d}",
            (248, 250, 252),
            (TIMER_PANEL_RECT.centerx, TIMER_PANEL_RECT.top + 73),
            True,
        )
        draw_text(
            self.screen,
            self.font_small,
            "seconds left",
            (148, 163, 184),
            (TIMER_PANEL_RECT.centerx, TIMER_PANEL_RECT.bottom - 24),
            True,
        )

    def gameplay_status_text(self) -> tuple[str, str]:
        if self.player_role == "Survivor":
            status = "Survive!"
            survivor_ability = self.survivor_ability_status()
            detail = (
                f"{self.survivor_status_message} | {survivor_ability}"
                if self.survivor_status_message
                else survivor_ability
            )
            return status, detail

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
        return status, detail

    def draw_status_panel(self) -> None:
        self.draw_panel_shell(STATUS_PANEL_RECT, "Round Status")
        status, detail = self.gameplay_status_text()
        draw_text(
            self.screen,
            self.font_small,
            status,
            (248, 199, 88),
            (STATUS_PANEL_RECT.left + 16, STATUS_PANEL_RECT.top + 47),
        )
        draw_wrapped_text_left(
            self.screen,
            self.font_small,
            detail,
            (203, 213, 225),
            pygame.Rect(
                STATUS_PANEL_RECT.left + 16,
                STATUS_PANEL_RECT.top + 73,
                STATUS_PANEL_RECT.width - 32,
                STATUS_PANEL_RECT.bottom - STATUS_PANEL_RECT.top - 86,
            ),
            2,
        )

    def draw_combat_panel(self) -> None:
        self.draw_panel_shell(COMBAT_PANEL_RECT, "Action")
        if isinstance(self.player, Killer):
            draw_text(
                self.screen,
                self.font_small,
                self.player.cooldown_status(),
                (226, 232, 240),
                (COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 47),
            )
            bar = pygame.Rect(
                COMBAT_PANEL_RECT.left + 16,
                COMBAT_PANEL_RECT.top + 78,
                COMBAT_PANEL_RECT.width - 32,
                16,
            )
            self.draw_cooldown_bar(self.player, bar)
            draw_text(
                self.screen,
                self.font_small,
                "Space: basic attack",
                (148, 163, 184),
                (COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 98),
            )
            return

        draw_wrapped_text_left(
            self.screen,
            self.font_small,
            self.survivor_ability_status(),
            (226, 232, 240),
            pygame.Rect(
                COMBAT_PANEL_RECT.left + 16,
                COMBAT_PANEL_RECT.top + 47,
                COMBAT_PANEL_RECT.width - 32,
                COMBAT_PANEL_RECT.height - 60,
            ),
            3,
        )

    def draw_ability_guide_panel(self) -> None:
        lines = self.ability_guide_lines()
        self.draw_panel_shell(ABILITY_PANEL_RECT, "Ability Guide")

        if not lines:
            draw_text(
                self.screen,
                self.font_small,
                "No abilities yet.",
                (148, 163, 184),
                (ABILITY_PANEL_RECT.left + 16, ABILITY_PANEL_RECT.top + 46),
            )
            return

        y = ABILITY_PANEL_RECT.top + 45
        content_rect = pygame.Rect(
            ABILITY_PANEL_RECT.left + 16,
            y,
            ABILITY_PANEL_RECT.width - 32,
            ABILITY_PANEL_RECT.bottom - y - 14,
        )
        for line in lines:
            y = draw_wrapped_text_left(
                self.screen,
                self.font_small,
                f"- {line}",
                (203, 213, 225),
                pygame.Rect(content_rect.left, y, content_rect.width, content_rect.bottom - y),
                2,
            )
            y += 7
            if y + self.font_small.get_height() > content_rect.bottom:
                break

    def ability_guide_lines(self) -> list[str]:
        if isinstance(self.player, Survivor):
            if self.player.survivor_id == "survivor_odd":
                return ["Move: WASD or arrows", "F: Picture Taken flash stuns killer 5s"]
            if self.player.survivor_id == "survivor_explorer":
                return ["Move: WASD or arrows", "A: Adrenaline invincible +60% speed", "A also Taming: killer 50% slower"]
            if self.player.survivor_id == "survivor_kitty":
                return ["Move: WASD or arrows", "L: place blue circle", "2: teleport to blue circle once"]
            if self.player.survivor_id == "survivor_queen_goopy":
                return ["Move: WASD or arrows", "K: summon 2 knights", "Knights stun killer 2.3s on touch"]
            if self.player.survivor_id == "survivor_trashy":
                return ["G: Gun Maker timing game / fire gun", "C: Shock Wave Cannon stuns and knocks back", "T: Devils Work turret, max 2", "Trashy abilities have 5s cooldowns"]
            if self.player.survivor_id == "survivor_kevin":
                return ["Move: WASD or arrows", "P: Punch in front for 5s", "S: Double Speed, +89% speed"]
            return ["Move: WASD or arrows", "Survive both lives until timer ends"]

        if not isinstance(self.player, Killer):
            return []

        if self.player.is_ducky():
            return ["Space: Lunge Swing attack", "C: Crying Swing belt/mace projectile", "Y: HG, Ducky faster and survivor slower"]
        if self.player.is_subslasher():
            return ["Space: Popsicle Sword Swing", "I: Perpelling Shootdown freeze spike", "E: Freezing Gun kill spike", "Q: Perpelling Subzero homing cubes"]
        if self.player.is_show_runner():
            return ["Space: Curtain Slash", "9: hahaha, slow survivor 50%", "U: script hook pulls survivor halfway", "A: shows power, +69% speed"]
        if self.player.is_vengance_bot():
            return ["Space: Vengance Lunge", "R: robot slash dash for 5s", "C: explosion landmine then teleport"]
        if self.player.is_malice_tiger():
            return ["Tiger form: +69% speed for Hunter's Rage", "Space: slash attack", "I: invisible 5s; survivor cannot see you", "Invisibility cooldown: 5s after visible"]
        if self.player.is_malice_bird():
            return ["Bird form: flies through walls", "I: summon 2 helper birds", "A: shoot white poop stun projectile", "Helpers slow survivor 50% on touch"]
        if self.player.is_malice_dinosaur():
            return ["Dinosaur form: 10% slower", "S: stomp shockwave; survivor dies in range", "R: dinosaur roar freezes survivor 16s", "Stomp and roar cooldown: 5s"]
        if self.player.is_malice():
            return ["Space: Malice Bite", "H: Hunter's Rage, random 20s form", "I: In Search For Bodies, pass through walls 4s"]

        return ["Space: attack", "Catch the survivor before time ends"]

    def draw_arena_preview(self) -> None:
        preview = pygame.Rect(0, 0, 760, 230)
        preview.center = (WIDTH // 2, 475)
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
        pygame.draw.rect(self.screen, (5, 10, 20), pygame.Rect(0, 0, WIDTH, TOP_BAR_HEIGHT))
        pygame.draw.line(self.screen, (51, 65, 85), (0, TOP_BAR_HEIGHT), (WIDTH, TOP_BAR_HEIGHT), 2)

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
            self.font_small,
            "WASD / Arrows move  |  Escape quits",
            (148, 163, 184),
            (WIDTH - 420, 50),
        )

    def hud_role_text(self, killer_name: str) -> str:
        text = f"Role: {self.player_role}  |  Round killer: {killer_name}"
        if self.player_role == "Survivor":
            text += f"  |  Life: {self.survivor_life_number}/{SURVIVOR_TOTAL_LIVES}"
        return text

    def survivor_ability_status(self) -> str:
        if not isinstance(self.player, Survivor):
            return "WASD / Arrows move"

        survivor = self.player
        if survivor.survivor_id == "survivor_odd":
            if survivor.odd_flash_cooldown > 0:
                return f"F cooldown {survivor.odd_flash_cooldown:.1f}s"
            return "F Picture Taken"
        if survivor.survivor_id == "survivor_explorer":
            if survivor.explorer_adrenaline_timer > 0 or self.explorer_taming_timer > 0:
                return f"A ability {max(survivor.explorer_adrenaline_timer, self.explorer_taming_timer):.1f}s"
            if survivor.explorer_ability_cooldown > 0:
                return f"A cooldown {survivor.explorer_ability_cooldown:.1f}s"
            return "A Adrenaline + Taming"
        if survivor.survivor_id == "survivor_kitty":
            if survivor.kitty_marker is not None:
                return "2 teleport to blue circle"
            return "L place blue circle" if not survivor.kitty_teleport_used else "Teleport used"
        if survivor.survivor_id == "survivor_queen_goopy":
            if survivor.queen_knights_cooldown > 0:
                return f"K cooldown {survivor.queen_knights_cooldown:.1f}s"
            return "K Knights"
        if survivor.survivor_id == "survivor_trashy":
            if survivor.trashy_minigame_active:
                return f"Click overlap {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}"
            if survivor.trashy_gun_ready:
                gun = "G fire gun"
            else:
                gun = "G Gun Maker" if not survivor.trashy_gun_used else "Gun used"
            shock = (
                f"C cooldown {survivor.trashy_shock_cooldown:.1f}s"
                if survivor.trashy_shock_cooldown > 0
                else "C cannon"
            )
            turret = (
                f"T cooldown {survivor.trashy_turret_cooldown:.1f}s"
                if survivor.trashy_turret_cooldown > 0
                else f"T turret {len(self.trashy_turrets)}/{TRASHY_MAX_TURRETS}"
            )
            return f"{gun} | {shock} | {turret}"
        if survivor.survivor_id == "survivor_kevin":
            punch = "P punch"
            speed = "S speed" if not survivor.kevin_speed_used else "Speed used"
            if survivor.kevin_punch_timer > 0:
                punch = f"Punch {survivor.kevin_punch_timer:.1f}s"
            elif survivor.kevin_punch_cooldown > 0:
                punch = f"P cooldown {survivor.kevin_punch_cooldown:.1f}s"
            if survivor.kevin_speed_timer > 0:
                speed = f"Speed {survivor.kevin_speed_timer:.1f}s"
            return f"{punch} | {speed}"
        return "WASD / Arrows move"

    def malice_ability_status(self, malice: Killer) -> str:
        if malice.is_malice_tiger():
            invis = "I invisible"
            if malice.tiger_invisible_timer > 0:
                invis = f"Invisible {malice.tiger_invisible_timer:.1f}s"
            elif malice.tiger_invisible_cooldown > 0:
                invis = f"I cooldown {malice.tiger_invisible_cooldown:.1f}s"
            return f"Tiger {malice.malice_form_timer:.1f}s | {invis}"

        if malice.is_malice_bird():
            summon = "I helpers"
            poop = "A poop"
            if malice.bird_summon_cooldown > 0:
                summon = f"I cooldown {malice.bird_summon_cooldown:.1f}s"
            if malice.bird_poop_cooldown > 0:
                poop = f"A cooldown {malice.bird_poop_cooldown:.1f}s"
            return f"Bird {malice.malice_form_timer:.1f}s | {summon} | {poop}"

        if malice.is_malice_dinosaur():
            stomp = "S stomp"
            roar = "R roar"
            if malice.dinosaur_stomp_cooldown > 0:
                stomp = f"S cooldown {malice.dinosaur_stomp_cooldown:.1f}s"
            if malice.dinosaur_roar_cooldown > 0:
                roar = f"R cooldown {malice.dinosaur_roar_cooldown:.1f}s"
            return f"Dino {malice.malice_form_timer:.1f}s | {stomp} | {roar}"

        rage = "H: Hunter's Rage"
        if malice.malice_hunter_cooldown > 0:
            rage = f"H cooldown {malice.malice_hunter_cooldown:.1f}s"
        return f"{malice.wall_phase_status()} | {rage}"

    def subslasher_ability_status(self) -> str:
        if not isinstance(self.player, Killer):
            return "I freeze | E kill | Q cubes"

        freeze = "I freeze"
        kill = "E kill"
        cubes = "Q cubes"
        if self.survivor_stun_timer > 0:
            freeze = f"Frozen {self.survivor_stun_timer:.1f}s"
        elif self.player.subslasher_freeze_cooldown > 0:
            freeze = f"I cooldown {self.player.subslasher_freeze_cooldown:.1f}s"
        if self.player.subslasher_kill_cooldown > 0:
            kill = f"E cooldown {self.player.subslasher_kill_cooldown:.1f}s"
        if self.player.subslasher_subzero_cooldown > 0:
            cubes = f"Q cooldown {self.player.subslasher_subzero_cooldown:.1f}s"
        return f"{freeze} | {kill} | {cubes}"

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
        hook = "U hook"
        speed = "A speed"
        if self.survivor_slow_timer > 0:
            slow = f"Slow {self.survivor_slow_timer:.1f}s"
        elif show_runner.show_slow_cooldown > 0:
            slow = f"9 cooldown {show_runner.show_slow_cooldown:.1f}s"
        if show_runner.show_hook_cooldown > 0:
            hook = f"U cooldown {show_runner.show_hook_cooldown:.1f}s"
        if show_runner.show_power_timer > 0:
            speed = f"Speed {show_runner.show_power_timer:.1f}s"
        elif show_runner.show_power_cooldown > 0:
            speed = f"A cooldown {show_runner.show_power_cooldown:.1f}s"
        return f"{slow} | {hook} | {speed}"

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

    def draw_cooldown_bar(self, killer: Killer, bar: pygame.Rect | None = None) -> None:
        if bar is None:
            bar = pygame.Rect(COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 78, 150, 16)
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

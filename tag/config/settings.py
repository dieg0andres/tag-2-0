from __future__ import annotations

from pathlib import Path

import pygame


WIDTH = 1280
HEIGHT = 800
MIN_WIDTH = 980
MIN_HEIGHT = 640
FPS = 60
ROUND_DURATION = 60.0
SURVIVOR_TOTAL_LIVES = 2

ROOT_DIR = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT_DIR / "assets"
SPRITE_DIR = ASSET_DIR / "sprites"
ANIMATION_DIR = SPRITE_DIR / "animations"
SAVE_FILE = ROOT_DIR / "save_data.json"

UI_MARGIN = 24
TOP_BAR_HEIGHT = 88
SIDE_PANEL_WIDTH = 330
PANEL_GAP = 18
PANEL_RADIUS = 14
WINDOW_FLAGS = pygame.RESIZABLE

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


def _clamp_int(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _set_rect(rect: pygame.Rect, x: int, y: int, width: int, height: int) -> None:
    rect.update(round(x), round(y), max(1, round(width)), max(1, round(height)))


def resize_layout(width: int, height: int) -> tuple[int, int]:
    """Recompute the game's responsive screen regions.

    The major layout objects are mutated in place so every module that imports
    ARENA_RECT, SIDE_PANEL_RECT, or the panel rects sees the new dimensions.
    """
    global WIDTH, HEIGHT, UI_MARGIN, SIDE_PANEL_WIDTH

    WIDTH = max(MIN_WIDTH, int(width))
    HEIGHT = max(MIN_HEIGHT, int(height))

    UI_MARGIN = _clamp_int(int(WIDTH * 0.018), 16, 28)
    gap = _clamp_int(int(WIDTH * 0.014), 12, 22)
    panel_gap = _clamp_int(int(HEIGHT * 0.018), 10, 16)

    wide_layout = WIDTH >= 1080
    if wide_layout:
        SIDE_PANEL_WIDTH = _clamp_int(int(WIDTH * 0.26), 305, 390)
        arena_width = WIDTH - SIDE_PANEL_WIDTH - gap - UI_MARGIN * 2
        arena_height = HEIGHT - TOP_BAR_HEIGHT - UI_MARGIN * 2
        _set_rect(ARENA_RECT, UI_MARGIN, TOP_BAR_HEIGHT + UI_MARGIN, arena_width, arena_height)
        _set_rect(SIDE_PANEL_RECT, ARENA_RECT.right + gap, ARENA_RECT.top, SIDE_PANEL_WIDTH, ARENA_RECT.height)

        timer_h = _clamp_int(int(SIDE_PANEL_RECT.height * 0.18), 104, 132)
        status_h = _clamp_int(int(SIDE_PANEL_RECT.height * 0.17), 96, 124)
        ability_h = _clamp_int(int(SIDE_PANEL_RECT.height * 0.40), 190, 300)
        combat_h = SIDE_PANEL_RECT.height - timer_h - status_h - ability_h - panel_gap * 3
        if combat_h < 100:
            missing = 100 - combat_h
            ability_h = max(170, ability_h - missing)
            combat_h = SIDE_PANEL_RECT.height - timer_h - status_h - ability_h - panel_gap * 3

        x = SIDE_PANEL_RECT.left
        y = SIDE_PANEL_RECT.top
        w = SIDE_PANEL_RECT.width
        _set_rect(TIMER_PANEL_RECT, x, y, w, timer_h)
        _set_rect(STATUS_PANEL_RECT, x, TIMER_PANEL_RECT.bottom + panel_gap, w, status_h)
        _set_rect(ABILITY_PANEL_RECT, x, STATUS_PANEL_RECT.bottom + panel_gap, w, ability_h)
        _set_rect(COMBAT_PANEL_RECT, x, ABILITY_PANEL_RECT.bottom + panel_gap, w, max(90, combat_h))
    else:
        bottom_h = _clamp_int(int(HEIGHT * 0.34), 210, 280)
        arena_width = WIDTH - UI_MARGIN * 2
        arena_height = HEIGHT - TOP_BAR_HEIGHT - bottom_h - UI_MARGIN * 2
        _set_rect(ARENA_RECT, UI_MARGIN, TOP_BAR_HEIGHT + UI_MARGIN, arena_width, max(280, arena_height))
        _set_rect(SIDE_PANEL_RECT, UI_MARGIN, ARENA_RECT.bottom + gap, arena_width, HEIGHT - ARENA_RECT.bottom - UI_MARGIN - gap)

        timer_w = _clamp_int(int(SIDE_PANEL_RECT.width * 0.16), 132, 170)
        status_w = _clamp_int(int(SIDE_PANEL_RECT.width * 0.22), 190, 245)
        combat_w = _clamp_int(int(SIDE_PANEL_RECT.width * 0.22), 190, 245)
        ability_w = SIDE_PANEL_RECT.width - timer_w - status_w - combat_w - panel_gap * 3
        if ability_w < 250:
            shortage = 250 - ability_w
            status_w = max(170, status_w - shortage // 2)
            combat_w = max(170, combat_w - (shortage - shortage // 2))
            ability_w = SIDE_PANEL_RECT.width - timer_w - status_w - combat_w - panel_gap * 3

        x = SIDE_PANEL_RECT.left
        y = SIDE_PANEL_RECT.top
        h = SIDE_PANEL_RECT.height
        _set_rect(TIMER_PANEL_RECT, x, y, timer_w, h)
        _set_rect(STATUS_PANEL_RECT, TIMER_PANEL_RECT.right + panel_gap, y, status_w, h)
        _set_rect(ABILITY_PANEL_RECT, STATUS_PANEL_RECT.right + panel_gap, y, max(230, ability_w), h)
        _set_rect(COMBAT_PANEL_RECT, ABILITY_PANEL_RECT.right + panel_gap, y, combat_w, h)

    bar_width = max(220, ARENA_RECT.width - 340)
    _set_rect(
        TRASHY_MINIGAME_BAR,
        ARENA_RECT.centerx - bar_width // 2,
        ARENA_RECT.bottom - 42,
        min(bar_width, ARENA_RECT.width - 40),
        28,
    )
    return WIDTH, HEIGHT


resize_layout(WIDTH, HEIGHT)

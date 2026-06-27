from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import pygame

from tag.config.settings import *
from tag.core.state import GameState
from tag.data.content import *
from tag.entities.objects import *
from tag.utils.text import draw_text, draw_wrapped_text, draw_wrapped_text_left
from tag.utils.vector import facing_axis, safe_normalize, vector_from_keys


class SurvivorAbilitiesMixin:
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


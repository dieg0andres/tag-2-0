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


class AIMixin:
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


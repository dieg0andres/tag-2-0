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


class KillerAbilitiesMixin:
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


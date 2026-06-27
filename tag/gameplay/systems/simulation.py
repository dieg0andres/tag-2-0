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


class SimulationMixin:
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


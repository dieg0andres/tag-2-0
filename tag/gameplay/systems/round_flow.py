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


class RoundFlowMixin:
    def reveal_role(self) -> None:
        self.player_role = random.choice(["Survivor", "Killer"])
        if self.player_role == "Killer":
            self.round_killer = self.selected_player_killer
        else:
            self.round_killer = random.choice(KILLER_IDS)
        self.skin_notice = ""
        self.survivor_life_number = 1
        self.survivor_status_message = ""
        self.survivor_stun_timer = 0.0
        self.survivor_slow_timer = 0.0
        self.explorer_taming_timer = 0.0
        self.state = GameState.ROLE_REVEAL

    def unlocked_skin_options_for_killer(self, killer_id: str) -> list[str]:
        return [
            skin_id
            for skin_id in self.skin_options_for_killer(killer_id)
            if skin_id == "classic" or self.skin_unlocked(skin_id)
        ]

    def selected_killer_has_skin_choices(self) -> bool:
        return len(self.unlocked_skin_options_for_killer(self.selected_player_killer)) > 1

    def set_selected_killer_for_role_reveal(self, killer_id: str) -> None:
        self.selected_player_killer = killer_id
        self.round_killer = killer_id
        self.skin_notice = ""
        if self.selected_skins.get(killer_id, "classic") not in self.unlocked_skin_options_for_killer(killer_id):
            self.selected_skins[killer_id] = "classic"

    def cycle_selected_killer(self, direction: int) -> None:
        current_index = KILLER_IDS.index(self.selected_player_killer)
        next_index = (current_index + direction) % len(KILLER_IDS)
        self.set_selected_killer_for_role_reveal(KILLER_IDS[next_index])

    def continue_from_role_reveal(self) -> None:
        if self.player_role == "Survivor":
            self.begin_round()
            return

        self.round_killer = self.selected_player_killer
        if self.selected_killer_has_skin_choices():
            self.state = GameState.KILLER_SKIN_SELECT
            return

        self.selected_skins[self.round_killer] = "classic"
        self.begin_round()

    def begin_round_from_skin_select(self) -> None:
        self.round_killer = self.selected_player_killer
        selected_skin = self.selected_skins.get(self.round_killer, "classic")
        if selected_skin not in self.unlocked_skin_options_for_killer(self.round_killer):
            self.selected_skins[self.round_killer] = "classic"
        self.begin_round()

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
        self.select_random_wall_layout()
        self.walls = self.create_walls()

        killer_sprite_key = self.sprite_key_for_round_killer()
        killer_sprite = self.sprites.get(killer_sprite_key) or self.sprites.get(self.round_killer)
        killer_walk_frames = self.walk_sprites.get(killer_sprite_key) or self.walk_sprites.get(self.round_killer, [])
        player_killer_skin = self.selected_skins.get(self.round_killer, "classic")

        if self.player_role == "Survivor":
            survivor_key = self.selected_player_survivor if self.selected_player_survivor in self.sprites else "survivor"
            survivor_sprite = self.sprites.get(survivor_key)
            survivor_walk_frames = self.walk_sprites.get(survivor_key, [])
            survivor_spawn = self.spawn_position(0.54, 0.68)
            killer_spawn = self.spawn_position(0.90, 0.08, survivor_spawn)
            self.survivor = Survivor(
                "You",
                survivor_spawn,
                survivor_sprite,
                self.selected_player_survivor,
                survivor_walk_frames,
            )
            self.player = self.survivor
            self.killers = [
                Killer(
                    self.round_killer,
                    KILLERS[self.round_killer]["name"],
                    killer_spawn,
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
            killer_spawn = self.spawn_position(0.54, 0.68)
            survivor_spawn = self.spawn_position(0.54, 0.08, killer_spawn)
            self.player = Killer(
                self.round_killer,
                "You",
                killer_spawn,
                killer_sprite,
                player_killer_skin if self.skin_unlocked(player_killer_skin) else "classic",
                killer_walk_frames,
            )
            self.survivor = Survivor(
                "AI Survivor",
                survivor_spawn,
                survivor_sprite,
                ai_survivor_id,
                survivor_walk_frames,
            )
            self.killers = [self.player]

        self.state = GameState.PLAYING
        self.start_round_music()

    def spawn_position(
        self,
        x_ratio: float,
        y_ratio: float,
        avoid_pos: pygame.Vector2 | None = None,
    ) -> pygame.Vector2:
        pos = pygame.Vector2(
            ARENA_RECT.left + ARENA_RECT.width * x_ratio,
            ARENA_RECT.top + ARENA_RECT.height * y_ratio,
        )
        rect = pygame.Rect(0, 0, CHARACTER_COLLISION_SIZE, CHARACTER_COLLISION_SIZE)
        rect.center = (round(pos.x), round(pos.y))
        blocked = not ARENA_RECT.contains(rect) or any(rect.colliderect(wall.rect) for wall in self.walls)
        if not blocked:
            return pos

        open_pos = self.random_open_position(avoid_pos, 180 if avoid_pos is not None else 0)
        return open_pos if open_pos is not None else pygame.Vector2(ARENA_RECT.center)

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

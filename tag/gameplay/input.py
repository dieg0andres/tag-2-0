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


class InputMixin:
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.is_resize_event(event):
                width = getattr(event, "w", None) or getattr(event, "x", None) or self.window_width()
                height = getattr(event, "h", None) or getattr(event, "y", None) or self.window_height()
                self.handle_window_resize(width, height)
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)

    def is_resize_event(self, event: pygame.event.Event) -> bool:
        resize_types = {pygame.VIDEORESIZE}
        for name in ("WINDOWRESIZED", "WINDOWSIZECHANGED"):
            if hasattr(pygame, name):
                resize_types.add(getattr(pygame, name))
        return event.type in resize_types

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
        window_width = self.window_width()
        card_width = 210
        card_height = 70
        card_gap = 18
        row_gap = 8
        columns = min(4, len(SURVIVOR_IDS), max(2, (window_width - 80) // (card_width + card_gap)))
        row = index // columns
        column = index % columns
        total_width = columns * card_width + (columns - 1) * card_gap
        start_x = (window_width - total_width) // 2
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
        window_width = self.window_width()
        card_width = 210
        card_height = 70
        card_gap = 18
        row_gap = 8
        options = self.skin_options_for_killer(self.round_killer)
        columns = min(4, len(options), max(2, (window_width - 80) // (card_width + card_gap)))
        row = index // columns
        column = index % columns
        total_width = columns * card_width + (columns - 1) * card_gap
        start_x = (window_width - total_width) // 2
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
        window_width = self.window_width()
        card_gap = 16
        card_width = min(172, max(140, (window_width - 96 - (len(KILLER_IDS) - 1) * card_gap) // len(KILLER_IDS)))
        total_width = len(KILLER_IDS) * card_width + (len(KILLER_IDS) - 1) * card_gap
        start_x = (window_width - total_width) // 2
        return pygame.Rect(start_x + index * (card_width + card_gap), 170, card_width, 305)

    def killer_from_card_click(self, pos: tuple[int, int]) -> str | None:
        for index, killer_id in enumerate(KILLER_IDS):
            if self.killer_card_rect(index).collidepoint(pos):
                return killer_id
        return None

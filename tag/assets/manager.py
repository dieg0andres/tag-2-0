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


class AssetMixin:
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


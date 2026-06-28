from __future__ import annotations

import random
import sys

import pygame

import tag.config.settings as settings
from tag.ai.behaviors import AIMixin
from tag.assets.manager import AssetMixin
from tag.config.settings import *
from tag.core.state import GameState
from tag.data.content import *
from tag.entities.objects import *
from tag.gameplay.abilities.killer.core import KillerAbilitiesMixin
from tag.gameplay.abilities.survivor import SurvivorAbilitiesMixin
from tag.gameplay.input import InputMixin
from tag.gameplay.systems.round_flow import RoundFlowMixin
from tag.gameplay.systems.simulation import SimulationMixin
from tag.persistence.progress import PersistenceMixin
from tag.ui.screen_mixins import UIMixin
from tag.world.arena import WorldMixin


class Game(AssetMixin, PersistenceMixin, WorldMixin, InputMixin, SurvivorAbilitiesMixin, KillerAbilitiesMixin, RoundFlowMixin, SimulationMixin, AIMixin, UIMixin):
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tag 2.0")
        settings.resize_layout(WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), WINDOW_FLAGS)
        self.clock = pygame.time.Clock()

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
        self.wall_layout_id = 0

        self.menu_buttons = {
            "play": Button(pygame.Rect(0, 0, 220, 58), "Start"),
            "reveal": Button(pygame.Rect(0, 0, 220, 58), "Reveal Role"),
            "begin": Button(pygame.Rect(0, 0, 220, 58), "Begin Round"),
        }
        self.update_menu_buttons()

        self.audio_enabled = False
        self.music_tracks: dict[str, Path] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.setup_audio()

    def window_width(self) -> int:
        return self.screen.get_width()

    def window_height(self) -> int:
        return self.screen.get_height()

    def window_center_x(self) -> int:
        return self.window_width() // 2

    def update_menu_buttons(self) -> None:
        width = self.window_width()
        height = self.window_height()
        center_x = width // 2
        self.menu_buttons["play"].rect.center = (center_x, min(max(420, height - 300), 490))
        self.menu_buttons["reveal"].rect.center = (center_x, min(max(540, height - 205), height - 150))
        self.menu_buttons["begin"].rect.center = (center_x, min(max(560, height - 170), height - 105))

    def handle_window_resize(self, width: int, height: int) -> None:
        old_arena = ARENA_RECT.copy()
        new_width, new_height = settings.resize_layout(width, height)
        self.screen = pygame.display.set_mode((new_width, new_height), WINDOW_FLAGS)
        self.update_menu_buttons()
        self.walls = self.create_walls()
        self.rescale_world_for_resize(old_arena, ARENA_RECT)

    def rescale_world_for_resize(self, old_arena: pygame.Rect, new_arena: pygame.Rect) -> None:
        if old_arena.width <= 0 or old_arena.height <= 0:
            return

        def scale_point(point: pygame.Vector2 | tuple[float, float]) -> pygame.Vector2:
            source = pygame.Vector2(point)
            x_ratio = (source.x - old_arena.left) / old_arena.width
            y_ratio = (source.y - old_arena.top) / old_arena.height
            return pygame.Vector2(
                new_arena.left + x_ratio * new_arena.width,
                new_arena.top + y_ratio * new_arena.height,
            )

        moved: set[int] = set()
        objects: list[object] = []
        for value in (
            self.player,
            self.survivor,
            *self.killers,
            *self.active_hitboxes,
            *self.projectiles,
            *self.ducky_belts,
            *self.landmines,
            *self.survivor_shots,
            *self.trashy_shockwaves,
            *self.trashy_turrets,
            *self.trashy_turret_shots,
            *self.goopy_knights,
            *self.malice_bird_poops,
            *self.malice_helper_birds,
        ):
            if value is not None and id(value) not in moved:
                moved.add(id(value))
                objects.append(value)

        for item in objects:
            rect = getattr(item, "rect", None)
            pos = getattr(item, "pos", None)
            if pos is not None:
                new_pos = scale_point(pos)
                pos.update(new_pos)
                if isinstance(rect, pygame.Rect):
                    rect.center = (round(new_pos.x), round(new_pos.y))
            elif isinstance(rect, pygame.Rect):
                new_center = scale_point(rect.center)
                rect.center = (round(new_center.x), round(new_center.y))

            if isinstance(item, Character):
                item.rect.clamp_ip(new_arena)
                item.pos.update(item.rect.center)
                self.resolve_wall_overlap(item)

        if isinstance(self.player, Survivor) and self.player.kitty_marker is not None:
            self.player.kitty_marker.update(scale_point(self.player.kitty_marker))
        if self.dinosaur_shockwave_timer > 0:
            self.dinosaur_shockwave_pos.update(scale_point(self.dinosaur_shockwave_pos))
        if isinstance(self.player, Survivor) and self.player.trashy_minigame_active:
            self.player.trashy_circle_x = float(TRASHY_MINIGAME_BAR.left + TRASHY_MINIGAME_CIRCLE_RADIUS)
            self.player.choose_new_trashy_target()

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

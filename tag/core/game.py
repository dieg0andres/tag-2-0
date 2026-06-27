from __future__ import annotations

import random
import sys

import pygame

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


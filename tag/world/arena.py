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


BASE_ARENA = pygame.Rect(24, 112, 884, 664)
ARENA_LAYOUTS = [
    {
        "name": "Open Cross",
        "difficulty": "Easy",
        "fill": (67, 73, 85),
        "border": (126, 137, 151),
        "walls": [
            pygame.Rect(140, 190, 245, 30),
            pygame.Rect(615, 175, 250, 30),
            pygame.Rect(475, 270, 44, 165),
            pygame.Rect(150, 360, 205, 32),
            pygame.Rect(665, 350, 205, 32),
            pygame.Rect(315, 510, 118, 30),
            pygame.Rect(560, 555, 130, 30),
            pygame.Rect(860, 585, 34, 130),
            pygame.Rect(90, 590, 34, 130),
        ],
    },
    {
        "name": "Broken Lanes",
        "difficulty": "Easy",
        "fill": (78, 92, 112),
        "border": (167, 189, 212),
        "walls": [
            pygame.Rect(100, 205, 210, 28),
            pygame.Rect(390, 205, 185, 28),
            pygame.Rect(650, 205, 205, 28),
            pygame.Rect(175, 345, 260, 30),
            pygame.Rect(535, 345, 260, 30),
            pygame.Rect(115, 505, 220, 32),
            pygame.Rect(415, 505, 155, 32),
            pygame.Rect(660, 505, 215, 32),
            pygame.Rect(455, 620, 52, 92),
        ],
    },
    {
        "name": "Pinwheel",
        "difficulty": "Medium",
        "fill": (83, 78, 117),
        "border": (196, 181, 253),
        "walls": [
            pygame.Rect(430, 205, 250, 30),
            pygame.Rect(575, 205, 34, 150),
            pygame.Rect(335, 345, 275, 30),
            pygame.Rect(335, 345, 34, 145),
            pygame.Rect(335, 465, 270, 30),
            pygame.Rect(570, 465, 34, 145),
            pygame.Rect(360, 585, 275, 30),
            pygame.Rect(135, 285, 115, 28),
            pygame.Rect(755, 560, 115, 28),
        ],
    },
    {
        "name": "Maze Sprint",
        "difficulty": "Medium",
        "fill": (88, 74, 64),
        "border": (251, 191, 36),
        "walls": [
            pygame.Rect(115, 185, 34, 175),
            pygame.Rect(235, 315, 34, 190),
            pygame.Rect(355, 185, 34, 190),
            pygame.Rect(475, 335, 34, 190),
            pygame.Rect(595, 185, 34, 190),
            pygame.Rect(715, 335, 34, 190),
            pygame.Rect(835, 185, 34, 190),
            pygame.Rect(120, 610, 235, 30),
            pygame.Rect(610, 610, 245, 30),
        ],
    },
    {
        "name": "Island Hops",
        "difficulty": "Medium",
        "fill": (56, 101, 94),
        "border": (94, 234, 212),
        "walls": [
            pygame.Rect(145, 215, 120, 78),
            pygame.Rect(380, 185, 140, 72),
            pygame.Rect(680, 210, 130, 82),
            pygame.Rect(250, 380, 150, 82),
            pygame.Rect(555, 360, 160, 88),
            pygame.Rect(115, 570, 140, 78),
            pygame.Rect(400, 585, 150, 74),
            pygame.Rect(720, 560, 135, 86),
            pygame.Rect(470, 430, 44, 58),
        ],
    },
    {
        "name": "Corner Cutters",
        "difficulty": "Hard",
        "fill": (102, 67, 67),
        "border": (252, 165, 165),
        "walls": [
            pygame.Rect(110, 185, 220, 30),
            pygame.Rect(115, 185, 34, 160),
            pygame.Rect(620, 185, 245, 30),
            pygame.Rect(830, 185, 34, 165),
            pygame.Rect(110, 610, 240, 30),
            pygame.Rect(110, 480, 34, 160),
            pygame.Rect(625, 610, 240, 30),
            pygame.Rect(830, 480, 34, 160),
            pygame.Rect(415, 335, 145, 32),
            pygame.Rect(415, 465, 145, 32),
        ],
    },
    {
        "name": "Zig Zag",
        "difficulty": "Hard",
        "fill": (70, 91, 62),
        "border": (190, 242, 100),
        "walls": [
            pygame.Rect(120, 205, 245, 28),
            pygame.Rect(365, 205, 34, 115),
            pygame.Rect(315, 320, 275, 28),
            pygame.Rect(590, 320, 34, 115),
            pygame.Rect(360, 435, 275, 28),
            pygame.Rect(315, 435, 34, 115),
            pygame.Rect(120, 550, 260, 28),
            pygame.Rect(575, 550, 275, 28),
            pygame.Rect(810, 550, 34, 125),
            pygame.Rect(455, 650, 110, 28),
        ],
    },
    {
        "name": "Split Arena",
        "difficulty": "Hard",
        "fill": (73, 84, 118),
        "border": (147, 197, 253),
        "walls": [
            pygame.Rect(455, 165, 42, 210),
            pygame.Rect(455, 465, 42, 240),
            pygame.Rect(145, 260, 220, 30),
            pygame.Rect(590, 260, 225, 30),
            pygame.Rect(145, 420, 220, 30),
            pygame.Rect(590, 420, 225, 30),
            pygame.Rect(145, 590, 220, 30),
            pygame.Rect(590, 590, 225, 30),
            pygame.Rect(290, 705, 115, 26),
            pygame.Rect(555, 705, 115, 26),
        ],
    },
    {
        "name": "Pressure Boxes",
        "difficulty": "Expert",
        "fill": (96, 64, 86),
        "border": (249, 168, 212),
        "walls": [
            pygame.Rect(140, 195, 155, 30),
            pygame.Rect(140, 195, 32, 135),
            pygame.Rect(650, 195, 175, 30),
            pygame.Rect(793, 195, 32, 135),
            pygame.Rect(360, 320, 220, 32),
            pygame.Rect(470, 320, 34, 150),
            pygame.Rect(155, 505, 190, 30),
            pygame.Rect(155, 505, 34, 145),
            pygame.Rect(615, 505, 210, 30),
            pygame.Rect(792, 505, 34, 145),
            pygame.Rect(395, 650, 175, 30),
        ],
    },
    {
        "name": "Chaos Chase",
        "difficulty": "Expert",
        "fill": (76, 58, 102),
        "border": (216, 180, 254),
        "walls": [
            pygame.Rect(100, 205, 165, 30),
            pygame.Rect(340, 170, 38, 145),
            pygame.Rect(470, 245, 175, 30),
            pygame.Rect(760, 190, 38, 150),
            pygame.Rect(185, 365, 175, 32),
            pygame.Rect(525, 390, 38, 150),
            pygame.Rect(670, 455, 175, 32),
            pygame.Rect(120, 585, 38, 135),
            pygame.Rect(310, 585, 190, 30),
            pygame.Rect(590, 630, 38, 105),
            pygame.Rect(730, 610, 150, 30),
        ],
    },
]


class WorldMixin:
    def select_random_wall_layout(self) -> None:
        self.wall_layout_id = random.randrange(len(ARENA_LAYOUTS))

    def create_walls(self) -> list[Wall]:
        layout_id = getattr(self, "wall_layout_id", 0) or 0
        layout = ARENA_LAYOUTS[layout_id % len(ARENA_LAYOUTS)]
        fill = layout["fill"]
        border = layout["border"]

        wall_rects = []
        for rect in layout["walls"]:
            x_ratio = (rect.left - BASE_ARENA.left) / BASE_ARENA.width
            y_ratio = (rect.top - BASE_ARENA.top) / BASE_ARENA.height
            width_ratio = rect.width / BASE_ARENA.width
            height_ratio = rect.height / BASE_ARENA.height
            wall_rects.append(
                pygame.Rect(
                    ARENA_RECT.left + round(x_ratio * ARENA_RECT.width),
                    ARENA_RECT.top + round(y_ratio * ARENA_RECT.height),
                    max(26, round(width_ratio * ARENA_RECT.width)),
                    max(22, round(height_ratio * ARENA_RECT.height)),
                )
            )
        return [Wall(rect, fill, border) for rect in wall_rects]

    def current_perimeter_edge(self, rect: pygame.Rect) -> str | None:
        if rect.top <= ARENA_RECT.top + PERIMETER_MARGIN:
            return "top"
        if rect.right >= ARENA_RECT.right - PERIMETER_MARGIN:
            return "right"
        if rect.bottom >= ARENA_RECT.bottom - PERIMETER_MARGIN:
            return "bottom"
        if rect.left <= ARENA_RECT.left + PERIMETER_MARGIN:
            return "left"
        return None

    def resolve_wall_overlap(self, character: Character) -> None:
        for wall in self.walls:
            if not character.rect.colliderect(wall.rect):
                continue

            overlap = character.rect.clip(wall.rect)
            if overlap.width < overlap.height:
                if character.rect.centerx < wall.rect.centerx:
                    character.rect.right = wall.rect.left
                else:
                    character.rect.left = wall.rect.right
            else:
                if character.rect.centery < wall.rect.centery:
                    character.rect.bottom = wall.rect.top
                else:
                    character.rect.top = wall.rect.bottom

            character.pos.update(character.rect.center)

    def random_open_position(
        self,
        avoid_pos: pygame.Vector2 | None,
        min_distance: float,
    ) -> pygame.Vector2 | None:
        half = CHARACTER_COLLISION_SIZE // 2

        for _ in range(100):
            x = random.randint(ARENA_RECT.left + half, ARENA_RECT.right - half)
            y = random.randint(ARENA_RECT.top + half, ARENA_RECT.bottom - half)
            rect = pygame.Rect(0, 0, CHARACTER_COLLISION_SIZE, CHARACTER_COLLISION_SIZE)
            rect.center = (x, y)

            if not ARENA_RECT.contains(rect):
                continue
            if any(rect.colliderect(wall.rect) for wall in self.walls):
                continue
            if avoid_pos is not None and pygame.Vector2(x, y).distance_to(avoid_pos) < min_distance:
                continue

            return pygame.Vector2(x, y)

        return None

    def draw_arena_preview(self) -> None:
        width, height = self.screen.get_size()
        preview = pygame.Rect(0, 0, min(760, width - 120), min(230, max(180, int(height * 0.28))))
        preview.center = (width // 2, min(475, height - 220))
        pygame.draw.rect(self.screen, (20, 31, 48), preview, border_radius=18)
        pygame.draw.rect(self.screen, (64, 77, 98), preview, 2, border_radius=18)
        for x in range(preview.left + 28, preview.right, 58):
            pygame.draw.line(self.screen, (28, 41, 62), (x, preview.top + 10), (x, preview.bottom - 10))
        for y in range(preview.top + 28, preview.bottom, 58):
            pygame.draw.line(self.screen, (28, 41, 62), (preview.left + 10, y), (preview.right - 10, y))

    def draw_arena(self) -> None:
        pygame.draw.rect(self.screen, (20, 31, 48), ARENA_RECT, border_radius=12)
        pygame.draw.rect(self.screen, (91, 106, 130), ARENA_RECT, 3, border_radius=12)

        for x in range(ARENA_RECT.left + 40, ARENA_RECT.right, 40):
            pygame.draw.line(
                self.screen,
                (28, 41, 62),
                (x, ARENA_RECT.top),
                (x, ARENA_RECT.bottom),
                1,
            )
        for y in range(ARENA_RECT.top + 40, ARENA_RECT.bottom, 40):
            pygame.draw.line(
                self.screen,
                (28, 41, 62),
                (ARENA_RECT.left, y),
                (ARENA_RECT.right, y),
                1,
            )

        for wall in self.walls:
            wall.draw(self.screen)

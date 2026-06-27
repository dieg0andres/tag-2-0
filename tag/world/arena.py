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


class WorldMixin:
    def create_walls(self) -> list[Wall]:
        base_arena = pygame.Rect(24, 112, 884, 664)
        base_wall_rects = [
            pygame.Rect(145, 205, 245, 30),
            pygame.Rect(610, 185, 250, 30),
            pygame.Rect(475, 295, 44, 190),
            pygame.Rect(160, 505, 205, 32),
            pygame.Rect(665, 490, 205, 32),
            pygame.Rect(315, 385, 118, 30),
            pygame.Rect(565, 370, 110, 30),
            pygame.Rect(865, 300, 34, 125),
            pygame.Rect(90, 325, 34, 135),
        ]

        wall_rects = []
        for rect in base_wall_rects:
            x_ratio = (rect.left - base_arena.left) / base_arena.width
            y_ratio = (rect.top - base_arena.top) / base_arena.height
            width_ratio = rect.width / base_arena.width
            height_ratio = rect.height / base_arena.height
            wall_rects.append(
                pygame.Rect(
                    ARENA_RECT.left + round(x_ratio * ARENA_RECT.width),
                    ARENA_RECT.top + round(y_ratio * ARENA_RECT.height),
                    max(26, round(width_ratio * ARENA_RECT.width)),
                    max(22, round(height_ratio * ARENA_RECT.height)),
                )
            )
        return [Wall(rect) for rect in wall_rects]

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

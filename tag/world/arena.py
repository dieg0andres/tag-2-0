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
from tag.ui.theme import COLORS
from tag.utils.text import draw_text, draw_wrapped_text, draw_wrapped_text_left
from tag.utils.vector import facing_axis, safe_normalize, vector_from_keys


BASE_ARENA = pygame.Rect(24, 112, 884, 664)


def moving_wall(
    rect: pygame.Rect,
    drift: tuple[int, int] = (0, 0),
    speed: float = 0.0,
    phase: float = 0.0,
    spin_speed: float = 0.0,
    spin_range: float = 0.0,
    spin_phase: float = 0.0,
    active_after: float = 0.0,
) -> dict[str, object]:
    return {
        "rect": rect,
        "drift": drift,
        "speed": speed,
        "phase": phase,
        "spin_speed": spin_speed,
        "spin_range": spin_range,
        "spin_phase": spin_phase,
        "active_after": active_after,
    }


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
    {
        "name": "Serpent Run",
        "difficulty": "Expert",
        "fill": (48, 89, 91),
        "border": (103, 232, 249),
        "walls": [
            pygame.Rect(95, 180, 190, 28),
            pygame.Rect(255, 180, 32, 120),
            pygame.Rect(255, 300, 210, 28),
            pygame.Rect(465, 220, 32, 108),
            pygame.Rect(465, 220, 215, 28),
            pygame.Rect(680, 220, 32, 132),
            pygame.Rect(485, 352, 227, 28),
            pygame.Rect(455, 352, 32, 122),
            pygame.Rect(245, 474, 242, 28),
            pygame.Rect(245, 474, 32, 140),
            pygame.Rect(245, 614, 260, 28),
            pygame.Rect(655, 520, 190, 30),
        ],
    },
    {
        "name": "Vault Rooms",
        "difficulty": "Expert",
        "fill": (74, 79, 92),
        "border": (226, 232, 240),
        "walls": [
            pygame.Rect(115, 190, 175, 28),
            pygame.Rect(115, 190, 28, 150),
            pygame.Rect(262, 255, 28, 120),
            pygame.Rect(610, 190, 175, 28),
            pygame.Rect(757, 190, 28, 150),
            pygame.Rect(610, 255, 28, 120),
            pygame.Rect(350, 340, 250, 32),
            pygame.Rect(350, 455, 250, 32),
            pygame.Rect(115, 570, 175, 28),
            pygame.Rect(262, 500, 28, 98),
            pygame.Rect(610, 570, 175, 28),
            pygame.Rect(610, 500, 28, 98),
        ],
    },
    {
        "name": "Double Helix",
        "difficulty": "Expert",
        "fill": (64, 74, 109),
        "border": (129, 140, 248),
        "walls": [
            pygame.Rect(150, 180, 170, 28),
            pygame.Rect(150, 285, 240, 28),
            pygame.Rect(220, 390, 250, 28),
            pygame.Rect(155, 495, 235, 28),
            pygame.Rect(150, 600, 170, 28),
            pygame.Rect(645, 180, 170, 28),
            pygame.Rect(575, 285, 240, 28),
            pygame.Rect(495, 390, 250, 28),
            pygame.Rect(575, 495, 235, 28),
            pygame.Rect(645, 600, 170, 28),
            pygame.Rect(455, 225, 42, 115),
            pygame.Rect(455, 520, 42, 115),
        ],
    },
    {
        "name": "Needle Garden",
        "difficulty": "Hard",
        "fill": (84, 92, 58),
        "border": (217, 249, 157),
        "walls": [
            pygame.Rect(125, 175, 28, 112),
            pygame.Rect(230, 235, 28, 150),
            pygame.Rect(335, 175, 28, 112),
            pygame.Rect(440, 235, 28, 150),
            pygame.Rect(545, 175, 28, 112),
            pygame.Rect(650, 235, 28, 150),
            pygame.Rect(755, 175, 28, 112),
            pygame.Rect(160, 500, 28, 150),
            pygame.Rect(285, 430, 28, 150),
            pygame.Rect(410, 500, 28, 150),
            pygame.Rect(535, 430, 28, 150),
            pygame.Rect(660, 500, 28, 150),
            pygame.Rect(785, 430, 28, 150),
        ],
    },
    {
        "name": "Trapdoor Grid",
        "difficulty": "Expert",
        "fill": (97, 61, 76),
        "border": (251, 113, 133),
        "walls": [
            pygame.Rect(120, 205, 130, 28),
            pygame.Rect(330, 205, 130, 28),
            pygame.Rect(540, 205, 130, 28),
            pygame.Rect(750, 205, 110, 28),
            pygame.Rect(210, 330, 130, 28),
            pygame.Rect(420, 330, 130, 28),
            pygame.Rect(630, 330, 130, 28),
            pygame.Rect(120, 455, 130, 28),
            pygame.Rect(330, 455, 130, 28),
            pygame.Rect(540, 455, 130, 28),
            pygame.Rect(750, 455, 110, 28),
            pygame.Rect(210, 580, 130, 28),
            pygame.Rect(420, 580, 130, 28),
            pygame.Rect(630, 580, 130, 28),
            pygame.Rect(470, 655, 36, 72),
        ],
    },
    {
        "name": "Theater Curtains",
        "difficulty": "Hard",
        "fill": (104, 52, 70),
        "border": (253, 164, 175),
        "walls": [
            pygame.Rect(95, 180, 34, 245),
            pygame.Rect(180, 230, 34, 245),
            pygame.Rect(265, 180, 34, 245),
            pygame.Rect(350, 230, 34, 245),
            pygame.Rect(575, 180, 34, 245),
            pygame.Rect(660, 230, 34, 245),
            pygame.Rect(745, 180, 34, 245),
            pygame.Rect(830, 230, 34, 245),
            pygame.Rect(410, 575, 150, 30),
            pygame.Rect(410, 670, 150, 30),
        ],
    },
    {
        "name": "Satellite Rings",
        "difficulty": "Expert",
        "fill": (50, 80, 108),
        "border": (125, 211, 252),
        "walls": [
            pygame.Rect(210, 190, 155, 28),
            pygame.Rect(210, 190, 28, 135),
            pygame.Rect(337, 190, 28, 135),
            pygame.Rect(210, 325, 155, 28),
            pygame.Rect(600, 190, 155, 28),
            pygame.Rect(600, 190, 28, 135),
            pygame.Rect(727, 190, 28, 135),
            pygame.Rect(600, 325, 155, 28),
            pygame.Rect(375, 410, 210, 30),
            pygame.Rect(210, 555, 155, 28),
            pygame.Rect(337, 555, 28, 135),
            pygame.Rect(600, 555, 155, 28),
            pygame.Rect(600, 555, 28, 135),
        ],
    },
    {
        "name": "Spiral Lock",
        "difficulty": "Expert",
        "fill": (88, 73, 58),
        "border": (253, 186, 116),
        "walls": [
            pygame.Rect(150, 185, 650, 28),
            pygame.Rect(772, 185, 28, 440),
            pygame.Rect(260, 625, 540, 28),
            pygame.Rect(260, 305, 28, 348),
            pygame.Rect(260, 305, 410, 28),
            pygame.Rect(642, 305, 28, 220),
            pygame.Rect(370, 525, 300, 28),
            pygame.Rect(370, 405, 28, 148),
            pygame.Rect(370, 405, 178, 28),
            pygame.Rect(520, 405, 28, 72),
        ],
    },
    {
        "name": "Drifting Gates",
        "difficulty": "Moving",
        "fill": (47, 86, 75),
        "border": (110, 231, 183),
        "walls": [
            pygame.Rect(130, 205, 180, 30),
            pygame.Rect(650, 205, 180, 30),
            {"rect": pygame.Rect(385, 265, 34, 190), "drift": (90, 0), "speed": 0.42, "phase": 0.0},
            {"rect": pygame.Rect(545, 265, 34, 190), "drift": (-90, 0), "speed": 0.42, "phase": 1.57},
            pygame.Rect(125, 405, 205, 30),
            pygame.Rect(635, 405, 205, 30),
            {"rect": pygame.Rect(250, 560, 180, 30), "drift": (0, 55), "speed": 0.35, "phase": 0.75},
            {"rect": pygame.Rect(535, 610, 180, 30), "drift": (0, -55), "speed": 0.35, "phase": 2.25},
            pygame.Rect(800, 565, 38, 125),
            pygame.Rect(110, 565, 38, 125),
        ],
    },
    {
        "name": "Tide Shift",
        "difficulty": "Moving",
        "fill": (38, 82, 111),
        "border": (56, 189, 248),
        "walls": [
            {"rect": pygame.Rect(120, 210, 210, 30), "drift": (70, 0), "speed": 0.30, "phase": 0.0},
            {"rect": pygame.Rect(620, 210, 210, 30), "drift": (-70, 0), "speed": 0.30, "phase": 3.14},
            pygame.Rect(455, 255, 44, 130),
            {"rect": pygame.Rect(185, 375, 200, 30), "drift": (0, 65), "speed": 0.27, "phase": 1.0},
            {"rect": pygame.Rect(570, 445, 200, 30), "drift": (0, -65), "speed": 0.27, "phase": 2.4},
            pygame.Rect(120, 610, 190, 30),
            pygame.Rect(655, 610, 190, 30),
            pygame.Rect(330, 555, 34, 135),
            pygame.Rect(605, 555, 34, 135),
            pygame.Rect(440, 685, 95, 28),
        ],
    },
    {
        "name": "Kinetic Crossroads",
        "difficulty": "Medium",
        "fill": (48, 77, 92),
        "border": (103, 232, 249),
        "walls": [
            moving_wall(pygame.Rect(185, 205, 190, 28), (65, 0), 0.95, 0.0),
            moving_wall(pygame.Rect(590, 205, 190, 28), (-65, 0), 0.95, 3.14),
            moving_wall(pygame.Rect(465, 285, 38, 165), (0, 55), 0.88, 1.2, 1.15, 13),
            pygame.Rect(150, 390, 165, 30),
            pygame.Rect(645, 390, 165, 30),
            moving_wall(pygame.Rect(235, 535, 210, 30), (0, -58), 0.82, 2.1),
            moving_wall(pygame.Rect(530, 535, 210, 30), (0, 58), 0.82, 0.5),
            pygame.Rect(110, 630, 36, 92),
            pygame.Rect(820, 630, 36, 92),
        ],
    },
    {
        "name": "Rotary Hall",
        "difficulty": "Medium",
        "fill": (72, 61, 100),
        "border": (216, 180, 254),
        "walls": [
            moving_wall(pygame.Rect(180, 190, 190, 28), (0, 48), 0.75, 0.3, 1.10, 12),
            moving_wall(pygame.Rect(600, 190, 190, 28), (0, 48), 0.75, 2.8, 1.10, 12, 1.57),
            pygame.Rect(115, 325, 185, 30),
            pygame.Rect(665, 325, 185, 30),
            moving_wall(pygame.Rect(395, 365, 175, 32), (80, 0), 1.05, 0.0, 1.30, 18),
            moving_wall(pygame.Rect(395, 505, 175, 32), (-80, 0), 1.05, 3.14, 1.30, 18, 1.57),
            pygame.Rect(205, 610, 170, 28),
            pygame.Rect(590, 610, 170, 28),
            moving_wall(pygame.Rect(465, 620, 36, 90), (0, -34), 0.90, 1.1, 1.45, 16),
        ],
    },
    {
        "name": "Neon Switchbacks",
        "difficulty": "Hard",
        "fill": (63, 85, 63),
        "border": (190, 242, 100),
        "walls": [
            moving_wall(pygame.Rect(120, 185, 230, 28), (50, 0), 1.10, 0.0),
            moving_wall(pygame.Rect(365, 245, 34, 145), (0, 48), 0.92, 1.0),
            moving_wall(pygame.Rect(240, 390, 255, 28), (-65, 0), 1.08, 2.1, 1.0, 10),
            moving_wall(pygame.Rect(560, 315, 34, 145), (0, -48), 0.92, 2.4),
            moving_wall(pygame.Rect(480, 460, 250, 28), (62, 0), 1.08, 0.7, 1.0, 10, 1.5),
            pygame.Rect(120, 555, 185, 28),
            pygame.Rect(655, 555, 185, 28),
            moving_wall(pygame.Rect(420, 620, 130, 28), (0, 58), 0.86, 0.4, 1.25, 14),
            pygame.Rect(825, 640, 34, 72),
        ],
    },
    {
        "name": "Pendulum Rooms",
        "difficulty": "Medium",
        "fill": (92, 64, 72),
        "border": (253, 164, 175),
        "walls": [
            pygame.Rect(120, 190, 150, 28),
            moving_wall(pygame.Rect(330, 205, 155, 30), (0, 70), 0.80, 0.2, 1.2, 20),
            pygame.Rect(690, 190, 150, 28),
            moving_wall(pygame.Rect(500, 300, 34, 165), (85, 0), 0.98, 1.4),
            pygame.Rect(155, 390, 175, 30),
            pygame.Rect(630, 390, 175, 30),
            moving_wall(pygame.Rect(265, 545, 145, 28), (75, 0), 0.90, 2.1, 1.1, 14),
            moving_wall(pygame.Rect(555, 545, 145, 28), (-75, 0), 0.90, 0.5, 1.1, 14, 2.0),
            pygame.Rect(450, 640, 60, 82),
        ],
    },
    {
        "name": "Rolling Barricades",
        "difficulty": "Hard",
        "fill": (64, 78, 103),
        "border": (147, 197, 253),
        "walls": [
            moving_wall(pygame.Rect(130, 210, 165, 32), (75, 0), 1.20, 0.0, 1.25, 15),
            moving_wall(pygame.Rect(400, 210, 165, 32), (75, 0), 1.20, 1.8, 1.25, 15),
            moving_wall(pygame.Rect(640, 210, 165, 32), (-62, 0), 1.20, 3.0, 1.25, 15),
            pygame.Rect(225, 350, 34, 150),
            moving_wall(pygame.Rect(350, 390, 260, 30), (0, 72), 0.85, 0.6),
            pygame.Rect(715, 350, 34, 150),
            moving_wall(pygame.Rect(135, 600, 190, 30), (65, 0), 1.05, 2.2),
            moving_wall(pygame.Rect(635, 600, 190, 30), (-65, 0), 1.05, 0.8),
            pygame.Rect(465, 610, 42, 90),
        ],
    },
    {
        "name": "Clockwork Canal",
        "difficulty": "Medium",
        "fill": (78, 72, 52),
        "border": (253, 224, 71),
        "walls": [
            moving_wall(pygame.Rect(170, 205, 150, 30), (0, 58), 0.78, 0.0),
            moving_wall(pygame.Rect(405, 205, 150, 30), (0, -58), 0.78, 1.57),
            moving_wall(pygame.Rect(640, 205, 150, 30), (0, 58), 0.78, 3.14),
            pygame.Rect(110, 350, 220, 28),
            pygame.Rect(635, 350, 220, 28),
            moving_wall(pygame.Rect(455, 410, 50, 125), (70, 0), 1.0, 0.6, 1.35, 18),
            pygame.Rect(160, 565, 165, 28),
            moving_wall(pygame.Rect(395, 585, 170, 28), (0, 58), 0.9, 2.0, 1.3, 14),
            pygame.Rect(650, 565, 165, 28),
        ],
    },
    {
        "name": "Shifting Courtyard",
        "difficulty": "Hard",
        "fill": (55, 91, 83),
        "border": (94, 234, 212),
        "walls": [
            moving_wall(pygame.Rect(140, 190, 120, 74), (65, 0), 0.95, 0.0, 1.15, 12),
            moving_wall(pygame.Rect(360, 185, 145, 66), (0, 58), 0.88, 1.2),
            moving_wall(pygame.Rect(675, 190, 130, 74), (-65, 0), 0.95, 3.14, 1.15, 12, 1.1),
            pygame.Rect(210, 365, 190, 28),
            moving_wall(pygame.Rect(470, 350, 40, 150), (90, 0), 1.10, 0.5),
            pygame.Rect(565, 365, 190, 28),
            moving_wall(pygame.Rect(150, 585, 140, 70), (0, -55), 0.82, 2.0),
            moving_wall(pygame.Rect(410, 585, 140, 70), (0, 55), 0.82, 0.5),
            moving_wall(pygame.Rect(700, 585, 140, 70), (0, -55), 0.82, 1.3),
        ],
    },
    {
        "name": "Sawtooth Drift",
        "difficulty": "Hard",
        "fill": (91, 67, 50),
        "border": (251, 146, 60),
        "walls": [
            moving_wall(pygame.Rect(110, 200, 150, 28), (70, 0), 1.18, 0.0),
            moving_wall(pygame.Rect(305, 260, 150, 28), (-70, 0), 1.18, 1.3),
            moving_wall(pygame.Rect(500, 320, 150, 28), (70, 0), 1.18, 2.6),
            moving_wall(pygame.Rect(635, 380, 150, 28), (-60, 0), 1.18, 3.8),
            moving_wall(pygame.Rect(500, 455, 150, 28), (70, 0), 1.18, 1.0),
            moving_wall(pygame.Rect(305, 520, 150, 28), (-70, 0), 1.18, 2.1),
            moving_wall(pygame.Rect(110, 585, 150, 28), (70, 0), 1.18, 3.4),
            pygame.Rect(810, 530, 34, 145),
            pygame.Rect(455, 625, 58, 85),
        ],
    },
    {
        "name": "Orbit Lattice",
        "difficulty": "Medium",
        "fill": (50, 69, 100),
        "border": (125, 211, 252),
        "walls": [
            pygame.Rect(135, 210, 165, 28),
            pygame.Rect(665, 210, 165, 28),
            moving_wall(pygame.Rect(385, 250, 190, 30), (0, 62), 0.83, 0.3, 1.45, 22),
            moving_wall(pygame.Rect(235, 395, 160, 30), (72, 0), 1.02, 1.4, 1.15, 16),
            moving_wall(pygame.Rect(570, 395, 160, 30), (-72, 0), 1.02, 2.9, 1.15, 16, 1.8),
            pygame.Rect(120, 555, 175, 28),
            pygame.Rect(670, 555, 175, 28),
            moving_wall(pygame.Rect(410, 610, 145, 28), (0, -50), 1.0, 0.6, 1.35, 16),
            pygame.Rect(450, 460, 60, 70),
        ],
    },
    {
        "name": "Mixer Maze",
        "difficulty": "Hard",
        "fill": (84, 65, 110),
        "border": (233, 213, 255),
        "walls": [
            moving_wall(pygame.Rect(160, 190, 185, 28), (55, 0), 1.0, 0.0, 1.3, 16),
            moving_wall(pygame.Rect(620, 190, 185, 28), (-55, 0), 1.0, 3.14, 1.3, 16),
            moving_wall(pygame.Rect(260, 315, 34, 155), (0, 60), 0.95, 1.3),
            moving_wall(pygame.Rect(670, 315, 34, 155), (0, -60), 0.95, 2.5),
            pygame.Rect(365, 370, 230, 30),
            moving_wall(pygame.Rect(155, 545, 205, 30), (70, 0), 1.12, 1.1),
            moving_wall(pygame.Rect(605, 545, 205, 30), (-70, 0), 1.12, 2.1),
            moving_wall(pygame.Rect(455, 625, 50, 92), (0, -42), 1.0, 0.3, 1.55, 18),
        ],
    },
    {
        "name": "Half-Time Guillotine",
        "difficulty": "Hard",
        "fill": (96, 54, 65),
        "border": (251, 113, 133),
        "walls": [
            pygame.Rect(120, 190, 200, 28),
            pygame.Rect(640, 190, 200, 28),
            moving_wall(pygame.Rect(455, 235, 48, 185), (0, 85), 1.65, 0.0, 1.75, 20, active_after=ROUND_DURATION / 2),
            pygame.Rect(180, 385, 185, 30),
            pygame.Rect(600, 385, 185, 30),
            moving_wall(pygame.Rect(250, 560, 185, 30), (90, 0), 1.70, 1.5, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(530, 610, 185, 30), (-90, 0), 1.70, 3.0, active_after=ROUND_DURATION / 2),
            pygame.Rect(110, 625, 34, 90),
            pygame.Rect(820, 625, 34, 90),
        ],
    },
    {
        "name": "Second Act Blades",
        "difficulty": "Hard",
        "fill": (72, 60, 103),
        "border": (196, 181, 253),
        "walls": [
            pygame.Rect(120, 220, 170, 28),
            pygame.Rect(675, 220, 170, 28),
            moving_wall(pygame.Rect(380, 260, 205, 28), (0, 70), 1.55, 0.0, 2.0, 24, active_after=ROUND_DURATION / 2),
            pygame.Rect(145, 370, 205, 28),
            pygame.Rect(615, 370, 205, 28),
            moving_wall(pygame.Rect(455, 435, 42, 145), (85, 0), 1.75, 1.1, 1.9, 18, active_after=ROUND_DURATION / 2),
            pygame.Rect(165, 605, 185, 28),
            moving_wall(pygame.Rect(390, 635, 190, 28), (0, -65), 1.60, 2.4, 2.1, 20, active_after=ROUND_DURATION / 2),
            pygame.Rect(615, 605, 185, 28),
        ],
    },
    {
        "name": "Wake-Up Corridors",
        "difficulty": "Medium",
        "fill": (56, 86, 74),
        "border": (134, 239, 172),
        "walls": [
            pygame.Rect(130, 205, 220, 28),
            pygame.Rect(610, 205, 220, 28),
            pygame.Rect(210, 340, 34, 160),
            pygame.Rect(720, 340, 34, 160),
            moving_wall(pygame.Rect(335, 385, 295, 30), (0, 78), 1.45, 0.6, active_after=ROUND_DURATION / 2),
            pygame.Rect(130, 560, 220, 28),
            pygame.Rect(610, 560, 220, 28),
            moving_wall(pygame.Rect(455, 610, 46, 92), (92, 0), 1.80, 2.0, 1.8, 16, active_after=ROUND_DURATION / 2),
        ],
    },
    {
        "name": "Late Surge Locks",
        "difficulty": "Hard",
        "fill": (80, 73, 58),
        "border": (252, 211, 77),
        "walls": [
            pygame.Rect(150, 190, 650, 28),
            pygame.Rect(772, 190, 28, 160),
            pygame.Rect(260, 332, 540, 28),
            moving_wall(pygame.Rect(250, 385, 36, 170), (120, 0), 1.85, 0.0, active_after=ROUND_DURATION / 2),
            pygame.Rect(260, 555, 540, 28),
            pygame.Rect(150, 410, 28, 170),
            moving_wall(pygame.Rect(450, 635, 120, 28), (0, -80), 1.55, 1.2, 2.0, 18, active_after=ROUND_DURATION / 2),
            pygame.Rect(685, 640, 150, 28),
        ],
    },
    {
        "name": "Afterburner Pins",
        "difficulty": "Medium",
        "fill": (50, 80, 105),
        "border": (186, 230, 253),
        "walls": [
            pygame.Rect(150, 205, 140, 28),
            pygame.Rect(675, 205, 140, 28),
            moving_wall(pygame.Rect(330, 245, 34, 135), (0, 90), 1.60, 0.0, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(600, 245, 34, 135), (0, 90), 1.60, 3.14, active_after=ROUND_DURATION / 2),
            pygame.Rect(210, 425, 190, 28),
            pygame.Rect(565, 425, 190, 28),
            moving_wall(pygame.Rect(430, 545, 110, 28), (95, 0), 1.85, 1.5, 2.0, 20, active_after=ROUND_DURATION / 2),
            pygame.Rect(130, 625, 160, 28),
            pygame.Rect(675, 625, 160, 28),
        ],
    },
    {
        "name": "Closing Credits",
        "difficulty": "Hard",
        "fill": (92, 54, 83),
        "border": (244, 114, 182),
        "walls": [
            pygame.Rect(110, 195, 170, 28),
            pygame.Rect(685, 195, 170, 28),
            pygame.Rect(150, 315, 34, 155),
            pygame.Rect(780, 315, 34, 155),
            moving_wall(pygame.Rect(345, 335, 275, 30), (0, 75), 1.65, 0.7, 1.9, 17, active_after=ROUND_DURATION / 2),
            pygame.Rect(160, 570, 190, 28),
            pygame.Rect(615, 570, 190, 28),
            moving_wall(pygame.Rect(455, 620, 46, 95), (115, 0), 1.90, 2.2, active_after=ROUND_DURATION / 2),
        ],
    },
    {
        "name": "Alarm Maze",
        "difficulty": "Hard",
        "fill": (100, 62, 48),
        "border": (253, 186, 116),
        "walls": [
            pygame.Rect(125, 185, 34, 190),
            pygame.Rect(245, 305, 34, 190),
            pygame.Rect(365, 185, 34, 190),
            pygame.Rect(565, 305, 34, 190),
            pygame.Rect(685, 185, 34, 190),
            pygame.Rect(805, 305, 34, 190),
            moving_wall(pygame.Rect(160, 590, 230, 30), (90, 0), 1.65, 0.0, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(575, 590, 230, 30), (-90, 0), 1.65, 3.14, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(455, 625, 55, 65), (0, -58), 1.55, 1.1, 1.9, 15, active_after=ROUND_DURATION / 2),
        ],
    },
    {
        "name": "Final-Half Fan",
        "difficulty": "Medium",
        "fill": (68, 75, 94),
        "border": (203, 213, 225),
        "walls": [
            pygame.Rect(110, 210, 180, 28),
            pygame.Rect(675, 210, 180, 28),
            pygame.Rect(220, 355, 170, 28),
            pygame.Rect(575, 355, 170, 28),
            moving_wall(pygame.Rect(450, 300, 60, 190), (0, 0), 0.0, 0.0, 2.2, 28, active_after=ROUND_DURATION / 2),
            pygame.Rect(110, 540, 180, 28),
            pygame.Rect(675, 540, 180, 28),
            moving_wall(pygame.Rect(390, 615, 185, 28), (85, 0), 1.6, 0.5, active_after=ROUND_DURATION / 2),
        ],
    },
    {
        "name": "Half-Time Switchyard",
        "difficulty": "Hard",
        "fill": (54, 83, 80),
        "border": (153, 246, 228),
        "walls": [
            pygame.Rect(145, 190, 185, 28),
            pygame.Rect(635, 190, 185, 28),
            moving_wall(pygame.Rect(430, 245, 110, 28), (0, 90), 1.75, 0.0, 2.15, 20, active_after=ROUND_DURATION / 2),
            pygame.Rect(190, 365, 180, 28),
            pygame.Rect(595, 365, 180, 28),
            moving_wall(pygame.Rect(455, 435, 48, 150), (95, 0), 1.85, 1.6, active_after=ROUND_DURATION / 2),
            pygame.Rect(140, 620, 180, 28),
            pygame.Rect(645, 620, 180, 28),
            moving_wall(pygame.Rect(420, 620, 130, 28), (0, -80), 1.7, 2.4, 2.0, 18, active_after=ROUND_DURATION / 2),
        ],
    },
    {
        "name": "Sleeping Spikes",
        "difficulty": "Medium",
        "fill": (78, 64, 96),
        "border": (221, 214, 254),
        "walls": [
            pygame.Rect(125, 205, 28, 120),
            pygame.Rect(260, 270, 28, 120),
            pygame.Rect(395, 205, 28, 120),
            pygame.Rect(530, 270, 28, 120),
            pygame.Rect(665, 205, 28, 120),
            pygame.Rect(800, 270, 28, 120),
            moving_wall(pygame.Rect(190, 520, 155, 28), (80, 0), 1.55, 0.0, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(405, 585, 155, 28), (-80, 0), 1.55, 1.6, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(620, 520, 155, 28), (80, 0), 1.55, 3.0, active_after=ROUND_DURATION / 2),
            pygame.Rect(450, 650, 62, 70),
        ],
    },
    {
        "name": "Sudden Spiral",
        "difficulty": "Hard",
        "fill": (74, 83, 50),
        "border": (217, 249, 157),
        "walls": [
            pygame.Rect(165, 190, 620, 28),
            pygame.Rect(757, 190, 28, 230),
            pygame.Rect(300, 420, 485, 28),
            pygame.Rect(300, 300, 28, 148),
            pygame.Rect(300, 300, 310, 28),
            moving_wall(pygame.Rect(610, 300, 36, 160), (0, 75), 1.55, 0.0, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(395, 535, 225, 28), (90, 0), 1.80, 2.0, 1.7, 15, active_after=ROUND_DURATION / 2),
            pygame.Rect(165, 640, 205, 28),
            pygame.Rect(655, 640, 185, 28),
        ],
    },
    {
        "name": "Wake The Walls",
        "difficulty": "Hard",
        "fill": (65, 73, 101),
        "border": (165, 180, 252),
        "walls": [
            pygame.Rect(150, 205, 170, 28),
            pygame.Rect(645, 205, 170, 28),
            pygame.Rect(230, 340, 34, 155),
            pygame.Rect(700, 340, 34, 155),
            moving_wall(pygame.Rect(360, 375, 245, 30), (0, 85), 1.75, 0.0, 2.0, 22, active_after=ROUND_DURATION / 2),
            pygame.Rect(150, 580, 170, 28),
            pygame.Rect(645, 580, 170, 28),
            moving_wall(pygame.Rect(455, 610, 42, 105), (100, 0), 1.95, 1.4, active_after=ROUND_DURATION / 2),
            moving_wall(pygame.Rect(420, 255, 125, 28), (-70, 0), 1.55, 2.6, active_after=ROUND_DURATION / 2),
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

        walls: list[Wall] = []
        for wall_data in layout["walls"]:
            if isinstance(wall_data, dict):
                rect = wall_data["rect"]
                drift = wall_data.get("drift", (0, 0))
                drift_speed = wall_data.get("speed", 0.0)
                drift_phase = wall_data.get("phase", 0.0)
                spin_speed = wall_data.get("spin_speed", 0.0)
                spin_range = wall_data.get("spin_range", 0.0)
                spin_phase = wall_data.get("spin_phase", 0.0)
                active_after = wall_data.get("active_after", 0.0)
            else:
                rect = wall_data
                drift = (0, 0)
                drift_speed = 0.0
                drift_phase = 0.0
                spin_speed = 0.0
                spin_range = 0.0
                spin_phase = 0.0
                active_after = 0.0

            x_ratio = (rect.left - BASE_ARENA.left) / BASE_ARENA.width
            y_ratio = (rect.top - BASE_ARENA.top) / BASE_ARENA.height
            width_ratio = rect.width / BASE_ARENA.width
            height_ratio = rect.height / BASE_ARENA.height
            scaled_rect = pygame.Rect(
                ARENA_RECT.left + round(x_ratio * ARENA_RECT.width),
                ARENA_RECT.top + round(y_ratio * ARENA_RECT.height),
                max(26, round(width_ratio * ARENA_RECT.width)),
                max(22, round(height_ratio * ARENA_RECT.height)),
            )
            scaled_drift = (
                round(drift[0] / BASE_ARENA.width * ARENA_RECT.width),
                round(drift[1] / BASE_ARENA.height * ARENA_RECT.height),
            )
            walls.append(
                Wall(
                    scaled_rect,
                    fill,
                    border,
                    scaled_drift,
                    drift_speed,
                    drift_phase,
                    spin_speed,
                    spin_range,
                    spin_phase,
                    active_after,
                )
            )
        return walls

    def update_walls(self, dt: float) -> None:
        moved = False
        for wall in self.walls:
            moved = wall.update(dt) or moved

        if not moved:
            return

        resolved: set[int] = set()
        for character in (self.player, self.survivor, *self.killers):
            if character is None or id(character) in resolved:
                continue
            resolved.add(id(character))
            if (
                isinstance(character, Killer)
                and (character.is_wall_phasing() or character.is_malice_bird())
            ):
                continue
            self.resolve_wall_overlap(character)

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
        pygame.draw.rect(self.screen, (13, 22, 40), preview, border_radius=22)
        pygame.draw.rect(self.screen, COLORS["border_soft"], preview, 2, border_radius=22)
        for x in range(preview.left + 28, preview.right, 58):
            pygame.draw.line(self.screen, (23, 36, 58), (x, preview.top + 10), (x, preview.bottom - 10))
        for y in range(preview.top + 28, preview.bottom, 58):
            pygame.draw.line(self.screen, (23, 36, 58), (preview.left + 10, y), (preview.right - 10, y))

    def draw_arena(self) -> None:
        pygame.draw.rect(self.screen, (13, 22, 40), ARENA_RECT, border_radius=16)
        pygame.draw.rect(self.screen, COLORS["border"], ARENA_RECT, 2, border_radius=16)

        for x in range(ARENA_RECT.left + 40, ARENA_RECT.right, 40):
            pygame.draw.line(
                self.screen,
                (22, 34, 55),
                (x, ARENA_RECT.top),
                (x, ARENA_RECT.bottom),
                1,
            )
        for y in range(ARENA_RECT.top + 40, ARENA_RECT.bottom, 40):
            pygame.draw.line(
                self.screen,
                (22, 34, 55),
                (ARENA_RECT.left, y),
                (ARENA_RECT.right, y),
                1,
            )

        for wall in self.walls:
            wall.draw(self.screen)

from __future__ import annotations

from enum import Enum


class GameState(Enum):
    GAME_INTRO = "GAME_INTRO"
    TITLE = "TITLE"
    ROUND_SETUP = "ROUND_SETUP"
    ROLE_REVEAL = "ROLE_REVEAL"
    KILLER_SKIN_SELECT = "KILLER_SKIN_SELECT"
    KILLER_INTRO = "KILLER_INTRO"
    PLAYING = "PLAYING"
    SCORE_SCREEN = "SCORE_SCREEN"
    GAME_OVER = "GAME_OVER"

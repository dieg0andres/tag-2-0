from __future__ import annotations

from enum import Enum


class GameState(Enum):
    TITLE = "TITLE"
    ROUND_SETUP = "ROUND_SETUP"
    ROLE_REVEAL = "ROLE_REVEAL"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"

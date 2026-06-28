from __future__ import annotations

from enum import Enum


class GameState(Enum):
    TITLE = "TITLE"
    ROUND_SETUP = "ROUND_SETUP"
    ROLE_REVEAL = "ROLE_REVEAL"
    KILLER_SKIN_SELECT = "KILLER_SKIN_SELECT"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"

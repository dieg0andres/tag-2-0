from __future__ import annotations

import pygame

from tag.core.state import GameState
from tag.ui.hud import HudMixin
from tag.ui.screens.game_over import GameOverScreenMixin
from tag.ui.screens.gameplay import GameplayScreenMixin
from tag.ui.screens.role_reveal import RoleRevealScreenMixin
from tag.ui.screens.setup import SetupScreenMixin
from tag.ui.screens.skin_select import SkinSelectScreenMixin
from tag.ui.screens.title import TitleScreenMixin


class UIMixin(
    TitleScreenMixin,
    SetupScreenMixin,
    RoleRevealScreenMixin,
    SkinSelectScreenMixin,
    GameplayScreenMixin,
    HudMixin,
    GameOverScreenMixin,
):
    def draw(self) -> None:
        if self.state == GameState.GAME_INTRO:
            self.draw_game_intro()
        elif self.state == GameState.TITLE:
            self.draw_title()
        elif self.state == GameState.ROUND_SETUP:
            self.draw_round_setup()
        elif self.state == GameState.ROLE_REVEAL:
            self.draw_role_reveal()
        elif self.state == GameState.KILLER_SKIN_SELECT:
            self.draw_killer_skin_select()
        elif self.state == GameState.KILLER_INTRO:
            self.draw_killer_intro()
        elif self.state == GameState.PLAYING:
            self.draw_gameplay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

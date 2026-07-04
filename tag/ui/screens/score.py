from __future__ import annotations

import pygame

from tag.ui.theme import COLORS, draw_cinematic_background, draw_panel, draw_vignette
from tag.utils.text import draw_text, draw_wrapped_text


class ScoreScreenMixin:
    def draw_score_screen(self) -> None:
        draw_cinematic_background(self.screen)
        self.draw_arena_preview()
        draw_vignette(self.screen, 115)

        center_x = self.window_center_x()
        width, height = self.screen.get_size()
        panel = pygame.Rect(0, 0, min(760, width - 80), min(430, height - 100))
        panel.center = (center_x, height // 2)
        draw_panel(self.screen, panel, fill=(12, 18, 34), border=COLORS["success"], radius=26, width=2, glow=COLORS["success"])

        draw_text(self.screen, self.font_large, "ROUND WON", COLORS["success"], (center_x, panel.top + 78), True)
        draw_wrapped_text(
            self.screen,
            self.font_medium,
            self.end_reason,
            COLORS["text_soft"],
            pygame.Rect(panel.left + 52, panel.top + 126, panel.width - 104, 70),
            4,
        )
        draw_text(self.screen, self.font_title, f"Score: {self.score}", COLORS["gold"], (center_x, panel.top + 230), True)
        draw_text(
            self.screen,
            self.font_small,
            "Continue to reroll your role for one more round, or quit with your current score.",
            COLORS["muted"],
            (center_x, panel.top + 296),
            True,
        )

        self.menu_buttons["continue"].draw(self.screen, self.font_medium, True)
        self.menu_buttons["quit_run"].draw(self.screen, self.font_medium, False)

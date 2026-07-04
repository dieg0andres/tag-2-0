from __future__ import annotations

import pygame

from tag.ui.theme import COLORS, draw_cinematic_background, draw_panel, draw_vignette
from tag.utils.text import draw_text, draw_wrapped_text


class GameOverScreenMixin:
    def draw_game_over(self) -> None:
        draw_cinematic_background(self.screen)
        self.draw_arena_preview()
        draw_vignette(self.screen, 120)

        result = "RUN COMPLETE" if self.player_won else "YOU LOSE"
        color = COLORS["success"] if self.player_won else COLORS["danger"]
        center_x = self.window_center_x()
        width, height = self.screen.get_size()
        panel = pygame.Rect(0, 0, min(760, width - 80), min(390, height - 100))
        panel.center = (center_x, height // 2)
        draw_panel(self.screen, panel, fill=(12, 18, 34), border=color, radius=26, width=2, glow=color)
        draw_text(self.screen, self.font_title, result, color, (center_x, panel.top + 88), True)
        draw_wrapped_text(
            self.screen,
            self.font_medium,
            self.end_reason,
            COLORS["text_soft"],
            pygame.Rect(panel.left + 48, panel.top + 140, panel.width - 96, 70),
            4,
        )
        draw_text(
            self.screen,
            self.font_large,
            f"Final Score: {self.final_score}",
            COLORS["gold"],
            (center_x, panel.top + 210),
            True,
        )
        skin_text = self.skin_progress_text()
        draw_wrapped_text(
            self.screen,
            self.font_small,
            skin_text,
            COLORS["gold"],
            pygame.Rect(panel.left + 58, panel.top + 270, panel.width - 116, 44),
            3,
        )
        if self.skin_notice:
            draw_wrapped_text(
                self.screen,
                self.font_small,
                self.skin_notice,
                COLORS["success"],
                pygame.Rect(panel.left + 58, panel.top + 315, panel.width - 116, 36),
                3,
            )
        draw_text(
            self.screen,
            self.font_small,
            "Press R to restart from the title screen. Press Escape to quit.",
            COLORS["muted"],
            (center_x, panel.bottom - 48),
            True,
        )

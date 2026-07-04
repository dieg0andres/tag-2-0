from __future__ import annotations

import pygame

from tag.config.settings import HIGH_SCORE_MESSAGE_LIMIT, HIGH_SCORE_NAME_LIMIT
from tag.ui.theme import COLORS, draw_cinematic_background, draw_panel, draw_vignette
from tag.utils.text import draw_text, ellipsize


class HighScoreScreenMixin:
    def draw_high_score_entry(self) -> None:
        draw_cinematic_background(self.screen)
        self.draw_arena_preview()
        draw_vignette(self.screen, 120)

        center_x = self.window_center_x()
        width, height = self.screen.get_size()
        panel = pygame.Rect(0, 0, min(820, width - 80), min(540, height - 80))
        panel.center = (center_x, height // 2)
        draw_panel(self.screen, panel, fill=(12, 18, 34), border=COLORS["gold"], radius=26, width=2, glow=COLORS["gold"])

        draw_text(self.screen, self.font_large, "NEW HIGH SCORE", COLORS["gold"], (center_x, panel.top + 62), True)
        draw_text(self.screen, self.font_title, str(self.final_score), COLORS["text"], (center_x, panel.top + 132), True)
        draw_text(
            self.screen,
            self.font_small,
            "Enter your name and an optional message, or skip without saving this score.",
            COLORS["text_soft"],
            (center_x, panel.top + 190),
            True,
        )

        field_width = min(560, panel.width - 120)
        self.high_score_name_rect = pygame.Rect(0, 0, field_width, 48)
        self.high_score_name_rect.center = (center_x, panel.top + 262)
        self.high_score_message_rect = pygame.Rect(0, 0, field_width, 48)
        self.high_score_message_rect.center = (center_x, panel.top + 350)

        self.draw_high_score_input_field(
            self.high_score_name_rect,
            "Name",
            self.high_score_name,
            HIGH_SCORE_NAME_LIMIT,
            self.high_score_active_field == "name",
        )
        self.draw_high_score_input_field(
            self.high_score_message_rect,
            "Message",
            self.high_score_message,
            HIGH_SCORE_MESSAGE_LIMIT,
            self.high_score_active_field == "message",
        )

        self.menu_buttons["submit_high_score"].draw(self.screen, self.font_medium, True)
        self.menu_buttons["skip_high_score"].draw(self.screen, self.font_medium, False)

    def draw_high_score_input_field(
        self,
        rect: pygame.Rect,
        label: str,
        value: str,
        limit: int,
        active: bool,
    ) -> None:
        label_text = f"{label} ({len(value)}/{limit})"
        draw_text(self.screen, self.font_small, label_text, COLORS["muted"], (rect.left, rect.top - 26))
        border = COLORS["primary_light"] if active else COLORS["border"]
        fill = COLORS["surface_2"] if active else COLORS["surface"]
        draw_panel(self.screen, rect, fill=fill, border=border, radius=14, width=2)
        display_value = value if value else f"{label}..."
        color = COLORS["text"] if value else COLORS["muted"]
        draw_text(
            self.screen,
            self.font_medium,
            ellipsize(self.font_medium, display_value, rect.width - 32),
            color,
            (rect.left + 16, rect.centery - self.font_medium.get_height() // 2),
        )

    def draw_high_score_board(self) -> None:
        draw_cinematic_background(self.screen)
        self.draw_arena_preview()
        draw_vignette(self.screen, 120)

        center_x = self.window_center_x()
        width, height = self.screen.get_size()
        panel = pygame.Rect(0, 0, min(920, width - 80), min(600, height - 80))
        panel.center = (center_x, height // 2)
        draw_panel(self.screen, panel, fill=(12, 18, 34), border=COLORS["primary"], radius=26, width=2, glow=COLORS["primary"])

        draw_text(self.screen, self.font_large, "HIGH SCORES", COLORS["text"], (center_x, panel.top + 54), True)
        source = getattr(self, "leaderboard_source", "local")
        pending_sync = hasattr(self, "leaderboard_task_pending") and self.leaderboard_task_pending()
        if source == "online":
            subtitle = "Top 10 online scores"
        elif pending_sync:
            subtitle = "Top 10 local fallback scores - syncing online"
        else:
            subtitle = "Top 10 local fallback scores"
        draw_text(self.screen, self.font_small, subtitle, COLORS["muted"], (center_x, panel.top + 100), True)
        if self.high_score_notice:
            draw_text(self.screen, self.font_small, self.high_score_notice, COLORS["success"], (center_x, panel.top + 124), True)

        if not self.high_scores:
            draw_text(self.screen, self.font_medium, "No high scores yet.", COLORS["text_soft"], (center_x, panel.centery), True)
        else:
            header_y = panel.top + 150
            draw_text(self.screen, self.font_small, "Rank", COLORS["muted"], (panel.left + 42, header_y))
            draw_text(self.screen, self.font_small, "Date", COLORS["muted"], (panel.left + 104, header_y))
            draw_text(self.screen, self.font_small, "Name", COLORS["muted"], (panel.left + 230, header_y))
            draw_text(self.screen, self.font_small, "Score", COLORS["muted"], (panel.left + 454, header_y))
            draw_text(self.screen, self.font_small, "Message", COLORS["muted"], (panel.left + 548, header_y))

            row_y = header_y + 34
            row_height = 34
            for index, entry in enumerate(self.high_scores[:10], start=1):
                if row_y + row_height > panel.bottom - 88:
                    break
                row_rect = pygame.Rect(panel.left + 32, row_y - 5, panel.width - 64, row_height)
                row_fill = COLORS["surface_2"] if index % 2 else COLORS["surface"]
                pygame.draw.rect(self.screen, row_fill, row_rect, border_radius=10)
                draw_text(self.screen, self.font_small, str(index), COLORS["gold"], (panel.left + 48, row_y))
                draw_text(self.screen, self.font_small, str(entry.get("date", "")), COLORS["text_soft"], (panel.left + 104, row_y))
                draw_text(
                    self.screen,
                    self.font_small,
                    ellipsize(self.font_small, str(entry.get("name", "")), 190),
                    COLORS["text"],
                    (panel.left + 230, row_y),
                )
                draw_text(self.screen, self.font_small, str(entry.get("score", 0)), COLORS["success"], (panel.left + 454, row_y))
                draw_text(
                    self.screen,
                    self.font_small,
                    ellipsize(self.font_small, str(entry.get("message", "")), panel.width - 600),
                    COLORS["text_soft"],
                    (panel.left + 548, row_y),
                )
                row_y += row_height + 4

        self.menu_buttons["title"].draw(self.screen, self.font_medium, True)

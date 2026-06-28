from __future__ import annotations

import pygame

from tag.ui.theme import COLORS, draw_cinematic_background, draw_panel, draw_pill, draw_vignette
from tag.utils.text import draw_text


class TitleScreenMixin:
    def draw_title(self) -> None:
        draw_cinematic_background(self.screen)
        self.draw_arena_preview()
        draw_vignette(self.screen, 115)

        width, height = self.screen.get_size()
        center_x = self.window_center_x()
        hero = pygame.Rect(0, 0, min(860, width - 72), min(600, height - 96))
        hero.center = (center_x, height // 2)
        draw_panel(self.screen, hero, fill=(12, 18, 34), border=COLORS["border"], radius=26, width=2, glow=COLORS["primary"])

        edge_inset = 48
        badge_y = hero.top + edge_inset
        chip_height = self.font_small.get_height() + 12
        chip_y = hero.bottom - edge_inset - chip_height // 2
        title_to_tagline = 70
        tagline_to_start = max(78, hero.height // 7)

        badge_rect = draw_pill(
            self.screen,
            self.font_small,
            "ARCADE SURVIVAL TAG",
            (hero.centerx, badge_y),
            fg=COLORS["primary_light"],
            bg=(16, 32, 58),
            border=(37, 99, 235),
            center=True,
        )
        cluster_height = (
            self.font_title.get_height() // 2
            + title_to_tagline
            + tagline_to_start
            + self.menu_buttons["play"].rect.height // 2
        )
        balanced_gap = max(18, (chip_y - badge_rect.bottom - cluster_height) // 2)
        title_y = badge_rect.bottom + balanced_gap + self.font_title.get_height() // 2
        tagline_y = title_y + title_to_tagline
        start_y = tagline_y + tagline_to_start

        draw_text(self.screen, self.font_title, "Tag 2.0", COLORS["text"], (center_x, title_y), True)
        draw_text(
            self.screen,
            self.font_medium,
            "Run, hunt, survive.",
            COLORS["text_soft"],
            (center_x, tagline_y),
            True,
        )
        self.menu_buttons["play"].rect.center = (center_x, start_y)

        chips = [("WASD / Arrows", "Move"), ("Space", "Attack"), ("Esc", "Quit")]
        total_chip_width = 0
        chip_sizes: list[tuple[str, str, int]] = []
        for key, label in chips:
            text = f"{key}  {label}"
            width_hint = self.font_small.size(text)[0] + 24
            chip_sizes.append((key, label, width_hint))
            total_chip_width += width_hint
        total_chip_width += 12 * (len(chips) - 1)
        chip_x = center_x - total_chip_width // 2
        for key, label, width_hint in chip_sizes:
            rect = draw_pill(
                self.screen,
                self.font_small,
                f"{key}  {label}",
                (chip_x, chip_y),
                fg=COLORS["text_soft"],
                bg=(18, 27, 46),
                border=COLORS["border_soft"],
            )
            chip_x += width_hint + 12

        self.menu_buttons["play"].draw(self.screen, self.font_medium, True)

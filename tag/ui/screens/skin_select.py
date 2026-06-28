from __future__ import annotations

import pygame

from tag.data.content import KILLERS
from tag.ui.theme import COLORS, draw_cinematic_background, draw_panel, draw_pill, draw_vignette
from tag.utils.text import draw_text, draw_wrapped_text, draw_wrapped_text_left, ellipsize


class SkinSelectScreenMixin:
    def draw_skin_selection(self) -> None:
        options = self.visible_skin_options_for_killer(self.round_killer)
        rects = [self.skin_card_rect(index) for index in range(len(options))]
        if not rects:
            return
        bounds = rects[0].unionall(rects[1:]) if len(rects) > 1 else rects[0]

        for index, skin_id in enumerate(options):
            rect = rects[index]
            selected = self.selected_skins.get(self.round_killer, "classic") == skin_id
            unlocked = skin_id == "classic" or self.skin_unlocked(skin_id)
            accent = COLORS["gold"] if unlocked else COLORS["warning"]
            draw_panel(
                self.screen,
                rect,
                fill=(28, 30, 24) if unlocked else (25, 25, 32),
                border=accent if selected else COLORS["border_soft"],
                radius=16,
                width=2 if selected else 1,
                glow=accent if selected else None,
            )

            sprite_key = self.skin_sprite_key(self.round_killer, skin_id)
            sprite = self.sprites.get(sprite_key)
            preview_rect = pygame.Rect(rect.left + 12, rect.centery - 26, 52, 52)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, KILLERS[self.round_killer]["color"], preview_rect)

            draw_text(
                self.screen,
                self.font_small,
                ellipsize(self.font_small, self.skin_name(self.round_killer, skin_id), rect.width - 84),
                COLORS["text"] if unlocked else COLORS["muted"],
                (rect.left + 76, rect.top + 12),
            )

            status = "Unlocked" if unlocked else f"Locked: {self.skin_challenge_text(skin_id)}"
            draw_wrapped_text_left(
                self.screen,
                self.font_small,
                status,
                COLORS["success"] if unlocked else COLORS["gold"],
                pygame.Rect(rect.left + 76, rect.top + 36, rect.width - 88, rect.height - 44),
                2,
                max_lines=2,
            )

        if self.skin_notice:
            notice_bottom = min(self.menu_buttons["begin"].rect.top - 8, bounds.bottom + 42)
            draw_wrapped_text(
                self.screen,
                self.font_small,
                self.skin_notice,
                COLORS["text_soft"],
                pygame.Rect(bounds.left, bounds.bottom + 8, bounds.width, max(24, notice_bottom - bounds.bottom - 8)),
                3,
            )

    def draw_killer_skin_select(self) -> None:
        draw_cinematic_background(self.screen)
        draw_vignette(self.screen, 110)
        center_x = self.window_center_x()
        width, height = self.screen.get_size()
        selected = KILLERS[self.round_killer]

        header = pygame.Rect(0, 0, min(720, width - 80), 210 if height >= 700 else 190)
        header.centerx = center_x
        first_card = self.skin_card_rect(0)
        header.top = first_card.top - 34 - header.height
        draw_panel(self.screen, header, fill=(12, 18, 34), border=COLORS["gold"], radius=26, width=2, glow=COLORS["gold"])
        draw_pill(
            self.screen,
            self.font_small,
            "KILLER LOADOUT",
            (center_x, header.top + 34),
            fg=COLORS["text"],
            bg=(38, 31, 19),
            border=(95, 72, 25),
            center=True,
        )
        draw_text(self.screen, self.font_large, selected["name"], COLORS["text"], (center_x, header.top + 103), True)

        self.menu_buttons["back"].draw(self.screen, self.font_small, False)
        self.menu_buttons["begin"].text = "Begin Round"
        self.draw_skin_selection()
        self.menu_buttons["begin"].draw(self.screen, self.font_medium, True)

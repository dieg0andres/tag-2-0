from __future__ import annotations

import pygame

from tag.data.content import KILLER_IDS, KILLERS
from tag.ui.theme import COLORS, draw_cinematic_background, draw_panel, draw_pill, draw_vignette
from tag.utils.text import draw_text, draw_wrapped_text, ellipsize


class SetupScreenMixin:
    def draw_round_setup(self) -> None:
        draw_cinematic_background(self.screen)
        draw_vignette(self.screen, 95)
        center_x = self.window_center_x()
        width = self.window_width()
        draw_text(
            self.screen,
            self.font_large,
            "Choose Your Hunter",
            COLORS["text"],
            (center_x, 66),
            True,
        )
        draw_wrapped_text(
            self.screen,
            self.font_small,
            "Choose your killer if your random role is Killer. Survivor rounds still use a random AI killer.",
            COLORS["text_soft"],
            pygame.Rect(center_x - min(430, width // 2 - 40), 104, min(860, width - 80), 44),
            4,
        )

        card_bottom = 0
        for index, killer_id in enumerate(KILLER_IDS):
            data = KILLERS[killer_id]
            panel = self.killer_card_rect(index)
            is_selected = killer_id == self.selected_player_killer
            accent = data.get("accent", COLORS["primary"])
            draw_panel(
                self.screen,
                panel,
                fill=(18, 27, 46) if is_selected else (13, 20, 36),
                border=accent if is_selected else COLORS["border_soft"],
                radius=20,
                width=2 if is_selected else 1,
                glow=accent if is_selected else None,
            )
            draw_pill(
                self.screen,
                self.font_small,
                str(index + 1),
                (panel.left + 13, panel.top + 10),
                fg=COLORS["text"],
                bg=accent if is_selected else COLORS["surface_2"],
                border=accent if is_selected else COLORS["border_soft"],
            )

            sprite = self.sprites.get(killer_id)
            preview_size = min(104, panel.width - 42, panel.height // 3)
            preview_rect = pygame.Rect(0, 0, preview_size, preview_size)
            preview_rect.center = (panel.centerx, panel.top + 68)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, data["color"], preview_rect)

            name = ellipsize(self.font_small, data["name"], panel.width - 30)
            draw_text(
                self.screen,
                self.font_small,
                name,
                COLORS["text"],
                (panel.left + 16, panel.top + 130),
            )
            draw_pill(
                self.screen,
                self.font_small,
                data["attack_name"],
                (panel.left + 14, panel.top + 158),
                fg=COLORS["gold"],
                bg=(38, 31, 19),
                border=(95, 72, 25),
            )
            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["description"],
                COLORS["muted"],
                pygame.Rect(panel.left + 16, panel.top + 198, panel.width - 32, panel.bottom - panel.top - 212),
                3,
            )
            card_bottom = max(card_bottom, panel.bottom)

        selected_name = KILLERS[self.selected_player_killer]["name"]
        draw_pill(
            self.screen,
            self.font_small,
            f"Selected killer if you become Killer: {selected_name}",
            (center_x, card_bottom + 18),
            fg=COLORS["gold"],
            bg=(34, 27, 16),
            border=(120, 86, 26),
            center=True,
        )
        self.menu_buttons["reveal"].draw(self.screen, self.font_medium, True)
        draw_text(
            self.screen,
            self.font_small,
            "Click a killer or press 1-5. Skin selection appears after you become Killer.",
            COLORS["muted"],
            (center_x, self.menu_buttons["reveal"].rect.bottom + 18),
            True,
        )

from __future__ import annotations

import math

import pygame

from tag.data.content import KILLER_IDS, KILLERS, SURVIVOR_IDS, SURVIVORS
from tag.ui.theme import COLORS, draw_cinematic_background, draw_panel, draw_pill, draw_vignette
from tag.utils.text import draw_text, ellipsize


ROLE_REVEAL_DANCE_KEYS = {
    "revenge_bot",
    "subslasher",
    "show_runner",
    "malice",
    "vengance_bot",
    "survivor",
    "survivor_odd",
    "survivor_explorer",
    "survivor_kitty",
    "survivor_kevin",
    "survivor_trashy",
    "survivor_queen_goopy",
}


class RoleRevealScreenMixin:
    def draw_role_reveal(self) -> None:
        draw_cinematic_background(self.screen)
        draw_vignette(self.screen, 110)
        selected = KILLERS[self.round_killer if self.player_role == "Survivor" else self.selected_player_killer]
        role_color = COLORS["primary"] if self.player_role == "Survivor" else COLORS["danger"]
        center_x = self.window_center_x()
        width, height = self.screen.get_size()

        reveal = pygame.Rect(0, 0, min(720, width - 80), 230 if height >= 700 else 210)
        reveal.centerx = center_x
        if self.player_role == "Killer":
            first_card = self.killer_card_rect(0)
            reveal.top = first_card.top - 34 - reveal.height
        else:
            first_card = self.survivor_card_rect(0)
            reveal.top = first_card.top - 34 - reveal.height
        draw_panel(self.screen, reveal, fill=(12, 18, 34), border=role_color, radius=26, width=2, glow=role_color)
        draw_pill(
            self.screen,
            self.font_small,
            "ROLE ASSIGNED",
            (center_x, reveal.top + 34),
            fg=COLORS["text"],
            bg=(23, 37, 66),
            border=role_color,
            center=True,
        )
        draw_text(self.screen, self.font_title, self.player_role, role_color, (center_x, reveal.top + 110), True)
        role_detail = (
            f"Round killer: {selected['name']}"
            if self.player_role == "Survivor"
            else f"Selected killer: {selected['name']}"
        )
        draw_pill(
            self.screen,
            self.font_small,
            role_detail,
            (center_x, reveal.top + 164),
            fg=COLORS["text_soft"],
            bg=(18, 27, 46),
            border=COLORS["border_soft"],
            center=True,
        )

        if self.player_role == "Killer":
            self.draw_killer_selection()
            self.menu_buttons["begin"].text = "Choose Skin" if self.selected_killer_has_skin_choices() else "Begin Round"
        else:
            self.draw_survivor_selection()
            self.menu_buttons["begin"].text = "Begin Round"
        self.menu_buttons["begin"].draw(self.screen, self.font_medium, True)

    def draw_role_reveal_card_preview(
        self,
        character_id: str,
        selected: bool,
        preview_rect: pygame.Rect,
        fallback_color: tuple[int, int, int],
        accent: tuple[int, int, int],
    ) -> None:
        if selected and character_id in ROLE_REVEAL_DANCE_KEYS:
            self.draw_role_reveal_dance_preview(character_id, preview_rect, fallback_color, accent)
            return

        sprite = self.sprites.get(character_id)
        if sprite is not None:
            preview = pygame.transform.smoothscale(sprite, preview_rect.size)
            self.screen.blit(preview, preview_rect)
        else:
            pygame.draw.ellipse(self.screen, fallback_color, preview_rect)

    def draw_role_reveal_dance_preview(
        self,
        character_id: str,
        preview_rect: pygame.Rect,
        fallback_color: tuple[int, int, int],
        accent: tuple[int, int, int],
    ) -> None:
        # This animation is intentionally separate from gameplay walking frames.
        # It builds a celebratory card-only pose from the existing sprite assets.
        ticks = pygame.time.get_ticks()
        t = ticks / 1000.0
        frames = self.walk_sprites.get(character_id, [])
        sprite = frames[(ticks // 110) % len(frames)] if frames else self.sprites.get(character_id)

        jump = max(0.0, math.sin(t * 8.5)) * 10
        sway = math.sin(t * 5.0) * 6
        spin = math.sin(t * 6.4) * 15 + math.sin(t * 11.0) * 3
        pulse = 1.0
        stage_pad = max(24, preview_rect.width // 3)
        stage = pygame.Surface(
            (preview_rect.width + stage_pad * 2, preview_rect.height + stage_pad * 2),
            pygame.SRCALPHA,
        )
        cx, cy = stage.get_width() // 2, stage.get_height() // 2
        size = min(preview_rect.width, preview_rect.height)

        shadow_rect = pygame.Rect(0, 0, int(size * 0.82), max(5, int(size * 0.13)))
        shadow_rect.center = (cx, cy + int(size * 0.48))
        pygame.draw.ellipse(stage, (0, 0, 0, 60), shadow_rect)

        for i in range(6):
            angle = t * 4.2 + i * math.tau / 6
            radius = size * (0.56 + 0.08 * math.sin(t * 3.0 + i))
            dot_x = cx + int(math.cos(angle) * radius)
            dot_y = cy + int(math.sin(angle) * radius * 0.58) - int(size * 0.08)
            sparkle_color = (255, 221, 93, 180) if i % 2 == 0 else (*accent[:3], 165)
            pygame.draw.circle(stage, sparkle_color, (dot_x, dot_y), 3 + (i % 2))

        if sprite is not None:
            base = pygame.transform.smoothscale(sprite, preview_rect.size)
            danced = pygame.transform.rotozoom(base, spin, pulse)
            danced_rect = danced.get_rect(center=(cx, cy - int(jump)))
            stage.blit(danced, danced_rect)
        else:
            fallback = pygame.Surface(preview_rect.size, pygame.SRCALPHA)
            pygame.draw.ellipse(fallback, (*fallback_color[:3], 255), fallback.get_rect())
            pygame.draw.ellipse(fallback, (*accent[:3], 255), fallback.get_rect(), 4)
            danced = pygame.transform.rotozoom(fallback, spin, pulse)
            danced_rect = danced.get_rect(center=(cx, cy - int(jump)))
            stage.blit(danced, danced_rect)

        stage_rect = stage.get_rect(center=(preview_rect.centerx + int(sway), preview_rect.centery))
        self.screen.blit(stage, stage_rect)

    def draw_survivor_selection(self) -> None:
        rects = [self.survivor_card_rect(index) for index in range(len(SURVIVOR_IDS))]
        if not rects:
            return

        for index, survivor_id in enumerate(SURVIVOR_IDS):
            data = SURVIVORS[survivor_id]
            rect = rects[index]
            selected = survivor_id == self.selected_player_survivor
            accent = COLORS["primary"]
            draw_panel(
                self.screen,
                rect,
                fill=(17, 31, 53) if selected else (13, 20, 36),
                border=accent if selected else COLORS["border_soft"],
                radius=16,
                width=2 if selected else 1,
                glow=accent if selected else None,
            )

            preview_size = min(72, rect.height - 50, rect.width // 3)
            preview_rect = pygame.Rect(0, 0, preview_size, preview_size)
            preview_rect.center = (rect.centerx, rect.centery - 18)
            self.draw_role_reveal_card_preview(survivor_id, selected, preview_rect, accent, accent)

            draw_text(
                self.screen,
                self.font_small,
                ellipsize(self.font_small, data["name"], rect.width - 24),
                COLORS["text"],
                (rect.centerx, preview_rect.bottom + 16),
                True,
            )

    def draw_killer_selection(self) -> None:
        rects = [self.killer_card_rect(index) for index in range(len(KILLER_IDS))]
        if not rects:
            return

        for index, killer_id in enumerate(KILLER_IDS):
            data = KILLERS[killer_id]
            rect = rects[index]
            selected = killer_id == self.selected_player_killer
            accent = data.get("accent", COLORS["primary"])
            draw_panel(
                self.screen,
                rect,
                fill=(18, 27, 46) if selected else (13, 20, 36),
                border=accent if selected else COLORS["border_soft"],
                radius=18,
                width=2 if selected else 1,
                glow=accent if selected else None,
            )
            draw_pill(
                self.screen,
                self.font_small,
                str(index + 1),
                (rect.left + 12, rect.top + 10),
                fg=COLORS["text"],
                bg=accent if selected else COLORS["surface_2"],
                border=accent if selected else COLORS["border_soft"],
            )

            preview_size = min(92, rect.width - 42, rect.height // 2)
            preview_rect = pygame.Rect(0, 0, preview_size, preview_size)
            preview_rect.center = (rect.centerx, rect.centery - 24)
            self.draw_role_reveal_card_preview(killer_id, selected, preview_rect, data["color"], accent)

            draw_pill(
                self.screen,
                self.font_small,
                ellipsize(self.font_small, data["name"], rect.width - 34),
                (rect.centerx, preview_rect.bottom + 22),
                fg=COLORS["text"],
                bg=accent if selected else COLORS["surface_2"],
                border=accent if selected else COLORS["border_soft"],
                center=True,
            )
            unlocked_count = len(self.unlocked_skin_options_for_killer(killer_id))
            total_count = len(self.skin_options_for_killer(killer_id))
            skin_text = f"{unlocked_count}/{total_count} unlocked"
            draw_text(
                self.screen,
                self.font_small,
                skin_text,
                COLORS["muted"],
                (rect.left + 14, rect.bottom - 28),
            )

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import pygame

from tag.config.settings import *
from tag.core.state import GameState
from tag.data.content import *
from tag.entities.objects import *
from tag.ui.theme import (
    COLORS,
    draw_cinematic_background,
    draw_divider,
    draw_panel,
    draw_pill,
    draw_progress_bar,
    draw_vignette,
)
from tag.utils.text import draw_text, draw_wrapped_text, draw_wrapped_text_left, ellipsize
from tag.utils.vector import facing_axis, safe_normalize, vector_from_keys


class UIMixin:
    def draw(self) -> None:
        if self.state == GameState.TITLE:
            self.draw_title()
        elif self.state == GameState.ROUND_SETUP:
            self.draw_round_setup()
        elif self.state == GameState.ROLE_REVEAL:
            self.draw_role_reveal()
        elif self.state == GameState.PLAYING:
            self.draw_gameplay()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

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

    def draw_role_reveal(self) -> None:
        draw_cinematic_background(self.screen)
        draw_vignette(self.screen, 110)
        selected = KILLERS[self.round_killer]
        role_color = COLORS["primary"] if self.player_role == "Survivor" else COLORS["danger"]
        center_x = self.window_center_x()
        width, height = self.screen.get_size()

        reveal = pygame.Rect(0, 0, min(720, width - 80), 230 if height >= 700 else 210)
        reveal.centerx = center_x
        reveal.top = 32
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
        draw_pill(
            self.screen,
            self.font_small,
            f"Round killer: {selected['name']}",
            (center_x, reveal.top + 164),
            fg=COLORS["text_soft"],
            bg=(18, 27, 46),
            border=COLORS["border_soft"],
            center=True,
        )

        if self.player_role == "Survivor":
            prompt = "Survive two 60-second lives while the random killer hunts you."
        else:
            prompt = "Catch the AI survivor with your selected killer before time runs out."
        draw_wrapped_text(
            self.screen,
            self.font_small,
            prompt,
            COLORS["text_soft"],
            pygame.Rect(reveal.left + 40, reveal.bottom - 38, reveal.width - 80, 28),
            3,
        )
        if self.player_role == "Killer":
            self.draw_skin_selection()
        else:
            self.draw_survivor_selection()
        self.menu_buttons["begin"].draw(self.screen, self.font_medium, True)

    def draw_survivor_selection(self) -> None:
        rects = [self.survivor_card_rect(index) for index in range(len(SURVIVOR_IDS))]
        if not rects:
            return
        bounds = rects[0].unionall(rects[1:]) if len(rects) > 1 else rects[0]
        draw_text(
            self.screen,
            self.font_medium,
            "Choose Survivor",
            COLORS["text"],
            (bounds.centerx, bounds.top - 30),
            True,
        )

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

            sprite = self.sprites.get(survivor_id)
            preview_rect = pygame.Rect(rect.left + 12, rect.centery - 26, 52, 52)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, accent, preview_rect)

            draw_text(
                self.screen,
                self.font_small,
                ellipsize(self.font_small, f"{index + 1}. {data['name']}", rect.width - 84),
                COLORS["text"],
                (rect.left + 76, rect.top + 12),
            )
            draw_wrapped_text_left(
                self.screen,
                self.font_small,
                data["description"],
                COLORS["muted"],
                pygame.Rect(rect.left + 76, rect.top + 36, rect.width - 88, rect.height - 44),
                2,
                max_lines=2,
            )

    def draw_skin_selection(self) -> None:
        options = self.skin_options_for_killer(self.round_killer)
        rects = [self.skin_card_rect(index) for index in range(len(options))]
        if not rects:
            return
        bounds = rects[0].unionall(rects[1:]) if len(rects) > 1 else rects[0]
        draw_text(
            self.screen,
            self.font_medium,
            "Choose Skin",
            COLORS["text"],
            (bounds.centerx, bounds.top - 30),
            True,
        )

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
                ellipsize(self.font_small, f"{index + 1}. {self.skin_name(self.round_killer, skin_id)}", rect.width - 84),
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

    def draw_gameplay(self) -> None:
        self.screen.fill((12, 19, 32))
        self.draw_arena()

        for hitbox in self.active_hitboxes:
            hitbox.draw(self.screen)

        for projectile in self.projectiles:
            projectile.draw(self.screen)

        for poop in self.malice_bird_poops:
            poop.draw(self.screen)

        for belt in self.ducky_belts:
            belt.draw(self.screen)

        for mine in self.landmines:
            mine.draw(self.screen)

        self.draw_survivor_ability_effects()

        for shot in self.survivor_shots:
            shot.draw(self.screen)

        for shockwave in self.trashy_shockwaves:
            shockwave.draw(self.screen)

        for turret in self.trashy_turrets:
            turret.draw(self.screen)

        for turret_shot in self.trashy_turret_shots:
            turret_shot.draw(self.screen)

        for knight in self.goopy_knights:
            knight.draw(self.screen)

        for bird in self.malice_helper_birds:
            bird.draw(self.screen)

        self.draw_dinosaur_shockwave()

        if self.survivor is not None:
            self.survivor.draw(self.screen, self.font_small)

        for killer in self.killers:
            if killer is not self.survivor:
                killer.draw(self.screen, self.font_small)

        self.draw_hud()
        self.draw_side_panel()
        self.draw_survivor_ability_ui()

    def draw_survivor_ability_effects(self) -> None:
        if not isinstance(self.player, Survivor):
            return

        survivor = self.player
        if survivor.kitty_marker is not None:
            pygame.draw.circle(
                self.screen,
                (59, 130, 246),
                (round(survivor.kitty_marker.x), round(survivor.kitty_marker.y)),
                KITTY_TELEPORT_MARKER_RADIUS,
                4,
            )
            pygame.draw.circle(
                self.screen,
                (191, 219, 254),
                (round(survivor.kitty_marker.x), round(survivor.kitty_marker.y)),
                8,
            )

        if self.survivor_flash_timer > 0:
            alpha = int(190 * (self.survivor_flash_timer / ODD_FLASH_VISUAL_DURATION))
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(
                overlay,
                (255, 255, 210, alpha),
                survivor.rect.center,
                220,
            )
            self.screen.blit(overlay, (0, 0))

        if survivor.explorer_adrenaline_timer > 0:
            pygame.draw.circle(self.screen, (34, 197, 94), survivor.rect.center, 39, 3)

        if self.explorer_taming_timer > 0:
            for killer in self.killers:
                pygame.draw.circle(self.screen, (45, 212, 191), killer.rect.center, 43, 3)

        if survivor.kevin_speed_timer > 0:
            angle = (pygame.time.get_ticks() * 0.6) % 360
            for offset in (0, 120, 240):
                direction = pygame.Vector2(1, 0).rotate(angle + offset)
                pygame.draw.line(
                    self.screen,
                    (96, 165, 250),
                    pygame.Vector2(survivor.rect.center) + direction * 24,
                    pygame.Vector2(survivor.rect.center) + direction * 38,
                    3,
                )

        if survivor.kevin_punch_timer > 0:
            hitbox = self.kevin_punch_hitbox(survivor)
            pygame.draw.rect(self.screen, (250, 204, 21), hitbox, 3, border_radius=8)

    def draw_survivor_ability_ui(self) -> None:
        if not isinstance(self.player, Survivor) or not self.player.trashy_minigame_active:
            return

        survivor = self.player
        shell = TRASHY_MINIGAME_BAR.inflate(38, 66)
        shell.centery = TRASHY_MINIGAME_BAR.centery - 3
        draw_panel(self.screen, shell, fill=(12, 18, 34), border=COLORS["primary"], radius=18, width=2, glow=COLORS["primary"])
        draw_text(
            self.screen,
            self.font_small,
            f"Gun Maker skill check  {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}",
            COLORS["text"],
            (shell.centerx, shell.top + 14),
            True,
        )
        pygame.draw.rect(self.screen, (23, 31, 49), TRASHY_MINIGAME_BAR, border_radius=12)
        pygame.draw.rect(self.screen, COLORS["border"], TRASHY_MINIGAME_BAR, 2, border_radius=12)
        target = survivor.trashy_target_rect()
        circle = survivor.trashy_circle_rect()
        pygame.draw.rect(self.screen, COLORS["success"], target, border_radius=6)
        pygame.draw.circle(self.screen, COLORS["text"], circle.center, TRASHY_MINIGAME_CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, COLORS["surface"], circle.center, TRASHY_MINIGAME_CIRCLE_RADIUS, 2)

    def draw_dinosaur_shockwave(self) -> None:
        if self.dinosaur_shockwave_timer <= 0:
            return

        elapsed_ratio = 1.0 - (
            self.dinosaur_shockwave_timer / MALICE_DINOSAUR_SHOCKWAVE_VISUAL_DURATION
        )
        radius = int(34 + MALICE_DINOSAUR_SHOCKWAVE_RADIUS * elapsed_ratio)
        alpha = int(190 * (self.dinosaur_shockwave_timer / MALICE_DINOSAUR_SHOCKWAVE_VISUAL_DURATION))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        center = (round(self.dinosaur_shockwave_pos.x), round(self.dinosaur_shockwave_pos.y))
        pygame.draw.circle(overlay, (248, 250, 252, alpha), center, radius, 5)
        pygame.draw.circle(overlay, (59, 130, 246, max(50, alpha // 2)), center, radius // 2, 2)
        self.screen.blit(overlay, (0, 0))

    def draw_panel_shell(self, rect: pygame.Rect, title: str) -> None:
        draw_panel(self.screen, rect, fill=COLORS["surface"], border=COLORS["border_soft"], radius=14, width=1)
        draw_text(self.screen, self.font_small, title.upper(), COLORS["muted"], (rect.left + 16, rect.top + 12))
        draw_divider(self.screen, rect, rect.top + 38)

    def draw_side_panel(self) -> None:
        pygame.draw.rect(self.screen, COLORS["bg_2"], SIDE_PANEL_RECT, border_radius=18)
        self.draw_timer_panel()
        self.draw_status_panel()
        self.draw_ability_guide_panel()
        self.draw_combat_panel()

    def draw_timer_panel(self) -> None:
        self.draw_panel_shell(TIMER_PANEL_RECT, "Time")
        number_y = TIMER_PANEL_RECT.centery + (10 if TIMER_PANEL_RECT.height < 150 else 4)
        draw_text(
            self.screen,
            self.font_large,
            f"{math.ceil(self.round_time):02d}",
            COLORS["text"],
            (TIMER_PANEL_RECT.centerx, number_y),
            True,
        )
        draw_text(
            self.screen,
            self.font_small,
            "seconds left",
            COLORS["muted"],
            (TIMER_PANEL_RECT.centerx, TIMER_PANEL_RECT.bottom - 24),
            True,
        )

    def gameplay_status_text(self) -> tuple[str, str]:
        if self.player_role == "Survivor":
            status = "Survive!"
            survivor_ability = self.survivor_ability_status()
            detail = (
                f"{self.survivor_status_message} | {survivor_ability}"
                if self.survivor_status_message
                else survivor_ability
            )
            return status, detail

        status = "Catch the survivor!"
        detail = "Space attacks"
        if isinstance(self.player, Killer):
            if self.player.is_ducky():
                detail = self.ducky_ability_status(self.player)
            elif self.player.is_malice():
                detail = self.malice_ability_status(self.player)
            elif self.player.is_subslasher():
                detail = self.subslasher_ability_status()
            elif self.player.is_show_runner():
                detail = self.show_runner_ability_status(self.player)
            elif self.player.is_vengance_bot():
                detail = self.vengance_ability_status(self.player)
        return status, detail

    def draw_status_panel(self) -> None:
        self.draw_panel_shell(STATUS_PANEL_RECT, "Objective")
        status, detail = self.gameplay_status_text()
        draw_pill(
            self.screen,
            self.font_small,
            status,
            (STATUS_PANEL_RECT.left + 16, STATUS_PANEL_RECT.top + 48),
            fg=COLORS["gold"],
            bg=(35, 28, 18),
            border=(112, 80, 25),
        )
        draw_wrapped_text_left(
            self.screen,
            self.font_small,
            detail,
            COLORS["text_soft"],
            pygame.Rect(
                STATUS_PANEL_RECT.left + 16,
                STATUS_PANEL_RECT.top + 84,
                STATUS_PANEL_RECT.width - 32,
                STATUS_PANEL_RECT.bottom - STATUS_PANEL_RECT.top - 96,
            ),
            2,
            max_lines=3,
        )

    def draw_combat_panel(self) -> None:
        self.draw_panel_shell(COMBAT_PANEL_RECT, "Action")
        if isinstance(self.player, Killer):
            draw_wrapped_text_left(
                self.screen,
                self.font_small,
                self.player.cooldown_status(),
                COLORS["text_soft"],
                pygame.Rect(COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 48, COMBAT_PANEL_RECT.width - 32, 30),
                2,
                max_lines=1,
            )
            bar = pygame.Rect(
                COMBAT_PANEL_RECT.left + 16,
                COMBAT_PANEL_RECT.top + 84,
                COMBAT_PANEL_RECT.width - 32,
                14,
            )
            self.draw_cooldown_bar(self.player, bar)
            draw_pill(
                self.screen,
                self.font_small,
                "Space: basic attack",
                (COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 108),
                fg=COLORS["muted"],
                bg=COLORS["surface_2"],
                border=COLORS["border_soft"],
            )
            return

        draw_wrapped_text_left(
            self.screen,
            self.font_small,
            self.survivor_ability_status(),
            COLORS["text_soft"],
            pygame.Rect(
                COMBAT_PANEL_RECT.left + 16,
                COMBAT_PANEL_RECT.top + 52,
                COMBAT_PANEL_RECT.width - 32,
                COMBAT_PANEL_RECT.height - 60,
            ),
            3,
            max_lines=4,
        )

    def draw_ability_guide_panel(self) -> None:
        lines = self.ability_guide_lines()
        self.draw_panel_shell(ABILITY_PANEL_RECT, "Abilities")

        if not lines:
            draw_text(
                self.screen,
                self.font_small,
                "No abilities yet.",
                COLORS["muted"],
                (ABILITY_PANEL_RECT.left + 16, ABILITY_PANEL_RECT.top + 46),
            )
            return

        y = ABILITY_PANEL_RECT.top + 45
        content_rect = pygame.Rect(
            ABILITY_PANEL_RECT.left + 16,
            y,
            ABILITY_PANEL_RECT.width - 32,
            ABILITY_PANEL_RECT.bottom - y - 14,
        )
        row_gap = 8
        hidden = 0
        for line in lines:
            if y + 34 > content_rect.bottom:
                hidden += 1
                continue
            row = pygame.Rect(content_rect.left, y, content_rect.width, 34)
            pygame.draw.rect(self.screen, COLORS["surface_2"], row, border_radius=10)
            pygame.draw.rect(self.screen, COLORS["border_soft"], row, 1, border_radius=10)
            if ":" in line:
                key, detail = line.split(":", 1)
                key_rect = draw_pill(
                    self.screen,
                    self.font_small,
                    key.strip(),
                    (row.left + 8, row.top + 5),
                    fg=COLORS["primary_light"],
                    bg=(17, 32, 56),
                    border=(37, 99, 235),
                )
                detail_x = key_rect.right + 8
                draw_text(
                    self.screen,
                    self.font_small,
                    ellipsize(self.font_small, detail.strip(), row.right - detail_x - 8),
                    COLORS["text_soft"],
                    (detail_x, row.top + 8),
                )
            else:
                draw_text(
                    self.screen,
                    self.font_small,
                    ellipsize(self.font_small, line, row.width - 18),
                    COLORS["text_soft"],
                    (row.left + 10, row.top + 8),
                )
            y += row.height + row_gap

        if hidden > 0 and y + self.font_small.get_height() <= content_rect.bottom:
            draw_text(
                self.screen,
                self.font_small,
                f"+ {hidden} more",
                COLORS["muted"],
                (content_rect.left + 8, y),
            )

    def ability_guide_lines(self) -> list[str]:
        if isinstance(self.player, Survivor):
            if self.player.survivor_id == "survivor_odd":
                return ["Move: WASD or arrows", "F: Picture Taken flash stuns killer 5s"]
            if self.player.survivor_id == "survivor_explorer":
                return ["Move: WASD or arrows", "A: Adrenaline invincible +60% speed", "A also Taming: killer 50% slower"]
            if self.player.survivor_id == "survivor_kitty":
                return ["Move: WASD or arrows", "L: place blue circle", "2: teleport to blue circle once"]
            if self.player.survivor_id == "survivor_queen_goopy":
                return ["Move: WASD or arrows", "K: summon 2 knights", "Knights stun killer 2.3s on touch"]
            if self.player.survivor_id == "survivor_trashy":
                return ["G: Gun Maker timing game / fire gun", "C: Shock Wave Cannon stuns and knocks back", "T: Devils Work turret, max 2", "Trashy abilities have 5s cooldowns"]
            if self.player.survivor_id == "survivor_kevin":
                return ["Move: WASD or arrows", "P: Punch in front for 5s", "S: Double Speed, +89% speed"]
            return ["Move: WASD or arrows", "Survive both lives until timer ends"]

        if not isinstance(self.player, Killer):
            return []

        if self.player.is_ducky():
            return ["Space: Lunge Swing attack", "C: Crying Swing belt/mace projectile", "Y: HG, Ducky faster and survivor slower"]
        if self.player.is_subslasher():
            return ["Space: Popsicle Sword Swing", "I: Perpelling Shootdown freeze spike", "E: Freezing Gun kill spike", "Q: Perpelling Subzero homing cubes"]
        if self.player.is_show_runner():
            return ["Space: Curtain Slash", "9: hahaha, slow survivor 50%", "U: script hook pulls survivor halfway", "A: shows power, +69% speed"]
        if self.player.is_vengance_bot():
            return ["Space: Vengance Lunge", "R: robot slash dash for 5s", "C: explosion landmine then teleport"]
        if self.player.is_malice_tiger():
            return ["Tiger form: +69% speed for Hunter's Rage", "Space: slash attack", "I: invisible 5s; survivor cannot see you", "Invisibility cooldown: 5s after visible"]
        if self.player.is_malice_bird():
            return ["Bird form: flies through walls", "I: summon 2 helper birds", "A: shoot white poop stun projectile", "Helpers slow survivor 50% on touch"]
        if self.player.is_malice_dinosaur():
            return ["Dinosaur form: 10% slower", "S: stomp shockwave; survivor dies in range", "R: dinosaur roar freezes survivor 16s", "Stomp and roar cooldown: 5s"]
        if self.player.is_malice():
            return ["Space: Malice Bite", "H: Hunter's Rage, random 20s form", "I: In Search For Bodies, pass through walls 4s"]

        return ["Space: attack", "Catch the survivor before time ends"]

    def draw_hud(self) -> None:
        width = self.window_width()
        pygame.draw.rect(self.screen, COLORS["bg"], pygame.Rect(0, 0, width, TOP_BAR_HEIGHT))
        pygame.draw.rect(self.screen, (10, 18, 34), pygame.Rect(14, 12, width - 28, TOP_BAR_HEIGHT - 24), border_radius=18)
        pygame.draw.line(self.screen, COLORS["border_soft"], (24, TOP_BAR_HEIGHT - 1), (width - 24, TOP_BAR_HEIGHT - 1), 1)
        selected = KILLERS[self.round_killer]
        draw_text(self.screen, self.font_medium, "Tag 2.0", COLORS["text"], (30, 16))

        cursor_x = 142
        role_color = COLORS["primary"] if self.player_role == "Survivor" else COLORS["danger"]
        role_pill = draw_pill(
            self.screen,
            self.font_small,
            self.player_role,
            (cursor_x, 19),
            fg=COLORS["text"],
            bg=(17, 32, 56) if self.player_role == "Survivor" else (55, 24, 32),
            border=role_color,
        )
        cursor_x = role_pill.right + 10
        killer_label = ellipsize(self.font_small, f"Killer: {selected['name']}", max(150, width // 5))
        killer_pill = draw_pill(
            self.screen,
            self.font_small,
            killer_label,
            (cursor_x, 19),
            fg=COLORS["text_soft"],
            bg=COLORS["surface_2"],
            border=COLORS["border_soft"],
        )
        cursor_x = killer_pill.right + 10
        if self.player_role == "Survivor":
            draw_pill(
                self.screen,
                self.font_small,
                f"Life {self.survivor_life_number}/{SURVIVOR_TOTAL_LIVES}",
                (cursor_x, 19),
                fg=COLORS["success"],
                bg=(17, 43, 34),
                border=(34, 197, 94),
            )

        controls = "WASD / Arrows move  |  Esc quits" if width >= 1080 else "Esc quits"
        controls_width = self.font_small.size(controls)[0] + 24
        draw_pill(
            self.screen,
            self.font_small,
            controls,
            (width - controls_width - 30, 19),
            fg=COLORS["muted"],
            bg=COLORS["surface"],
            border=COLORS["border_soft"],
        )

    def hud_role_text(self, killer_name: str) -> str:
        text = f"Role: {self.player_role}  |  Round killer: {killer_name}"
        if self.player_role == "Survivor":
            text += f"  |  Life: {self.survivor_life_number}/{SURVIVOR_TOTAL_LIVES}"
        return text

    def survivor_ability_status(self) -> str:
        if not isinstance(self.player, Survivor):
            return "WASD / Arrows move"

        survivor = self.player
        if survivor.survivor_id == "survivor_odd":
            if survivor.odd_flash_cooldown > 0:
                return f"F cooldown {survivor.odd_flash_cooldown:.1f}s"
            return "F Picture Taken"
        if survivor.survivor_id == "survivor_explorer":
            if survivor.explorer_adrenaline_timer > 0 or self.explorer_taming_timer > 0:
                return f"A ability {max(survivor.explorer_adrenaline_timer, self.explorer_taming_timer):.1f}s"
            if survivor.explorer_ability_cooldown > 0:
                return f"A cooldown {survivor.explorer_ability_cooldown:.1f}s"
            return "A Adrenaline + Taming"
        if survivor.survivor_id == "survivor_kitty":
            if survivor.kitty_marker is not None:
                return "2 teleport to blue circle"
            return "L place blue circle" if not survivor.kitty_teleport_used else "Teleport used"
        if survivor.survivor_id == "survivor_queen_goopy":
            if survivor.queen_knights_cooldown > 0:
                return f"K cooldown {survivor.queen_knights_cooldown:.1f}s"
            return "K Knights"
        if survivor.survivor_id == "survivor_trashy":
            if survivor.trashy_minigame_active:
                return f"Click overlap {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}"
            if survivor.trashy_gun_ready:
                gun = "G fire gun"
            else:
                gun = "G Gun Maker" if not survivor.trashy_gun_used else "Gun used"
            shock = (
                f"C cooldown {survivor.trashy_shock_cooldown:.1f}s"
                if survivor.trashy_shock_cooldown > 0
                else "C cannon"
            )
            turret = (
                f"T cooldown {survivor.trashy_turret_cooldown:.1f}s"
                if survivor.trashy_turret_cooldown > 0
                else f"T turret {len(self.trashy_turrets)}/{TRASHY_MAX_TURRETS}"
            )
            return f"{gun} | {shock} | {turret}"
        if survivor.survivor_id == "survivor_kevin":
            punch = "P punch"
            speed = "S speed" if not survivor.kevin_speed_used else "Speed used"
            if survivor.kevin_punch_timer > 0:
                punch = f"Punch {survivor.kevin_punch_timer:.1f}s"
            elif survivor.kevin_punch_cooldown > 0:
                punch = f"P cooldown {survivor.kevin_punch_cooldown:.1f}s"
            if survivor.kevin_speed_timer > 0:
                speed = f"Speed {survivor.kevin_speed_timer:.1f}s"
            return f"{punch} | {speed}"
        return "WASD / Arrows move"

    def malice_ability_status(self, malice: Killer) -> str:
        if malice.is_malice_tiger():
            invis = "I invisible"
            if malice.tiger_invisible_timer > 0:
                invis = f"Invisible {malice.tiger_invisible_timer:.1f}s"
            elif malice.tiger_invisible_cooldown > 0:
                invis = f"I cooldown {malice.tiger_invisible_cooldown:.1f}s"
            return f"Tiger {malice.malice_form_timer:.1f}s | {invis}"

        if malice.is_malice_bird():
            summon = "I helpers"
            poop = "A poop"
            if malice.bird_summon_cooldown > 0:
                summon = f"I cooldown {malice.bird_summon_cooldown:.1f}s"
            if malice.bird_poop_cooldown > 0:
                poop = f"A cooldown {malice.bird_poop_cooldown:.1f}s"
            return f"Bird {malice.malice_form_timer:.1f}s | {summon} | {poop}"

        if malice.is_malice_dinosaur():
            stomp = "S stomp"
            roar = "R roar"
            if malice.dinosaur_stomp_cooldown > 0:
                stomp = f"S cooldown {malice.dinosaur_stomp_cooldown:.1f}s"
            if malice.dinosaur_roar_cooldown > 0:
                roar = f"R cooldown {malice.dinosaur_roar_cooldown:.1f}s"
            return f"Dino {malice.malice_form_timer:.1f}s | {stomp} | {roar}"

        rage = "H: Hunter's Rage"
        if malice.malice_hunter_cooldown > 0:
            rage = f"H cooldown {malice.malice_hunter_cooldown:.1f}s"
        return f"{malice.wall_phase_status()} | {rage}"

    def subslasher_ability_status(self) -> str:
        if not isinstance(self.player, Killer):
            return "I freeze | E kill | Q cubes"

        freeze = "I freeze"
        kill = "E kill"
        cubes = "Q cubes"
        if self.survivor_stun_timer > 0:
            freeze = f"Frozen {self.survivor_stun_timer:.1f}s"
        elif self.player.subslasher_freeze_cooldown > 0:
            freeze = f"I cooldown {self.player.subslasher_freeze_cooldown:.1f}s"
        if self.player.subslasher_kill_cooldown > 0:
            kill = f"E cooldown {self.player.subslasher_kill_cooldown:.1f}s"
        if self.player.subslasher_subzero_cooldown > 0:
            cubes = f"Q cooldown {self.player.subslasher_subzero_cooldown:.1f}s"
        return f"{freeze} | {kill} | {cubes}"

    def ducky_ability_status(self, ducky: Killer) -> str:
        swing = "C swing"
        hg = "Y HG"
        if ducky.ducky_swing_cooldown > 0:
            swing = f"C cooldown {ducky.ducky_swing_cooldown:.1f}s"
        if ducky.ducky_hg_timer > 0:
            hg = f"HG {ducky.ducky_hg_timer:.1f}s"
        elif ducky.ducky_hg_cooldown > 0:
            hg = f"Y cooldown {ducky.ducky_hg_cooldown:.0f}s"
        return f"{swing} | {hg}"

    def show_runner_ability_status(self, show_runner: Killer) -> str:
        slow = "9 slow"
        hook = "U hook"
        speed = "A speed"
        if self.survivor_slow_timer > 0:
            slow = f"Slow {self.survivor_slow_timer:.1f}s"
        elif show_runner.show_slow_cooldown > 0:
            slow = f"9 cooldown {show_runner.show_slow_cooldown:.1f}s"
        if show_runner.show_hook_cooldown > 0:
            hook = f"U cooldown {show_runner.show_hook_cooldown:.1f}s"
        if show_runner.show_power_timer > 0:
            speed = f"Speed {show_runner.show_power_timer:.1f}s"
        elif show_runner.show_power_cooldown > 0:
            speed = f"A cooldown {show_runner.show_power_cooldown:.1f}s"
        return f"{slow} | {hook} | {speed}"

    def vengance_ability_status(self, vengance_bot: Killer) -> str:
        dash = "R dash"
        mine = "C mine"
        if vengance_bot.vengance_dash_timer > 0:
            dash = f"Dash {vengance_bot.vengance_dash_timer:.1f}s"
        elif vengance_bot.vengance_dash_cooldown > 0:
            dash = f"R cooldown {vengance_bot.vengance_dash_cooldown:.0f}s"
        if vengance_bot.vengance_mine_cooldown > 0:
            mine = f"C cooldown {vengance_bot.vengance_mine_cooldown:.0f}s"
        return f"{dash} | {mine}"

    def draw_cooldown_bar(self, killer: Killer, bar: pygame.Rect | None = None) -> None:
        if bar is None:
            bar = pygame.Rect(COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 78, 150, 16)

        if killer.attack_phase is not None:
            progress = 1.0
        elif killer.cooldown_remaining <= 0:
            progress = 1.0
        else:
            progress = 1.0 - (killer.cooldown_remaining / killer.data["cooldown"])

        draw_progress_bar(self.screen, bar, progress, fill=COLORS["success"])

    def draw_game_over(self) -> None:
        draw_cinematic_background(self.screen)
        self.draw_arena_preview()
        draw_vignette(self.screen, 120)

        result = "YOU WIN" if self.player_won else "YOU LOSE"
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
        skin_text = self.skin_progress_text()
        draw_wrapped_text(
            self.screen,
            self.font_small,
            skin_text,
            COLORS["gold"],
            pygame.Rect(panel.left + 58, panel.top + 220, panel.width - 116, 44),
            3,
        )
        if self.skin_notice:
            draw_wrapped_text(
                self.screen,
                self.font_small,
                self.skin_notice,
                COLORS["success"],
                pygame.Rect(panel.left + 58, panel.top + 265, panel.width - 116, 36),
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

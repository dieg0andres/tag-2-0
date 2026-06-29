from __future__ import annotations

import pygame

from tag.config.settings import (
    KITTY_TELEPORT_MARKER_RADIUS,
    LABEL_FADE_DURATION,
    LABEL_FULL_VISIBLE_DURATION,
    MALICE_DINOSAUR_SHOCKWAVE_RADIUS,
    MALICE_DINOSAUR_SHOCKWAVE_VISUAL_DURATION,
    ODD_FLASH_VISUAL_DURATION,
    ROUND_DURATION,
    TRASHY_GUN_TARGET_HITS,
    TRASHY_MINIGAME_BAR,
    TRASHY_MINIGAME_CIRCLE_RADIUS,
)
from tag.entities.objects import Survivor
from tag.ui.theme import COLORS, draw_panel
from tag.utils.text import draw_text


class GameplayScreenMixin:
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
        label_alpha = self.overhead_label_alpha()

        if self.survivor is not None:
            self.survivor.draw(self.screen, self.font_small, label_alpha)

        for killer in self.killers:
            if killer is not self.survivor:
                killer.draw(self.screen, self.font_small, label_alpha)

        self.draw_hud()
        self.draw_side_panel()
        self.draw_survivor_ability_ui()

    def overhead_label_alpha(self) -> int:
        elapsed = ROUND_DURATION - self.round_time
        if elapsed <= LABEL_FULL_VISIBLE_DURATION:
            return 255

        fade_elapsed = elapsed - LABEL_FULL_VISIBLE_DURATION
        if fade_elapsed >= LABEL_FADE_DURATION:
            return 0

        fade_progress = fade_elapsed / LABEL_FADE_DURATION
        return round(255 * (1.0 - fade_progress))

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
            f"Press Space on overlap  {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}",
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

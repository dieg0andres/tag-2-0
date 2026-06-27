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
from tag.utils.text import draw_text, draw_wrapped_text, draw_wrapped_text_left
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
        self.screen.fill((10, 16, 30))
        self.draw_arena_preview()
        center_x = self.window_center_x()
        draw_text(self.screen, self.font_title, "Tag 2.0", (248, 250, 252), (center_x, 160), True)
        draw_text(
            self.screen,
            self.font_medium,
            "Random role. Survive twice or catch.",
            (203, 213, 225),
            (center_x, 245),
            True,
        )
        draw_text(
            self.screen,
            self.font_small,
            "WASD / Arrows move  |  Space attacks as killer  |  Escape quits",
            (148, 163, 184),
            (center_x, 305),
            True,
        )
        self.menu_buttons["play"].draw(self.screen, self.font_medium, True)
        draw_text(
            self.screen,
            self.font_small,
            "Press Enter or click Start",
            (203, 213, 225),
            (center_x, self.menu_buttons["play"].rect.bottom + 20),
            True,
        )

    def draw_round_setup(self) -> None:
        self.screen.fill((13, 22, 36))
        center_x = self.window_center_x()
        draw_text(
            self.screen,
            self.font_large,
            "Round Setup",
            (248, 250, 252),
            (center_x, 78),
            True,
        )
        draw_text(
            self.screen,
            self.font_small,
            "Choose your killer if your random role is Killer. Survivor rounds still use a random AI killer.",
            (203, 213, 225),
            (center_x, 123),
            True,
        )

        for index, killer_id in enumerate(KILLER_IDS):
            data = KILLERS[killer_id]
            panel = self.killer_card_rect(index)
            is_selected = killer_id == self.selected_player_killer
            pygame.draw.rect(self.screen, (24, 34, 52), panel, border_radius=12)
            pygame.draw.rect(
                self.screen,
                (248, 199, 88) if is_selected else (77, 88, 106),
                panel,
                4 if is_selected else 3,
                border_radius=12,
            )
            draw_text(
                self.screen,
                self.font_small,
                str(index + 1),
                (248, 199, 88) if is_selected else (148, 163, 184),
                (panel.left + 13, panel.top + 10),
            )

            sprite = self.sprites.get(killer_id)
            preview_rect = pygame.Rect(0, 0, 82, 82)
            preview_rect.center = (panel.centerx, panel.top + 56)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, data["color"], preview_rect)

            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["name"],
                (248, 250, 252),
                pygame.Rect(panel.left + 10, panel.top + 106, panel.width - 20, 44),
            )
            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["attack_name"],
                (248, 199, 88),
                pygame.Rect(panel.left + 10, panel.top + 155, panel.width - 20, 48),
            )
            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["description"],
                (177, 188, 205),
                pygame.Rect(panel.left + 10, panel.top + 218, panel.width - 20, 58),
            )

        selected_name = KILLERS[self.selected_player_killer]["name"]
        draw_text(
            self.screen,
            self.font_small,
            f"Selected killer if you become Killer: {selected_name}",
            (248, 199, 88),
            (center_x, 492),
            True,
        )
        self.menu_buttons["reveal"].draw(self.screen, self.font_medium, True)
        draw_text(
            self.screen,
            self.font_small,
            "Click a killer or press 1-5. Skin selection appears after you become Killer.",
            (203, 213, 225),
            (center_x, self.menu_buttons["reveal"].rect.bottom + 18),
            True,
        )

    def draw_role_reveal(self) -> None:
        self.screen.fill((10, 16, 30))
        selected = KILLERS[self.round_killer]
        role_color = (96, 165, 250) if self.player_role == "Survivor" else (248, 113, 113)
        center_x = self.window_center_x()

        draw_text(self.screen, self.font_large, "Role Reveal", (248, 250, 252), (center_x, 125), True)
        draw_text(self.screen, self.font_title, self.player_role, role_color, (center_x, 240), True)
        draw_text(
            self.screen,
            self.font_medium,
            f"Round killer: {selected['name']}",
            (226, 232, 240),
            (center_x, 330),
            True,
        )

        if self.player_role == "Survivor":
            prompt = "Survive two 60-second lives while the random killer hunts you."
        else:
            prompt = "Catch the AI survivor with your selected killer before time runs out."
        draw_text(self.screen, self.font_medium, prompt, (203, 213, 225), (center_x, 380), True)
        if self.player_role == "Killer":
            self.draw_skin_selection()
        else:
            self.draw_survivor_selection()
        self.menu_buttons["begin"].draw(self.screen, self.font_medium, True)

    def draw_survivor_selection(self) -> None:
        center_x = self.window_center_x()
        draw_text(
            self.screen,
            self.font_medium,
            "Choose Survivor",
            (248, 250, 252),
            (center_x, 420),
            True,
        )

        for index, survivor_id in enumerate(SURVIVOR_IDS):
            data = SURVIVORS[survivor_id]
            rect = self.survivor_card_rect(index)
            selected = survivor_id == self.selected_player_survivor
            fill = (24, 41, 58)
            outline = (96, 165, 250) if selected else (88, 100, 116)
            pygame.draw.rect(self.screen, fill, rect, border_radius=8)
            pygame.draw.rect(self.screen, outline, rect, 3 if selected else 2, border_radius=8)

            sprite = self.sprites.get(survivor_id)
            preview_rect = pygame.Rect(rect.left + 8, rect.top + 13, 44, 44)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, (96, 165, 250), preview_rect)

            draw_text(
                self.screen,
                self.font_small,
                f"{index + 1}. {data['name']}",
                (248, 250, 252),
                (rect.left + 60, rect.top + 9),
            )
            draw_wrapped_text(
                self.screen,
                self.font_small,
                data["description"],
                (203, 213, 225),
                pygame.Rect(rect.left + 60, rect.top + 32, rect.width - 68, 30),
            )

    def draw_skin_selection(self) -> None:
        center_x = self.window_center_x()
        draw_text(
            self.screen,
            self.font_medium,
            "Choose Skin",
            (248, 250, 252),
            (center_x, 420),
            True,
        )

        for index, skin_id in enumerate(self.skin_options_for_killer(self.round_killer)):
            rect = self.skin_card_rect(index)
            selected = self.selected_skins.get(self.round_killer, "classic") == skin_id
            unlocked = skin_id == "classic" or self.skin_unlocked(skin_id)
            fill = (25, 42, 37) if unlocked else (35, 35, 42)
            outline = (248, 199, 88) if selected else (88, 100, 116)
            pygame.draw.rect(self.screen, fill, rect, border_radius=8)
            pygame.draw.rect(self.screen, outline, rect, 3 if selected else 2, border_radius=8)

            sprite_key = self.skin_sprite_key(self.round_killer, skin_id)
            sprite = self.sprites.get(sprite_key)
            preview_rect = pygame.Rect(rect.left + 8, rect.top + 13, 44, 44)
            if sprite is not None:
                preview = pygame.transform.smoothscale(sprite, preview_rect.size)
                self.screen.blit(preview, preview_rect)
            else:
                pygame.draw.ellipse(self.screen, KILLERS[self.round_killer]["color"], preview_rect)

            draw_text(
                self.screen,
                self.font_small,
                f"{index + 1}. {self.skin_name(self.round_killer, skin_id)}",
                (248, 250, 252) if unlocked else (148, 163, 184),
                (rect.left + 60, rect.top + 9),
            )

            status = "Unlocked" if unlocked else f"Locked: {self.skin_challenge_text(skin_id)}"
            draw_wrapped_text(
                self.screen,
                self.font_small,
                status,
                (134, 239, 172) if unlocked else (248, 199, 88),
                pygame.Rect(rect.left + 60, rect.top + 32, rect.width - 68, 30),
            )

        if self.skin_notice:
            draw_wrapped_text(
                self.screen,
                self.font_small,
                self.skin_notice,
                (203, 213, 225),
                pygame.Rect(center_x - 350, 582, 700, 36),
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
        pygame.draw.rect(self.screen, (127, 29, 29), TRASHY_MINIGAME_BAR, border_radius=10)
        pygame.draw.rect(self.screen, (254, 202, 202), TRASHY_MINIGAME_BAR, 2, border_radius=10)
        target = survivor.trashy_target_rect()
        circle = survivor.trashy_circle_rect()
        pygame.draw.rect(self.screen, (34, 197, 94), target, border_radius=4)
        pygame.draw.circle(self.screen, (248, 250, 252), circle.center, TRASHY_MINIGAME_CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, (15, 23, 42), circle.center, TRASHY_MINIGAME_CIRCLE_RADIUS, 2)
        draw_text(
            self.screen,
            self.font_small,
            f"Gun Maker {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}",
            (248, 250, 252),
            (TRASHY_MINIGAME_BAR.centerx, TRASHY_MINIGAME_BAR.top - 20),
            True,
        )

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
        pygame.draw.rect(self.screen, (12, 19, 32), rect, border_radius=PANEL_RADIUS)
        pygame.draw.rect(self.screen, (51, 65, 85), rect, 2, border_radius=PANEL_RADIUS)
        draw_text(self.screen, self.font_small, title, (248, 250, 252), (rect.left + 16, rect.top + 12))
        pygame.draw.line(
            self.screen,
            (51, 65, 85),
            (rect.left + 14, rect.top + 37),
            (rect.right - 14, rect.top + 37),
            1,
        )

    def draw_side_panel(self) -> None:
        pygame.draw.rect(self.screen, (8, 13, 24), SIDE_PANEL_RECT, border_radius=10)
        self.draw_timer_panel()
        self.draw_status_panel()
        self.draw_ability_guide_panel()
        self.draw_combat_panel()

    def draw_timer_panel(self) -> None:
        self.draw_panel_shell(TIMER_PANEL_RECT, "Time")
        draw_text(
            self.screen,
            self.font_large,
            f"{math.ceil(self.round_time):02d}",
            (248, 250, 252),
            (TIMER_PANEL_RECT.centerx, TIMER_PANEL_RECT.top + 73),
            True,
        )
        draw_text(
            self.screen,
            self.font_small,
            "seconds left",
            (148, 163, 184),
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
        self.draw_panel_shell(STATUS_PANEL_RECT, "Round Status")
        status, detail = self.gameplay_status_text()
        draw_text(
            self.screen,
            self.font_small,
            status,
            (248, 199, 88),
            (STATUS_PANEL_RECT.left + 16, STATUS_PANEL_RECT.top + 47),
        )
        draw_wrapped_text_left(
            self.screen,
            self.font_small,
            detail,
            (203, 213, 225),
            pygame.Rect(
                STATUS_PANEL_RECT.left + 16,
                STATUS_PANEL_RECT.top + 73,
                STATUS_PANEL_RECT.width - 32,
                STATUS_PANEL_RECT.bottom - STATUS_PANEL_RECT.top - 86,
            ),
            2,
        )

    def draw_combat_panel(self) -> None:
        self.draw_panel_shell(COMBAT_PANEL_RECT, "Action")
        if isinstance(self.player, Killer):
            draw_text(
                self.screen,
                self.font_small,
                self.player.cooldown_status(),
                (226, 232, 240),
                (COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 47),
            )
            bar = pygame.Rect(
                COMBAT_PANEL_RECT.left + 16,
                COMBAT_PANEL_RECT.top + 78,
                COMBAT_PANEL_RECT.width - 32,
                16,
            )
            self.draw_cooldown_bar(self.player, bar)
            draw_text(
                self.screen,
                self.font_small,
                "Space: basic attack",
                (148, 163, 184),
                (COMBAT_PANEL_RECT.left + 16, COMBAT_PANEL_RECT.top + 98),
            )
            return

        draw_wrapped_text_left(
            self.screen,
            self.font_small,
            self.survivor_ability_status(),
            (226, 232, 240),
            pygame.Rect(
                COMBAT_PANEL_RECT.left + 16,
                COMBAT_PANEL_RECT.top + 47,
                COMBAT_PANEL_RECT.width - 32,
                COMBAT_PANEL_RECT.height - 60,
            ),
            3,
        )

    def draw_ability_guide_panel(self) -> None:
        lines = self.ability_guide_lines()
        self.draw_panel_shell(ABILITY_PANEL_RECT, "Ability Guide")

        if not lines:
            draw_text(
                self.screen,
                self.font_small,
                "No abilities yet.",
                (148, 163, 184),
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
        for line in lines:
            y = draw_wrapped_text_left(
                self.screen,
                self.font_small,
                f"- {line}",
                (203, 213, 225),
                pygame.Rect(content_rect.left, y, content_rect.width, content_rect.bottom - y),
                2,
            )
            y += 7
            if y + self.font_small.get_height() > content_rect.bottom:
                break

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
        pygame.draw.rect(self.screen, (5, 10, 20), pygame.Rect(0, 0, width, TOP_BAR_HEIGHT))
        pygame.draw.line(self.screen, (51, 65, 85), (0, TOP_BAR_HEIGHT), (width, TOP_BAR_HEIGHT), 2)

        selected = KILLERS[self.round_killer]
        draw_text(self.screen, self.font_medium, "Tag 2.0", (248, 250, 252), (24, 14))
        draw_text(
            self.screen,
            self.font_small,
            self.hud_role_text(selected["name"]),
            (203, 213, 225),
            (24, 50),
        )
        draw_text(
            self.screen,
            self.font_small,
            "WASD / Arrows move  |  Escape quits" if width >= 1080 else "Esc quits",
            (148, 163, 184),
            (width - 420 if width >= 1080 else width - 100, 50),
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
        pygame.draw.rect(self.screen, (31, 41, 55), bar, border_radius=7)

        if killer.attack_phase is not None:
            progress = 1.0
        elif killer.cooldown_remaining <= 0:
            progress = 1.0
        else:
            progress = 1.0 - (killer.cooldown_remaining / killer.data["cooldown"])

        fill = bar.copy()
        fill.width = max(0, int(bar.width * progress))
        pygame.draw.rect(self.screen, (34, 197, 94), fill, border_radius=7)
        pygame.draw.rect(self.screen, (148, 163, 184), bar, 2, border_radius=7)

    def draw_game_over(self) -> None:
        self.screen.fill((10, 16, 30))
        self.draw_arena_preview()

        result = "YOU WIN" if self.player_won else "YOU LOSE"
        color = (74, 222, 128) if self.player_won else (248, 113, 113)
        center_x = self.window_center_x()
        draw_text(self.screen, self.font_title, result, color, (center_x, 160), True)
        draw_text(self.screen, self.font_medium, self.end_reason, (226, 232, 240), (center_x, 255), True)
        skin_text = self.skin_progress_text()
        draw_text(self.screen, self.font_small, skin_text, (248, 199, 88), (center_x, 292), True)
        if self.skin_notice:
            draw_text(self.screen, self.font_small, self.skin_notice, (134, 239, 172), (center_x, 320), True)
        draw_text(
            self.screen,
            self.font_small,
            "Press R to restart from the title screen. Press Escape to quit.",
            (203, 213, 225),
            (center_x, 355),
            True,
        )

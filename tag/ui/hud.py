from __future__ import annotations

import math

import pygame

from tag.config.settings import (
    ABILITY_PANEL_RECT,
    COMBAT_PANEL_RECT,
    SIDE_PANEL_RECT,
    STATUS_PANEL_RECT,
    SURVIVOR_TOTAL_LIVES,
    TIMER_PANEL_RECT,
    TOP_BAR_HEIGHT,
    TRASHY_GUN_TARGET_HITS,
    TRASHY_MAX_TURRETS,
)
from tag.data.content import KILLERS
from tag.entities.objects import Killer, Survivor
from tag.ui.theme import COLORS, draw_divider, draw_panel, draw_pill, draw_progress_bar
from tag.utils.text import draw_text, draw_wrapped_text_left, ellipsize
from tag.world.arena import ARENA_LAYOUTS


class HudMixin:
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
                return ["G: Gun Maker / homing gun", "Space: hit 3 Gun Maker overlaps", "Gun passes through walls and stuns", "C: Shock Wave Cannon; T: turret"]
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
        controls = "WASD / Arrows move  |  Esc quits" if width >= 1080 else "Esc quits"
        controls_width = self.font_small.size(controls)[0] + 24
        controls_left = width - controls_width - 30
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

        layout_id = getattr(self, "wall_layout_id", 0) or 0
        arena = ARENA_LAYOUTS[layout_id % len(ARENA_LAYOUTS)]
        arena_label = ellipsize(self.font_small, f"Arena: {arena['name']}", max(140, width // 6))
        arena_width = self.font_small.size(arena_label)[0] + 24
        life_label = f"Life {self.survivor_life_number}/{SURVIVOR_TOTAL_LIVES}" if self.player_role == "Survivor" else ""
        life_width = self.font_small.size(life_label)[0] + 24 if life_label else 0
        life_gap = 10 if life_label else 0
        if cursor_x + arena_width + life_gap + life_width <= controls_left - 10:
            arena_pill = draw_pill(
                self.screen,
                self.font_small,
                arena_label,
                (cursor_x, 19),
                fg=COLORS["text_soft"],
                bg=COLORS["surface_2"],
                border=COLORS["border_soft"],
            )
            cursor_x = arena_pill.right + 10

        if self.player_role == "Survivor":
            draw_pill(
                self.screen,
                self.font_small,
                life_label,
                (cursor_x, 19),
                fg=COLORS["success"],
                bg=(17, 43, 34),
                border=(34, 197, 94),
            )

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
                return f"Space overlap {survivor.trashy_hits}/{TRASHY_GUN_TARGET_HITS}"
            if survivor.trashy_gun_ready:
                gun = "G fire homing gun"
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

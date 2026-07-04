from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from datetime import date
import json
import math
import random
import sys
import time
from pathlib import Path

import pygame

from tag.config.settings import *
from tag.core.state import GameState
from tag.data.content import *
from tag.entities.objects import *
from tag.persistence.leaderboard_service import (
    LeaderboardSyncResult,
    clean_leaderboard_entry,
    refresh_online_scores,
    score_qualifies_for_entries,
    sorted_leaderboard_entries,
    startup_sync,
    submit_score_and_refresh,
)
from tag.utils.text import draw_text, draw_wrapped_text, draw_wrapped_text_left
from tag.utils.vector import facing_axis, safe_normalize, vector_from_keys


class PersistenceMixin:
    def load_save_data(self) -> dict[str, object]:
        default_data = {
            "total_wins": 0,
            "unlocked_skins": [],
            "challenge_progress": {
                "show_runner_wins": 0,
                "show_runner_kills": 0,
                "vengance_bot_wins": 0,
                "vengance_bot_survives": 0,
                "vengance_bot_low_mine_wins": 0,
                "ducky_losses": 0,
                "ducky_daddys_belt_wins": 0,
                "ducky_ogel_wins": 0,
                "malice_bird_form_wins": 0,
                "explorer_losses": 0,
                "malice_wins": 0,
            },
        }

        if not SAVE_FILE.exists():
            return default_data

        try:
            data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default_data

        wins = data.get("total_wins", 0)
        if not isinstance(wins, int):
            wins = 0

        unlocked = data.get("unlocked_skins", [])
        if not isinstance(unlocked, list):
            unlocked = []

        progress = data.get("challenge_progress", {})
        if not isinstance(progress, dict):
            progress = {}

        clean_progress = dict(default_data["challenge_progress"])
        for key, value in progress.items():
            if isinstance(key, str) and isinstance(value, int):
                clean_progress[key] = max(0, value)

        clean_unlocked = {skin_id for skin_id in unlocked if skin_id in SKINS}
        if wins >= FRIED_CHICKEN_UNLOCK_WINS:
            clean_unlocked.add("fried_chicken")
        show_runner_kills = clean_progress.get("show_runner_kills", 0)
        if show_runner_kills >= SHOW_RUNNER_MASTERY_1_KILLS:
            clean_unlocked.add("show_runner_mastery_1")
        if show_runner_kills >= SHOW_RUNNER_MASTERY_2_KILLS:
            clean_unlocked.add("show_runner_mastery_2")
        if show_runner_kills >= SHOW_RUNNER_MASTERY_3_KILLS:
            clean_unlocked.add("show_runner_mastery_3")
        vengance_bot_wins = clean_progress.get("vengance_bot_wins", 0)
        if vengance_bot_wins >= VENGANCE_BOT_MASTERY_1_WINS:
            clean_unlocked.add("vengance_bot_mastery_1")
        if vengance_bot_wins >= VENGANCE_BOT_MASTERY_2_WINS:
            clean_unlocked.add("vengance_bot_mastery_2")
        if vengance_bot_wins >= VENGANCE_BOT_MASTERY_3_WINS:
            clean_unlocked.add("vengance_bot_mastery_3")
        if clean_progress.get("vengance_bot_low_mine_wins", 0) >= 2:
            clean_unlocked.add("vengance_werewolf")
        if (
            clean_progress.get("ducky_daddys_belt_wins", 0) >= 1
            and clean_progress.get("ducky_ogel_wins", 0) >= 1
        ):
            clean_unlocked.add("ducky_subject_5_png")
        if clean_progress.get("malice_bird_form_wins", 0) >= MALICE_BIRD_FORM_WINS:
            clean_unlocked.add("malice_bug")
        if clean_progress.get("explorer_losses", 0) >= MALICE_BONES_EXPLORER_LOSSES:
            clean_unlocked.add("malice_bones")
        if clean_progress.get("malice_wins", 0) >= MALICE_ROBOTIC_WINS:
            clean_unlocked.add("malice_robotic")

        return {
            "total_wins": max(0, wins),
            "unlocked_skins": sorted(clean_unlocked),
            "challenge_progress": clean_progress,
        }

    def save_progress(self) -> None:
        try:
            SAVE_FILE.write_text(
                json.dumps(
                    {
                        "total_wins": self.total_wins,
                        "unlocked_skins": sorted(self.unlocked_skins),
                        "challenge_progress": self.challenge_progress,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        except OSError:
            pass

    def clean_high_score_entry(self, entry: object) -> dict[str, object] | None:
        return clean_leaderboard_entry(entry)

    def sorted_high_scores(self, entries: list[dict[str, object]]) -> list[dict[str, object]]:
        return sorted_leaderboard_entries(entries)

    def load_high_scores(self) -> list[dict[str, object]]:
        if not HIGH_SCORE_FILE.exists():
            return []

        try:
            data = json.loads(HIGH_SCORE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        entries: list[dict[str, object]] = []
        for item in data:
            entry = self.clean_high_score_entry(item)
            if entry is not None:
                entries.append(entry)
        return self.sorted_high_scores(entries)

    def write_high_scores(self, entries: list[dict[str, object]]) -> None:
        scores = self.sorted_high_scores(entries)
        try:
            HIGH_SCORE_FILE.write_text(
                json.dumps(scores, indent=2),
                encoding="utf-8",
            )
        except OSError:
            pass

    def save_high_scores(self) -> None:
        self.high_scores = self.sorted_high_scores(self.high_scores)
        self.write_high_scores(self.high_scores)

    def setup_leaderboard_sync(self) -> None:
        self.online_high_scores: list[dict[str, object]] = []
        self.leaderboard_online_available = False
        self.leaderboard_loaded_at: float | None = None
        self.leaderboard_scores_dirty = False
        self.leaderboard_source = "local"
        self.leaderboard_tasks: list[tuple[str, Future]] = []
        self.leaderboard_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="leaderboard")

    def shutdown_leaderboard_sync(self) -> None:
        executor = getattr(self, "leaderboard_executor", None)
        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=True)
            self.leaderboard_executor = None

    def leaderboard_task_pending(self, task_name: str | None = None) -> bool:
        for pending_name, future in getattr(self, "leaderboard_tasks", []):
            if future.done():
                continue
            if task_name is None or pending_name == task_name:
                return True
        return False

    def queue_leaderboard_task(self, task_name: str, task_func, *args) -> None:
        executor = getattr(self, "leaderboard_executor", None)
        if executor is None:
            return
        future = executor.submit(task_func, *args)
        self.leaderboard_tasks.append((task_name, future))

    def queue_startup_leaderboard_sync(self) -> None:
        if self.leaderboard_task_pending("startup"):
            return
        local_scores = self.load_high_scores()
        self.high_scores = local_scores
        self.queue_leaderboard_task("startup", startup_sync, local_scores)

    def queue_leaderboard_refresh(self) -> None:
        if self.leaderboard_task_pending():
            return
        self.queue_leaderboard_task("refresh", refresh_online_scores)

    def poll_leaderboard_tasks(self) -> None:
        remaining_tasks: list[tuple[str, Future]] = []
        for task_name, future in self.leaderboard_tasks:
            if not future.done():
                remaining_tasks.append((task_name, future))
                continue

            try:
                result = future.result()
            except Exception:
                self.apply_leaderboard_error(task_name)
            else:
                self.apply_leaderboard_result(task_name, result)

        self.leaderboard_tasks = remaining_tasks

    def apply_leaderboard_result(self, task_name: str, result: LeaderboardSyncResult) -> None:
        scores = self.sorted_high_scores(result.scores)
        self.online_high_scores = scores
        self.high_scores = scores
        self.leaderboard_online_available = True
        self.leaderboard_loaded_at = time.monotonic()
        self.leaderboard_scores_dirty = False
        self.leaderboard_source = "online"

        local_cache = scores
        if result.remaining_local_scores:
            local_cache = self.sorted_high_scores([*scores, *result.remaining_local_scores])
        self.write_high_scores(local_cache)

        if task_name == "startup" and result.posted_count:
            self.high_score_notice = f"Online leaderboard synced {result.posted_count} local score{'s' if result.posted_count != 1 else ''}."
        elif task_name == "submit":
            self.high_score_notice = "High score submitted online."
        elif task_name == "refresh":
            self.high_score_notice = "Online leaderboard updated."
        else:
            self.high_score_notice = "Online leaderboard loaded."

    def apply_leaderboard_error(self, task_name: str) -> None:
        self.leaderboard_online_available = False
        self.leaderboard_source = "local"
        self.high_scores = self.load_high_scores()
        if task_name == "submit":
            self.leaderboard_scores_dirty = True
            self.high_score_notice = "Online leaderboard unavailable. Score saved locally."
        else:
            self.high_score_notice = "Online leaderboard unavailable. Showing local scores."

    def online_high_scores_stale(self) -> bool:
        if not self.leaderboard_online_available or self.leaderboard_loaded_at is None:
            return True
        if self.leaderboard_scores_dirty:
            return True
        return time.monotonic() - self.leaderboard_loaded_at > LEADERBOARD_CACHE_TTL_SECONDS

    def high_score_qualifies(self, score: int) -> bool:
        score = max(0, int(score))
        if self.online_high_scores_stale():
            self.queue_leaderboard_refresh()

        if self.leaderboard_online_available:
            self.high_scores = self.sorted_high_scores(self.online_high_scores)
        else:
            self.high_scores = self.load_high_scores()
            self.leaderboard_source = "local"
        return score_qualifies_for_entries(score, self.high_scores)

    def reset_high_score_entry(self) -> None:
        self.high_score_name = ""
        self.high_score_message = ""
        self.high_score_active_field = "name"
        self.high_score_notice = ""

    def show_high_score_entry(self) -> None:
        self.reset_high_score_entry()
        self.state = GameState.HIGH_SCORE_ENTRY

    def show_high_score_board(self) -> None:
        if self.leaderboard_online_available and not self.leaderboard_task_pending("submit"):
            self.high_scores = self.sorted_high_scores(self.online_high_scores)
            self.leaderboard_source = "online"
        else:
            self.high_scores = self.load_high_scores()
            self.leaderboard_source = "local"
        self.state = GameState.HIGH_SCORE_BOARD

    def submit_high_score(self) -> None:
        name = self.high_score_name.strip()[:HIGH_SCORE_NAME_LIMIT] or "Player"
        message = self.high_score_message.strip()[:HIGH_SCORE_MESSAGE_LIMIT]
        entry = {
            "date": date.today().isoformat(),
            "name": name,
            "score": max(0, int(self.final_score)),
            "message": message,
        }
        self.high_scores = self.sorted_high_scores([entry, *self.load_high_scores()])
        self.save_high_scores()
        self.leaderboard_scores_dirty = True
        self.high_score_notice = "High score saved locally. Syncing online..."
        self.queue_leaderboard_task("submit", submit_score_and_refresh, entry)
        self.show_high_score_board()

    def skip_high_score_entry(self) -> None:
        self.high_score_notice = "High score skipped."
        self.show_high_score_board()

    def fried_chicken_unlocked(self) -> bool:
        return self.skin_unlocked("fried_chicken")

    def skin_unlocked(self, skin_id: str) -> bool:
        return skin_id in self.unlocked_skins

    def unlock_skin(self, skin_id: str, reason: str) -> None:
        if skin_id not in SKINS or skin_id in self.unlocked_skins:
            return

        self.unlocked_skins.add(skin_id)
        self.skin_notice = f"{SKINS[skin_id]['name']} unlocked: {reason}"
        self.save_progress()

    def record_win(self) -> None:
        was_locked = not self.fried_chicken_unlocked()
        self.total_wins += 1
        if was_locked and self.total_wins >= FRIED_CHICKEN_UNLOCK_WINS:
            self.unlock_skin("fried_chicken", "5 wins completed")

        if self.player_role == "Killer" and self.round_killer == "revenge_bot":
            selected_ducky_skin = self.selected_skins.get("revenge_bot")
            if selected_ducky_skin == "ducky_daddys_belt":
                self.challenge_progress["ducky_daddys_belt_wins"] = max(
                    1,
                    self.challenge_progress.get("ducky_daddys_belt_wins", 0),
                )
            elif selected_ducky_skin == "ducky_ogel":
                self.challenge_progress["ducky_ogel_wins"] = max(
                    1,
                    self.challenge_progress.get("ducky_ogel_wins", 0),
                )

            if (
                self.challenge_progress.get("ducky_daddys_belt_wins", 0) >= 1
                and self.challenge_progress.get("ducky_ogel_wins", 0) >= 1
            ):
                self.unlock_skin("ducky_subject_5_png", "won with Daddy's Belt and Ogel")

        if self.player_role == "Killer" and self.round_killer == "show_runner":
            if self.selected_skins.get("show_runner") == "pack_runner":
                self.unlock_skin("maldin_inverted", "won with Pack Runner")
            wins = self.challenge_progress.get("show_runner_wins", 0) + 1
            self.challenge_progress["show_runner_wins"] = wins
            if wins >= OCEAN_RUNNER_UNLOCK_WINS:
                self.unlock_skin("ocean_runner", "3 Show Runner wins completed")

            kills = self.challenge_progress.get("show_runner_kills", 0) + 1
            self.challenge_progress["show_runner_kills"] = kills
            if kills >= SHOW_RUNNER_MASTERY_1_KILLS:
                self.unlock_skin("show_runner_mastery_1", "20 Show Runner kills completed")
            if kills >= SHOW_RUNNER_MASTERY_2_KILLS:
                self.unlock_skin("show_runner_mastery_2", "40 Show Runner kills completed")
            if kills >= SHOW_RUNNER_MASTERY_3_KILLS:
                self.unlock_skin("show_runner_mastery_3", "61 Show Runner kills completed")

        if (
            self.player_role == "Killer"
            and self.round_killer == "subslasher"
            and self.selected_skins.get("subslasher") == "tennis_dude"
        ):
            self.unlock_skin("pickle_ball_bro", "won with Tennis Dude")

        if self.player_role == "Killer" and self.round_killer == "vengance_bot":
            if self.vengance_mines_placed_this_round <= 3:
                low_mine_wins = self.challenge_progress.get("vengance_bot_low_mine_wins", 0) + 1
                self.challenge_progress["vengance_bot_low_mine_wins"] = low_mine_wins
                if low_mine_wins >= 2:
                    self.unlock_skin("vengance_werewolf", "2 wins with 3 or fewer landmines")

            if self.vengance_mines_placed_this_round == 0:
                self.unlock_skin("vengance_scoreboard", "won without landmines")

            wins = self.challenge_progress.get("vengance_bot_wins", 0) + 1
            self.challenge_progress["vengance_bot_wins"] = wins
            if wins >= VENGANCE_BOT_MASTERY_1_WINS:
                self.unlock_skin("vengance_bot_mastery_1", "20 Vengance Bot wins completed")
            if wins >= VENGANCE_BOT_MASTERY_2_WINS:
                self.unlock_skin("vengance_bot_mastery_2", "50 Vengance Bot wins completed")
            if wins >= VENGANCE_BOT_MASTERY_3_WINS:
                self.unlock_skin("vengance_bot_mastery_3", "79 Vengance Bot wins completed")

        if self.player_role == "Killer" and self.round_killer == "malice":
            if isinstance(self.player, Killer) and self.player.is_malice_bird():
                bird_form_wins = self.challenge_progress.get("malice_bird_form_wins", 0) + 1
                self.challenge_progress["malice_bird_form_wins"] = bird_form_wins
                if bird_form_wins >= MALICE_BIRD_FORM_WINS:
                    self.unlock_skin("malice_bug", "3 Malice bird-form wins completed")

            wins = self.challenge_progress.get("malice_wins", 0) + 1
            self.challenge_progress["malice_wins"] = wins
            if wins >= MALICE_ROBOTIC_WINS:
                self.unlock_skin("malice_robotic", "8 Malice wins completed")

        if self.player_role == "Survivor" and self.round_killer == "vengance_bot":
            self.record_vengance_bot_survive()

        self.save_progress()

    def record_loss(self) -> None:
        if self.player_role == "Killer" and self.round_killer == "revenge_bot":
            losses = self.challenge_progress.get("ducky_losses", 0) + 1
            self.challenge_progress["ducky_losses"] = losses
            if losses >= DUCKY_INVERTED_LOSSES:
                self.unlock_skin("ducky_inverted", "lost twice as Ducky")
            if losses >= DUCKY_OGEL_LOSSES:
                self.unlock_skin("ducky_ogel", "lost 4 times as Ducky")

        if self.player_role == "Survivor" and self.selected_player_survivor == "survivor_explorer":
            losses = self.challenge_progress.get("explorer_losses", 0) + 1
            self.challenge_progress["explorer_losses"] = losses
            if losses >= MALICE_BONES_EXPLORER_LOSSES:
                self.unlock_skin("malice_bones", "lost 3 rounds as Explorer")

        self.save_progress()

    def record_vengance_bot_survive(self) -> None:
        survives = self.challenge_progress.get("vengance_bot_survives", 0) + 1
        self.challenge_progress["vengance_bot_survives"] = survives
        if survives >= WICK_WONALDS_SURVIVES:
            self.unlock_skin("wick_wonalds", "survived Vengance Bot twice")

    def skin_challenge_text(self, skin_id: str) -> str:
        if skin_id == "fried_chicken":
            remaining = max(0, FRIED_CHICKEN_UNLOCK_WINS - self.total_wins)
            return f"win {remaining} more"
        if skin_id in ("ducky_inverted", "ducky_ogel"):
            target = DUCKY_INVERTED_LOSSES if skin_id == "ducky_inverted" else DUCKY_OGEL_LOSSES
            losses = self.challenge_progress.get("ducky_losses", 0)
            return f"Ducky losses {losses}/{target}"
        if skin_id == "ducky_daddys_belt":
            return "C swing survivor kill"
        if skin_id == "ducky_subject_5_png":
            belt_win = self.challenge_progress.get("ducky_daddys_belt_wins", 0)
            ogel_win = self.challenge_progress.get("ducky_ogel_wins", 0)
            return f"Belt win {belt_win}/1, Ogel win {ogel_win}/1"
        if skin_id == "ocean_runner":
            wins = self.challenge_progress.get("show_runner_wins", 0)
            return f"Show Runner wins {wins}/{OCEAN_RUNNER_UNLOCK_WINS}"
        if skin_id in ("show_runner_mastery_1", "show_runner_mastery_2", "show_runner_mastery_3"):
            target = self.show_runner_mastery_kill_target(skin_id)
            kills = self.challenge_progress.get("show_runner_kills", 0)
            return f"Show Runner kills {kills}/{target}"
        if skin_id == "wick_wonalds":
            survives = self.challenge_progress.get("vengance_bot_survives", 0)
            return f"survive Vengance Bot {survives}/{WICK_WONALDS_SURVIVES}"
        if skin_id == "vengance_spinning":
            return "one perimeter lap"
        if skin_id == "vengance_werewolf":
            wins = self.challenge_progress.get("vengance_bot_low_mine_wins", 0)
            return f"low-mine wins {wins}/2"
        if skin_id in ("vengance_bot_mastery_1", "vengance_bot_mastery_2", "vengance_bot_mastery_3"):
            target = self.vengance_bot_mastery_win_target(skin_id)
            wins = self.challenge_progress.get("vengance_bot_wins", 0)
            return f"Vengance Bot wins {wins}/{target}"
        if skin_id == "malice_bug":
            wins = self.challenge_progress.get("malice_bird_form_wins", 0)
            return f"Malice bird wins {wins}/{MALICE_BIRD_FORM_WINS}"
        if skin_id == "malice_bones":
            losses = self.challenge_progress.get("explorer_losses", 0)
            return f"Explorer losses {losses}/{MALICE_BONES_EXPLORER_LOSSES}"
        if skin_id == "malice_robotic":
            wins = self.challenge_progress.get("malice_wins", 0)
            return f"Malice wins {wins}/{MALICE_ROBOTIC_WINS}"
        return SKINS[skin_id]["challenge"]

    def show_runner_mastery_kill_target(self, skin_id: str) -> int:
        if skin_id == "show_runner_mastery_1":
            return SHOW_RUNNER_MASTERY_1_KILLS
        if skin_id == "show_runner_mastery_2":
            return SHOW_RUNNER_MASTERY_2_KILLS
        return SHOW_RUNNER_MASTERY_3_KILLS

    def vengance_bot_mastery_win_target(self, skin_id: str) -> int:
        if skin_id == "vengance_bot_mastery_1":
            return VENGANCE_BOT_MASTERY_1_WINS
        if skin_id == "vengance_bot_mastery_2":
            return VENGANCE_BOT_MASTERY_2_WINS
        return VENGANCE_BOT_MASTERY_3_WINS

    def skin_challenge_detail(self, skin_id: str) -> str:
        if skin_id == "fried_chicken":
            remaining = max(0, FRIED_CHICKEN_UNLOCK_WINS - self.total_wins)
            return f"Win {remaining} more round{'s' if remaining != 1 else ''} to unlock Fried Chicken."
        if skin_id == "ducky_inverted":
            losses = self.challenge_progress.get("ducky_losses", 0)
            remaining = max(0, DUCKY_INVERTED_LOSSES - losses)
            return f"Play as Ducky and lose {remaining} more round{'s' if remaining != 1 else ''}."
        if skin_id == "ducky_ogel":
            losses = self.challenge_progress.get("ducky_losses", 0)
            remaining = max(0, DUCKY_OGEL_LOSSES - losses)
            return f"Play as Ducky and lose {remaining} more round{'s' if remaining != 1 else ''}."
        if skin_id == "ducky_daddys_belt":
            return "Play as Ducky and kill the survivor with the C swing ability."
        if skin_id == "ducky_subject_5_png":
            belt_done = self.challenge_progress.get("ducky_daddys_belt_wins", 0) >= 1
            ogel_done = self.challenge_progress.get("ducky_ogel_wins", 0) >= 1
            missing = []
            if not belt_done:
                missing.append("win a round using Daddy's Belt")
            if not ogel_done:
                missing.append("win a round using Ogel")
            return "Unlock by completing: " + " and ".join(missing) + "."
        if skin_id == "tennis_dude":
            return "Play as Subslasher and hit the survivor with Perpelling Shootdown, the freeze ice spike."
        if skin_id == "pickle_ball_bro":
            return "Play as Subslasher, select the Tennis Dude skin, then win the round."
        if skin_id == "pack_runner":
            return "Play as Show Runner and run around the arena perimeter 3 times in a row."
        if skin_id == "maldin_inverted":
            return "Play as Show Runner, select the Pack Runner skin, then win the round."
        if skin_id == "ocean_runner":
            wins = self.challenge_progress.get("show_runner_wins", 0)
            remaining = max(0, OCEAN_RUNNER_UNLOCK_WINS - wins)
            return f"Win {remaining} more round{'s' if remaining != 1 else ''} as Show Runner."
        if skin_id in ("show_runner_mastery_1", "show_runner_mastery_2", "show_runner_mastery_3"):
            target = self.show_runner_mastery_kill_target(skin_id)
            kills = self.challenge_progress.get("show_runner_kills", 0)
            remaining = max(0, target - kills)
            return f"Kill {remaining} more survivor{'s' if remaining != 1 else ''} as Show Runner."
        if skin_id == "wick_wonalds":
            survives = self.challenge_progress.get("vengance_bot_survives", 0)
            remaining = max(0, WICK_WONALDS_SURVIVES - survives)
            return f"Survive Vengance Bot {remaining} more time{'s' if remaining != 1 else ''} as Survivor."
        if skin_id == "mlg":
            return "Play as Vengance Bot and kill the survivor with a landmine after placing 2 or fewer landmines that round."
        if skin_id == "vengance_scoreboard":
            return "Play as Vengance Bot and win the round without placing any landmines."
        if skin_id == "vengance_spinning":
            return "Run clockwise around all 4 arena edges once with any player character."
        if skin_id == "vengance_werewolf":
            wins = self.challenge_progress.get("vengance_bot_low_mine_wins", 0)
            remaining = max(0, 2 - wins)
            return f"Win {remaining} more Vengance Bot round{'s' if remaining != 1 else ''} while placing 3 or fewer landmines."
        if skin_id in ("vengance_bot_mastery_1", "vengance_bot_mastery_2", "vengance_bot_mastery_3"):
            target = self.vengance_bot_mastery_win_target(skin_id)
            wins = self.challenge_progress.get("vengance_bot_wins", 0)
            remaining = max(0, target - wins)
            return f"Win {remaining} more round{'s' if remaining != 1 else ''} as Vengance Bot."
        if skin_id == "malice_bug":
            wins = self.challenge_progress.get("malice_bird_form_wins", 0)
            remaining = max(0, MALICE_BIRD_FORM_WINS - wins)
            return f"Win {remaining} more Malice round{'s' if remaining != 1 else ''} while Hunter's Rage bird form is active at round end."
        if skin_id == "malice_bones":
            losses = self.challenge_progress.get("explorer_losses", 0)
            remaining = max(0, MALICE_BONES_EXPLORER_LOSSES - losses)
            return f"Choose Explorer as Survivor and lose {remaining} more round{'s' if remaining != 1 else ''}."
        if skin_id == "malice_robotic":
            wins = self.challenge_progress.get("malice_wins", 0)
            remaining = max(0, MALICE_ROBOTIC_WINS - wins)
            return f"Win {remaining} more round{'s' if remaining != 1 else ''} as Malice."
        return SKINS[skin_id]["challenge"]

    def skin_progress_text(self) -> str:
        unlocked_count = len(self.unlocked_skins)
        total_count = len(SKINS)
        if unlocked_count == total_count:
            return "All killer cosmetics unlocked."
        return f"Killer cosmetics unlocked: {unlocked_count}/{total_count}. Keep clearing challenges."

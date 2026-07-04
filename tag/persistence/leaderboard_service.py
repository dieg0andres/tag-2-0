from __future__ import annotations

from dataclasses import dataclass, field

import requests

from tag.config.settings import (
    HIGH_SCORE_LIMIT,
    HIGH_SCORE_MESSAGE_LIMIT,
    HIGH_SCORE_NAME_LIMIT,
    LEADERBOARD_SYNC_LIMIT,
    LEADERBOARD_TIMEOUT,
    LEADERBOARD_URL,
)


ScoreEntry = dict[str, object]


class LeaderboardServiceError(RuntimeError):
    """Raised when the online leaderboard cannot be reached or parsed."""


def display_date(value: object) -> str:
    if not isinstance(value, str):
        return ""
    date_text = value.strip()
    if "T" in date_text:
        date_text = date_text.split("T", 1)[0]
    elif " " in date_text:
        date_text = date_text.split(" ", 1)[0]
    return date_text[:10]


@dataclass(frozen=True)
class LeaderboardSyncResult:
    scores: list[ScoreEntry]
    posted_count: int = 0
    remaining_local_scores: list[ScoreEntry] = field(default_factory=list)


def clean_leaderboard_entry(entry: object) -> ScoreEntry | None:
    if not isinstance(entry, dict):
        return None

    score = entry.get("score", 0)
    if isinstance(score, bool):
        score = 0
    elif isinstance(score, int):
        score = max(0, score)
    elif isinstance(score, str) and score.isdigit():
        score = int(score)
    else:
        return None

    entry_date = display_date(entry.get("date", ""))

    name = entry.get("name", "Player")
    if not isinstance(name, str):
        name = "Player"
    name = name.strip()[:HIGH_SCORE_NAME_LIMIT] or "Player"

    message = entry.get("message", "")
    if not isinstance(message, str):
        message = ""
    message = message.strip()[:HIGH_SCORE_MESSAGE_LIMIT]

    return {
        "date": entry_date,
        "name": name,
        "score": score,
        "message": message,
    }


def sorted_leaderboard_entries(entries: list[ScoreEntry]) -> list[ScoreEntry]:
    clean_entries = [entry for entry in (clean_leaderboard_entry(entry) for entry in entries) if entry is not None]
    return sorted(clean_entries, key=lambda entry: int(entry.get("score", 0)), reverse=True)[:HIGH_SCORE_LIMIT]


def leaderboard_entry_signature(entry: ScoreEntry) -> tuple[str, int, str]:
    clean_entry = clean_leaderboard_entry(entry) or {"name": "Player", "score": 0, "message": ""}
    return (
        str(clean_entry.get("name", "")).strip(),
        int(clean_entry.get("score", 0)),
        str(clean_entry.get("message", "")).strip(),
    )


def score_qualifies_for_entries(score: int, entries: list[ScoreEntry]) -> bool:
    score = max(0, int(score))
    scores = sorted_leaderboard_entries(entries)
    if len(scores) < HIGH_SCORE_LIMIT:
        return True
    lowest_score = int(scores[-1].get("score", 0))
    return score > lowest_score


def post_payload_for_entry(entry: ScoreEntry) -> dict[str, object]:
    clean_entry = clean_leaderboard_entry(entry)
    if clean_entry is None:
        raise LeaderboardServiceError("Invalid leaderboard entry.")

    payload: dict[str, object] = {
        "name": clean_entry["name"],
        "score": clean_entry["score"],
    }
    message = str(clean_entry.get("message", "")).strip()
    if message:
        payload["message"] = message
    return payload


def fetch_online_scores(session=requests) -> list[ScoreEntry]:
    try:
        response = session.get(LEADERBOARD_URL, timeout=LEADERBOARD_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise LeaderboardServiceError(f"Leaderboard GET failed: {exc}") from exc
    except ValueError as exc:
        raise LeaderboardServiceError(f"Leaderboard GET returned invalid JSON: {exc}") from exc

    scores = data.get("top_10_scores") if isinstance(data, dict) else None
    if not isinstance(scores, list):
        raise LeaderboardServiceError("Leaderboard GET response did not include top_10_scores.")

    return sorted_leaderboard_entries(scores)


def post_online_score(entry: ScoreEntry, session=requests) -> None:
    payload = post_payload_for_entry(entry)
    try:
        response = session.post(LEADERBOARD_URL, json=payload, timeout=LEADERBOARD_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise LeaderboardServiceError(f"Leaderboard POST failed: {exc}") from exc


def select_local_scores_to_sync(
    local_scores: list[ScoreEntry],
    online_scores: list[ScoreEntry],
    limit: int | None = None,
) -> list[ScoreEntry]:
    selected: list[ScoreEntry] = []
    simulated_online = sorted_leaderboard_entries(online_scores)
    seen_signatures = {leaderboard_entry_signature(entry) for entry in simulated_online}

    for entry in sorted_leaderboard_entries(local_scores):
        signature = leaderboard_entry_signature(entry)
        if signature in seen_signatures:
            continue
        if not score_qualifies_for_entries(int(entry.get("score", 0)), simulated_online):
            continue

        selected.append(entry)
        seen_signatures.add(signature)
        simulated_online = sorted_leaderboard_entries([*simulated_online, entry])
        if limit is not None and len(selected) >= max(0, limit):
            break

    return selected


def startup_sync(local_scores: list[ScoreEntry], session=requests) -> LeaderboardSyncResult:
    online_scores = fetch_online_scores(session)
    scores_to_post = select_local_scores_to_sync(local_scores, online_scores, LEADERBOARD_SYNC_LIMIT)

    for entry in scores_to_post:
        post_online_score(entry, session)

    if scores_to_post:
        online_scores = fetch_online_scores(session)

    remaining_local_scores = select_local_scores_to_sync(local_scores, online_scores)
    return LeaderboardSyncResult(
        scores=online_scores,
        posted_count=len(scores_to_post),
        remaining_local_scores=remaining_local_scores,
    )


def refresh_online_scores(session=requests) -> LeaderboardSyncResult:
    return LeaderboardSyncResult(scores=fetch_online_scores(session))


def submit_score_and_refresh(entry: ScoreEntry, session=requests) -> LeaderboardSyncResult:
    post_online_score(entry, session)
    return LeaderboardSyncResult(scores=fetch_online_scores(session), posted_count=1)

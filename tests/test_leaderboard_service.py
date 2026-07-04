from __future__ import annotations

import unittest

from tag.persistence import leaderboard_service as service


def entry(name: str, score: int, message: str = "") -> dict[str, object]:
    return {
        "date": "2026-07-04T10:15:00-05:00",
        "name": name,
        "score": score,
        "message": message,
    }


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self.payload


class FakeSession:
    def __init__(self, get_payloads: list[dict[str, object]]) -> None:
        self.get_payloads = list(get_payloads)
        self.posts: list[dict[str, object]] = []

    def get(self, url: str, timeout: float) -> FakeResponse:
        return FakeResponse(self.get_payloads.pop(0))

    def post(self, url: str, json: dict[str, object], timeout: float) -> FakeResponse:
        self.posts.append(json)
        return FakeResponse({})


class LeaderboardServiceTest(unittest.TestCase):
    def test_clean_entry_defaults_missing_message(self) -> None:
        cleaned = service.clean_leaderboard_entry({"name": " Diego ", "score": "100"})

        self.assertEqual(
            cleaned,
            {
                "date": "",
                "name": "Diego",
                "score": 100,
                "message": "",
            },
        )

    def test_clean_entry_shows_timestamp_as_date_only(self) -> None:
        cleaned = service.clean_leaderboard_entry(entry("Diego", 100))

        self.assertEqual(cleaned["date"], "2026-07-04")

    def test_post_payload_omits_empty_message(self) -> None:
        payload = service.post_payload_for_entry(entry("Diego", 100))

        self.assertEqual(payload, {"name": "Diego", "score": 100})

    def test_select_local_scores_to_sync_avoids_duplicates_and_caps_limit(self) -> None:
        online_scores = [
            entry("A", 100),
            entry("B", 90),
            entry("C", 80),
            entry("D", 70),
            entry("E", 60),
            entry("F", 50),
            entry("G", 40),
            entry("H", 30),
            entry("I", 20),
            entry("J", 10),
        ]
        local_scores = [
            entry("B", 90),
            entry("Local 1", 95),
            entry("Local 2", 85),
            entry("Too Low", 5),
        ]

        selected = service.select_local_scores_to_sync(local_scores, online_scores, limit=2)

        self.assertEqual([item["name"] for item in selected], ["Local 1", "Local 2"])

    def test_startup_sync_posts_two_local_scores_and_keeps_remaining_backlog(self) -> None:
        first_online_scores = [
            entry("A", 100),
            entry("B", 90),
            entry("C", 80),
            entry("D", 70),
            entry("E", 60),
            entry("F", 50),
            entry("G", 40),
            entry("H", 30),
            entry("I", 20),
            entry("J", 10),
        ]
        refreshed_online_scores = [
            entry("A", 100),
            entry("Local 1", 95),
            entry("B", 90),
            entry("Local 2", 85),
            entry("C", 80),
            entry("D", 70),
            entry("E", 60),
            entry("F", 50),
            entry("G", 40),
            entry("H", 30),
        ]
        session = FakeSession(
            [
                {"top_10_scores": first_online_scores},
                {"top_10_scores": refreshed_online_scores},
            ]
        )
        local_scores = [
            entry("Local 1", 95),
            entry("Local 2", 85),
            entry("Local 3", 75),
        ]

        result = service.startup_sync(local_scores, session=session)

        self.assertEqual(result.posted_count, 2)
        self.assertEqual([post["name"] for post in session.posts], ["Local 1", "Local 2"])
        self.assertEqual([item["name"] for item in result.remaining_local_scores], ["Local 3"])

    def test_fetch_online_scores_rejects_bad_shape(self) -> None:
        session = FakeSession([{"scores": []}])

        with self.assertRaises(service.LeaderboardServiceError):
            service.fetch_online_scores(session=session)


if __name__ == "__main__":
    unittest.main()

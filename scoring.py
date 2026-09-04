'''
    scoring: turns a finished run into a score and keeps a local leaderboard
'''
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from engine import Engine

LEADERBOARD_FILE = "leaderboard.json"

# Global leaderboard API (see infra/). The local file above is always the
# source of truth and the offline fallback; the API is best-effort on top -
# set MATURAM_LEADERBOARD_API_KEY to enable submitting to it.
API_BASE_URL = os.environ.get(
    "MATURAM_LEADERBOARD_API_URL",
    "https://arrpq65ila.execute-api.eu-west-2.amazonaws.com",
)
API_KEY = os.environ.get("MATURAM_LEADERBOARD_API_KEY")
API_TIMEOUT_SECONDS = 2

# XP is the main currency of progress, depth is the hardest-won measure of
# progress so it's weighted heavily, and turns survived is a small tiebreaker
# so that stalling in a safe corner doesn't outscore actually playing.
XP_WEIGHT = 1
DEPTH_WEIGHT = 100
TURN_WEIGHT = 1


@dataclass
class ScoreEntry:
    '''
        a single recorded run
    '''
    player: str
    score: int
    xp: int
    depth: int
    turns: int
    timestamp: str


def calculate_score(engine: "Engine") -> int:
    '''
        combine XP earned, dungeon depth reached, and turns survived into one score
    '''
    xp = engine.player.level.current_xp
    depth = engine.game_world.current_floor
    turns = engine.turn_count

    return xp * XP_WEIGHT + depth * DEPTH_WEIGHT + turns * TURN_WEIGHT


def load_leaderboard(filename: str = LEADERBOARD_FILE) -> List[ScoreEntry]:
    '''
        load previously recorded scores, or an empty list if none exist yet
    '''
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as f:
        raw_entries = json.load(f)

    return [ScoreEntry(**raw) for raw in raw_entries]


def record_score(engine: "Engine", filename: str = LEADERBOARD_FILE) -> ScoreEntry:
    '''
        calculate the final score for this run and append it to the leaderboard file
    '''
    entry = ScoreEntry(
        player=engine.player.name,
        score=calculate_score(engine),
        xp=engine.player.level.current_xp,
        depth=engine.game_world.current_floor,
        turns=engine.turn_count,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    entries = load_leaderboard(filename)
    entries.append(entry)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in entries], f, indent=2)

    submit_remote_score(entry)

    return entry


def submit_remote_score(entry: ScoreEntry) -> bool:
    '''
        best-effort push of a locally-recorded entry to the global
        leaderboard; the local file is always the source of truth, so any
        failure here (no key configured, offline, API down) is swallowed
    '''
    if not API_KEY:
        return False

    try:
        response = requests.post(
            f"{API_BASE_URL}/scores",
            json={
                "player": entry.player,
                "score": entry.score,
                "xp": entry.xp,
                "depth": entry.depth,
                "turns": entry.turns,
            },
            headers={"x-api-key": API_KEY},
            timeout=API_TIMEOUT_SECONDS,
        )
        return response.ok
    except requests.exceptions.RequestException:
        return False


def top_scores(filename: str = LEADERBOARD_FILE, count: int = 10) -> List[ScoreEntry]:
    '''
        the highest-scoring runs recorded so far, best first
    '''
    entries = load_leaderboard(filename)

    return sorted(entries, key=lambda entry: entry.score, reverse=True)[:count]


def global_top_scores(count: int = 10, filename: str = LEADERBOARD_FILE) -> List[ScoreEntry]:
    '''
        top scores from the shared global leaderboard; falls back to the
        local leaderboard on any failure (offline, API down, etc.)
    '''
    try:
        response = requests.get(
            f"{API_BASE_URL}/scores/top",
            params={"limit": count},
            timeout=API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return [ScoreEntry(**raw) for raw in response.json()]
    except requests.exceptions.RequestException:
        return top_scores(filename, count)

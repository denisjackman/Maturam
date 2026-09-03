'''
    scoring: turns a finished run into a score and keeps a local leaderboard
'''
from __future__ import annotations

import getpass
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine

LEADERBOARD_FILE = "leaderboard.json"

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
        player=getpass.getuser(),
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

    return entry


def top_scores(filename: str = LEADERBOARD_FILE, count: int = 10) -> List[ScoreEntry]:
    '''
        the highest-scoring runs recorded so far, best first
    '''
    entries = load_leaderboard(filename)

    return sorted(entries, key=lambda entry: entry.score, reverse=True)[:count]

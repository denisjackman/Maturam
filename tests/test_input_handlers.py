'''
    Tests for input_handlers.py - the pure, console-free parts.
'''
import scoring
from input_handlers import _format_leaderboard_row  # pylint: disable=W0212


def make_entry(**overrides):
    ''' a ScoreEntry with sensible defaults, overridden per test '''
    defaults = {
        "player": "Zara",
        "score": 1430,
        "xp": 195,
        "depth": 5,
        "turns": 810,
        "timestamp": "2026-09-04T12:00:00+00:00",
    }
    defaults.update(overrides)
    return scoring.ScoreEntry(**defaults)


def test_format_leaderboard_row_includes_rank_name_level_score_and_date():
    ''' the row should surface every field the leaderboard advertises '''
    row = _format_leaderboard_row(5, make_entry())

    assert row.startswith(" 5. ")
    assert "Zara" in row
    assert "L 5" in row
    assert " 1430" in row
    assert "2026-09-04" in row


def test_format_leaderboard_row_truncates_long_names():
    ''' names longer than the name column should be truncated with an ellipsis '''
    row = _format_leaderboard_row(1, make_entry(player="Bartholomew Fenwick"))

    assert "Bartholomew…" in row
    assert "Fenwick" not in row


def test_format_leaderboard_row_keeps_short_names_untruncated():
    ''' names within the column width should appear in full, padded '''
    row = _format_leaderboard_row(1, make_entry(player="Grix"))

    assert "Grix" in row
    assert "…" not in row

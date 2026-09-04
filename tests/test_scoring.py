'''
    Tests for scoring.py - score calculation and the local leaderboard file.
'''
import scoring


def test_calculate_score_combines_xp_depth_and_turns(engine, player):
    ''' score should be xp + depth*100 + turns, per the documented weights '''
    player.level.current_xp = 50
    engine.game_world.current_floor = 2
    engine.turn_count = 30

    assert scoring.calculate_score(engine) == 50 + 2 * 100 + 30


def test_load_leaderboard_missing_file_returns_empty_list(tmp_path):
    ''' loading a leaderboard that has never been written should return [] '''
    filename = str(tmp_path / "leaderboard.json")

    assert scoring.load_leaderboard(filename) == []


def test_record_score_appends_and_persists(engine, player, tmp_path):
    ''' record_score should write a loadable entry with the calculated score '''
    player.level.current_xp = 10
    engine.game_world.current_floor = 1
    engine.turn_count = 5
    filename = str(tmp_path / "leaderboard.json")

    entry = scoring.record_score(engine, filename)

    assert entry.score == 10 + 1 * 100 + 5
    loaded = scoring.load_leaderboard(filename)
    assert len(loaded) == 1
    assert loaded[0].score == entry.score


def test_record_score_uses_the_players_chosen_name(engine, player, tmp_path):
    ''' the leaderboard entry should use the character's own name, not the OS user '''
    player.name = "Thundermaw"
    filename = str(tmp_path / "leaderboard.json")

    entry = scoring.record_score(engine, filename)

    assert entry.player == "Thundermaw"


def test_record_score_appends_to_existing_entries(engine, player, tmp_path):
    ''' recording twice should keep both runs, not overwrite the file '''
    filename = str(tmp_path / "leaderboard.json")
    assert player is engine.player  # the fixture must wire engine.player before recording

    scoring.record_score(engine, filename)
    scoring.record_score(engine, filename)

    assert len(scoring.load_leaderboard(filename)) == 2


def test_top_scores_orders_best_first_and_respects_count(engine, player, tmp_path):
    ''' top_scores should sort descending by score and cap at count '''
    filename = str(tmp_path / "leaderboard.json")

    for xp in (10, 30, 20):
        player.level.current_xp = xp
        scoring.record_score(engine, filename)

    results = scoring.top_scores(filename, count=2)

    assert [entry.score for entry in results] == [30, 20]

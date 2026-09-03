'''
    Tests for render_functions.py (the pure, console-free parts).
'''
import entity_factories
from render_functions import get_names_at_location


def test_returns_empty_string_when_out_of_bounds(gamemap):
    ''' out-of-bounds coordinates should yield no names '''
    assert get_names_at_location(-1, 0, gamemap) == ""


def test_returns_empty_string_when_not_visible(gamemap, player):
    ''' unexplored/unseen tiles should yield no names '''
    assert get_names_at_location(player.x, player.y, gamemap) == ""


def test_returns_capitalised_name_when_visible(gamemap, player):
    ''' a visible tile should report the entity's capitalised name '''
    gamemap.visible[player.x, player.y] = True
    assert get_names_at_location(player.x, player.y, gamemap) == "Player"


def test_joins_multiple_entity_names(gamemap, player):
    ''' multiple entities on the same tile should all be named '''
    dagger = entity_factories.dagger.spawn(gamemap, player.x, player.y)
    gamemap.visible[player.x, player.y] = True

    result = get_names_at_location(player.x, player.y, gamemap)

    # .capitalize() lowercases everything but the first character, so
    # compare case-insensitively rather than asserting exact names.
    assert player.name.lower() in result.lower()
    assert dagger.name.lower() in result.lower()

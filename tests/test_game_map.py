'''
    Tests for game_map.py
'''
import entity_factories


def test_in_bounds(gamemap):
    ''' in_bounds() should only accept coordinates within width/height '''
    assert gamemap.in_bounds(0, 0) is True
    assert gamemap.in_bounds(gamemap.width - 1, gamemap.height - 1) is True
    assert gamemap.in_bounds(-1, 0) is False
    assert gamemap.in_bounds(gamemap.width, 0) is False


def test_get_blocking_entity_at_location(gamemap, player):
    ''' should find a movement-blocking entity at a given location '''
    assert gamemap.get_blocking_entity_at_location(5, 5) is player
    assert gamemap.get_blocking_entity_at_location(0, 0) is None


def test_get_actor_at_location(gamemap, player, orc):
    ''' should find whichever actor occupies a given location '''
    assert gamemap.get_actor_at_location(5, 5) is player
    assert gamemap.get_actor_at_location(10, 10) is orc
    assert gamemap.get_actor_at_location(0, 0) is None


def test_actors_and_items_iterators(gamemap, player, orc):
    ''' actors/items properties should filter entities by type '''
    dagger = entity_factories.dagger.spawn(gamemap, 1, 1)

    assert set(gamemap.actors) == {player, orc}
    assert list(gamemap.items) == [dagger]

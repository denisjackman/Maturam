'''
    Tests for entity.py - Entity/Actor base behaviour.
'''
import math

from entity import Entity
from entity_factories import player as player_template
from game_map import GameMap


def test_move_updates_position():
    ''' move() should offset x/y by the given delta '''
    entity = Entity(x=1, y=1)
    entity.move(2, -1)
    assert (entity.x, entity.y) == (3, 0)


def test_distance():
    ''' distance() should return straight-line distance to a point '''
    entity = Entity(x=0, y=0)
    assert entity.distance(3, 4) == math.sqrt(25)


def test_place_moves_entity_between_gamemaps(gamemap):
    ''' place() with a new gamemap should relocate the entity there '''
    actor = player_template.spawn(gamemap, 5, 5)
    other_map = GameMap(engine=gamemap.engine, width=10, height=10)

    actor.place(2, 2, other_map)

    assert actor not in gamemap.entities
    assert actor in other_map.entities
    assert (actor.x, actor.y) == (2, 2)


def test_spawn_creates_an_independent_copy(gamemap):
    ''' spawn() should deep-copy the template, not share components '''
    first = player_template.spawn(gamemap, 1, 1)
    second = player_template.spawn(gamemap, 2, 2)

    first.fighter.hp = 1

    assert first is not second
    assert first.fighter is not second.fighter
    assert second.fighter.hp == player_template.fighter.max_hp


def test_actor_is_alive_reflects_ai_state(player):
    ''' is_alive should track whether the actor still has an ai '''
    assert player.is_alive is True
    player.ai = None
    assert player.is_alive is False

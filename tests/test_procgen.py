'''
    Tests for procgen.py
'''
import entity_factories
from procgen import (
    RectangularRoom,
    get_entities_at_random,
    get_max_value_for_floor,
)


def test_rectangular_room_center():
    ''' center should be the midpoint of the room's bounds '''
    room = RectangularRoom(x=0, y=0, width=10, height=6)
    assert room.center == (5, 3)


def test_rectangular_room_inner():
    ''' inner should be a 1-tile-inset slice pair for carving floors '''
    room = RectangularRoom(x=2, y=3, width=4, height=5)
    inner_x, inner_y = room.inner

    assert (inner_x.start, inner_x.stop) == (3, 6)
    assert (inner_y.start, inner_y.stop) == (4, 8)


def test_rectangular_room_intersects_overlapping():
    ''' intersects() should be True for overlapping rooms '''
    room_a = RectangularRoom(0, 0, 5, 5)
    room_b = RectangularRoom(3, 3, 5, 5)
    assert room_a.intersects(room_b) is True


def test_rectangular_room_intersects_disjoint():
    ''' intersects() should be False for rooms that don't overlap '''
    room_a = RectangularRoom(0, 0, 5, 5)
    room_b = RectangularRoom(20, 20, 5, 5)
    assert room_a.intersects(room_b) is False


def test_get_max_value_for_floor_uses_highest_unlocked_tier():
    ''' should return the value for the highest tier unlocked at that floor '''
    tiers = [(1, 1), (4, 2), (6, 5)]

    assert get_max_value_for_floor(tiers, floor=0) == 0
    assert get_max_value_for_floor(tiers, floor=1) == 1
    assert get_max_value_for_floor(tiers, floor=5) == 2
    assert get_max_value_for_floor(tiers, floor=6) == 5


def test_get_entities_at_random_respects_floor_gating():
    ''' entities gated to a later floor should not be chosen early '''
    chances = {
        0: [(entity_factories.orc, 100)],
        10: [(entity_factories.troll, 100)],
    }

    chosen = get_entities_at_random(chances, number_of_entities=5, floor=0)

    assert len(chosen) == 5
    assert all(entity is entity_factories.orc for entity in chosen)


def test_get_entities_at_random_returns_requested_count():
    ''' should always return exactly number_of_entities picks '''
    chances = {0: [(entity_factories.orc, 50), (entity_factories.troll, 50)]}

    chosen = get_entities_at_random(chances, number_of_entities=8, floor=0)

    assert len(chosen) == 8

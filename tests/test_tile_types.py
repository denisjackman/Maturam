'''
    Tests for tile_types.py
'''
import tile_types


def test_floor_is_walkable_and_transparent():
    ''' floor tiles should be walkable and not block sight '''
    assert bool(tile_types.floor["walkable"]) is True
    assert bool(tile_types.floor["transparent"]) is True


def test_wall_blocks_movement_and_sight():
    ''' wall tiles should block both movement and sight '''
    assert bool(tile_types.wall["walkable"]) is False
    assert bool(tile_types.wall["transparent"]) is False


def test_down_stairs_is_walkable():
    ''' down-stairs tiles should be walkable '''
    assert bool(tile_types.down_stairs["walkable"]) is True


def test_new_tile_builds_expected_fields():
    ''' new_tile() should populate the walkable/transparent/dark/light fields '''
    tile = tile_types.new_tile(
        walkable=True,
        transparent=False,
        dark=(ord("x"), (1, 2, 3), (4, 5, 6)),
        light=(ord("y"), (7, 8, 9), (10, 11, 12)),
    )

    assert bool(tile["walkable"]) is True
    assert bool(tile["transparent"]) is False
    assert tile["dark"]["ch"] == ord("x")
    assert tuple(tile["light"]["fg"]) == (7, 8, 9)

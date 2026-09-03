'''
    Tests for components/level.py
'''
from components.level import Level


def test_experience_to_next_level():
    ''' threshold should be level_up_base + current_level * level_up_factor '''
    level = Level(current_level=1, level_up_base=0, level_up_factor=150)
    assert level.experience_to_next_level == 150


def test_requires_level_up_threshold():
    ''' requires_level_up should flip once xp exceeds the threshold '''
    level = Level(current_level=1, level_up_base=0, level_up_factor=150)

    level.current_xp = 150
    assert level.requires_level_up is False

    level.current_xp = 151
    assert level.requires_level_up is True


def test_add_xp_of_zero_is_a_no_op(player):
    ''' add_xp(0) should leave current_xp unchanged '''
    player.level.add_xp(0)
    assert player.level.current_xp == 0


def test_increase_level_carries_over_excess_xp(player):
    ''' increase_level() should keep xp earned beyond the threshold '''
    threshold = player.level.experience_to_next_level
    player.level.current_xp = threshold + 20

    player.level.increase_level()

    assert player.level.current_level == 2
    assert player.level.current_xp == 20


def test_increase_max_hp_heals_and_levels_up(player):
    ''' increase_max_hp() should grow max_hp and advance the level '''
    start_max_hp = player.fighter.max_hp
    start_level = player.level.current_level
    player.level.current_xp = player.level.experience_to_next_level + 1

    player.level.increase_max_hp(20)

    assert player.fighter.max_hp == start_max_hp + 20
    assert player.level.current_level == start_level + 1

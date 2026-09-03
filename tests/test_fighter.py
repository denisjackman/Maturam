'''
    Tests for components/fighter.py
'''
import entity_factories


def test_hp_clamps_to_max(player):
    ''' hp should never be set above max_hp '''
    player.fighter.hp = 9999
    assert player.fighter.hp == player.fighter.max_hp


def test_hp_clamps_to_zero_minimum(player):
    ''' hp should never be set below zero '''
    player.fighter.hp = -50
    assert player.fighter.hp == 0


def test_heal_does_not_exceed_max(player):
    ''' heal() should cap recovered hp at max_hp '''
    player.fighter.hp = player.fighter.max_hp - 5
    recovered = player.fighter.heal(20)

    assert recovered == 5
    assert player.fighter.hp == player.fighter.max_hp


def test_heal_at_full_health_recovers_nothing(player):
    ''' heal() at full hp should report zero recovered '''
    assert player.fighter.heal(10) == 0


def test_take_damage_reduces_hp(player):
    ''' take_damage() should subtract from current hp '''
    start_hp = player.fighter.hp
    player.fighter.take_damage(4)
    assert player.fighter.hp == start_hp - 4


def test_power_and_defense_include_equipment_bonus(player):
    ''' power/defense should include bonuses from equipped items '''
    dagger = entity_factories.dagger.spawn(player.gamemap, 0, 0)
    player.equipment.equip_to_slot("weapon", dagger, add_message=False)

    assert player.fighter.power == player.fighter.base_power + 2
    assert player.fighter.defense == player.fighter.base_defense


def test_death_marks_actor_dead_and_awards_xp_to_player(player, orc):
    ''' dropping an actor's hp to zero should kill it and award xp '''
    expected_xp = entity_factories.orc.level.xp_given

    orc.fighter.hp -= 9999  # drives hp to 0, triggering die() via the setter

    assert orc.is_alive is False
    assert orc.name == "remains of Orc"
    assert player.level.current_xp == expected_xp

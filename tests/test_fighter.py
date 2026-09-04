'''
    Tests for components/fighter.py
'''
import entity_factories
import scoring
from components.ai import ConfusedEnemy


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


def test_player_death_stores_the_final_score_entry(engine, player):
    '''
        dying should snapshot the leaderboard entry on the engine so it can't
        drift from what gets shown on the game-over screen - regression for a
        bug where the displayed score kept counting turns that happened after
        death, landing 1 higher than the score actually recorded
    '''
    engine.turn_count = 10
    player.level.current_xp = 5
    engine.game_world.current_floor = 1

    player.fighter.hp -= 9999  # drives hp to 0, triggering die() via the setter

    recorded_score = engine.final_score_entry.score
    engine.turn_count += 1  # the turn loop still increments the count after death

    assert scoring.calculate_score(engine) == recorded_score + 1
    assert engine.final_score_entry.score == recorded_score


def test_regen_interval_scales_with_max_hp(player):
    ''' higher max_hp (constitution) should mean a shorter regen interval '''
    player.fighter.max_hp = 15
    slow_interval = player.fighter.regen_interval

    player.fighter.max_hp = 60
    fast_interval = player.fighter.regen_interval

    assert fast_interval < slow_interval


def test_regen_interval_is_floored(player):
    ''' regen_interval should never drop below the floor, however high max_hp goes '''
    player.fighter.max_hp = 10000
    assert player.fighter.regen_interval == 5


def test_tick_regen_does_nothing_at_full_health(player):
    ''' tick_regen should not accumulate progress once at full hp '''
    player.fighter.tick_regen()
    assert player.fighter.regen_progress == 0


def test_tick_regen_heals_after_enough_safe_turns(player):
    ''' after regen_interval safe ticks, hp should go up by 1 '''
    player.fighter.hp = player.fighter.max_hp - 1
    interval = player.fighter.regen_interval

    for _ in range(interval - 1):
        player.fighter.tick_regen()
    assert player.fighter.hp == player.fighter.max_hp - 1  # not yet

    player.fighter.tick_regen()
    assert player.fighter.hp == player.fighter.max_hp


def test_tick_regen_paused_when_hostile_visible(player, orc):
    ''' regen progress should not advance while a hostile actor is visible '''
    player.fighter.hp = player.fighter.max_hp - 1
    player.gamemap.visible[orc.x, orc.y] = True

    for _ in range(player.fighter.regen_interval):
        player.fighter.tick_regen()

    assert player.fighter.hp == player.fighter.max_hp - 1
    assert player.fighter.regen_progress == 0


def test_tick_regen_paused_when_incapacitated(player):
    ''' regen progress should not advance while confused '''
    player.fighter.hp = player.fighter.max_hp - 1
    player.ai = ConfusedEnemy(player, previous_ai=player.ai, turns_remaining=5)

    for _ in range(player.fighter.regen_interval):
        player.fighter.tick_regen()

    assert player.fighter.hp == player.fighter.max_hp - 1
    assert player.fighter.regen_progress == 0

'''
    Tests for components/equipment.py
'''
import entity_factories


def test_no_equipment_gives_zero_bonus(player):
    ''' an actor with nothing equipped should have zero bonuses '''
    assert player.equipment.defense_bonus == 0
    assert player.equipment.power_bonus == 0


def test_equip_to_slot_applies_bonus(player):
    ''' equipping an item should apply its bonus and mark it equipped '''
    dagger = entity_factories.dagger.spawn(player.gamemap, 0, 0)

    player.equipment.equip_to_slot("weapon", dagger, add_message=False)

    assert player.equipment.weapon is dagger
    assert player.equipment.power_bonus == 2
    assert player.equipment.item_is_equipped(dagger) is True


def test_toggle_equip_unequips_when_already_worn(player):
    ''' toggling an equipped item should remove it and its bonus '''
    dagger = entity_factories.dagger.spawn(player.gamemap, 0, 0)
    player.equipment.equip_to_slot("weapon", dagger, add_message=False)

    player.equipment.toggle_equip(dagger, add_message=False)

    assert player.equipment.weapon is None
    assert player.equipment.power_bonus == 0


def test_toggle_equip_swaps_existing_weapon(player):
    ''' toggling a new weapon should replace the one already worn '''
    dagger = entity_factories.dagger.spawn(player.gamemap, 0, 0)
    sword = entity_factories.sword.spawn(player.gamemap, 0, 0)
    player.equipment.equip_to_slot("weapon", dagger, add_message=False)

    player.equipment.toggle_equip(sword, add_message=False)

    assert player.equipment.weapon is sword
    assert player.equipment.power_bonus == 4


def test_equip_message_is_logged(player):
    ''' equip_to_slot() with add_message=True should log a message '''
    dagger = entity_factories.dagger.spawn(player.gamemap, 0, 0)

    player.equipment.equip_to_slot("weapon", dagger, add_message=True)

    last_message = player.gamemap.engine.message_log.messages[-1]
    assert last_message.plain_text == "You equip the Dagger."

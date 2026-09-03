'''
    Tests for entity_factories.py.

    The entities defined there (player, orc, dagger, ...) are module-level
    singletons meant to be cloned via Entity.spawn() rather than used
    directly - these guard against a spawned copy ever leaking state back
    into the shared template.
'''
import entity_factories

ACTOR_TEMPLATES = [
    entity_factories.player,
    entity_factories.orc,
    entity_factories.troll,
]

ITEM_TEMPLATES = [
    entity_factories.confusion_scroll,
    entity_factories.fireball_scroll,
    entity_factories.health_potion,
    entity_factories.lightning_scroll,
    entity_factories.dagger,
    entity_factories.sword,
    entity_factories.leather_armor,
    entity_factories.chain_mail,
]


def test_every_actor_template_spawns_at_the_given_position(gamemap):
    ''' every actor template should spawn cleanly at the given position '''
    for index, template in enumerate(ACTOR_TEMPLATES):
        clone = template.spawn(gamemap, index, index)
        assert (clone.x, clone.y) == (index, index)
        assert clone in gamemap.entities


def test_every_item_template_spawns_at_the_given_position(gamemap):
    ''' every item template should spawn cleanly at the given position '''
    for index, template in enumerate(ITEM_TEMPLATES):
        clone = template.spawn(gamemap, index, index)
        assert (clone.x, clone.y) == (index, index)
        assert clone in gamemap.entities


def test_mutating_a_spawned_actor_does_not_affect_the_template(gamemap):
    ''' mutating a spawned clone should never leak back into the template '''
    original_hp = entity_factories.orc.fighter.hp

    clone = entity_factories.orc.spawn(gamemap, 0, 0)
    clone.fighter.hp = 1

    assert entity_factories.orc.fighter.hp == original_hp

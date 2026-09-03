'''
    Shared pytest fixtures for the Maturam test suite.
'''
# Fixtures depending on other fixtures (e.g. gamemap(engine)) necessarily
# shadow the outer fixture-function name - that's the pytest fixture
# pattern, not a real redefinition bug.
# pylint: disable=W0621
import pytest

import entity_factories
from game_map import GameMap
from message_log import MessageLog


class FakeEngine:
    '''
        Minimal stand-in for engine.Engine - just enough (message_log,
        player) to satisfy BaseComponent.engine without needing a real
        tcod rendering context.
    '''
    def __init__(self):
        self.message_log = MessageLog()
        self.player = None


@pytest.fixture
def engine():
    '''A minimal engine double.'''
    return FakeEngine()


@pytest.fixture
def gamemap(engine):
    '''A small GameMap wired to the fake engine.'''
    return GameMap(engine=engine, width=20, height=20)


@pytest.fixture
def player(gamemap):
    '''A spawned player actor, registered as the engine's active player.'''
    actor = entity_factories.player.spawn(gamemap, 5, 5)
    gamemap.engine.player = actor
    return actor


@pytest.fixture
def orc(gamemap):
    '''A spawned orc actor.'''
    return entity_factories.orc.spawn(gamemap, 10, 10)

'''
    This is a factory for entities
'''
from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor
from colours import (
    WHITE,
    ORC_GREEN,
    TROLL_GREEN
)
player = Actor(
    char="@",
    color=WHITE,
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
)


orc = Actor(
    char="o",
    color=ORC_GREEN,
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
)

troll = Actor(
    char="T",
    color=TROLL_GREEN,
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
)

'''
    This is a factory for entities
'''
from components.ai import HostileEnemy
from components.consumable import HealingConsumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item

from colours import (
    WHITE,
    ORC_GREEN,
    TROLL_GREEN,
    HEALING_POTION
)

player = Actor(
    char="@",
    color=WHITE,
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="o",
    color=ORC_GREEN,
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
)

troll = Actor(
    char="T",
    color=TROLL_GREEN,
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
)

health_potion = Item(
    char="!",
    color=HEALING_POTION,
    name="Health Potion",
    consumable=HealingConsumable(amount=4),
)

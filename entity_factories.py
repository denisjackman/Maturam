'''
    This is a factory for entities
'''
from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

import colours

player = Actor(
    char="@",
    color=colours.WHITE,
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    color=colours.ORC_GREEN,
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

troll = Actor(
    char="T",
    color=colours.TROLL_GREEN,
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

confusion_scroll = Item(
    char="~",
    color=colours.CONFUSION_SCROLL,
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    char="~",
    color=colours.RED,
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

health_potion = Item(
    char="!",
    color=colours.HEALING_POTION,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="~",
    color=colours.LIGHTNING_SCROLL,
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)


dagger = Item(
    char="/",
    color=colours.WEAPONS_COLOUR,
    name="Dagger",
    equippable=equippable.Dagger()
)

sword = Item(
    char="/",
    color=colours.WEAPONS_COLOUR,
    name="Sword",
    equippable=equippable.Sword()
)

leather_armor = Item(
    char="[",
    color=colours.ARMOR_COLOUR,
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[",
    color=colours.ARMOR_COLOUR,
    name="Chain Mail",
    equippable=equippable.ChainMail()
)

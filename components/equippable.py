'''
    equippable.py
'''
from __future__ import annotations

from typing import TYPE_CHECKING

from equipment_types import EquipmentType
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    '''
        Equippable.owner - The owner of this equippable component.
    '''
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
    ):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


class Dagger(Equippable):
    '''
        Dagger.owner - The owner of this equippable component.
    '''
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)


class Sword(Equippable):
    '''
        Sword.owner - The owner of this equippable component.
    '''
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)


class LeatherArmor(Equippable):
    '''
        LeatherArmor.owner - The owner of this equippable component.
    '''
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)


class ChainMail(Equippable):
    '''
        ChainMail.owner - The owner of this equippable component.
    '''
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)

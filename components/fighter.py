'''
    fighter class
'''
from __future__ import annotations

from typing import TYPE_CHECKING
import colours
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    '''
        fighter class
    '''
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self) -> int:
        '''
            hit point functions
        '''
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        '''
            defense property
        '''
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        '''
            power property
        '''
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        '''
            defense bonus
        '''
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        return 0

    @property
    def power_bonus(self) -> int:
        '''
            power bonus
        '''
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        return 0

    def die(self) -> None:
        '''
            die method
        '''
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = colours.PLAYER_DIE
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = colours.ENEMY_DIE

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        '''
            heal function
        '''
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        '''
            take damage
        '''
        self.hp -= amount

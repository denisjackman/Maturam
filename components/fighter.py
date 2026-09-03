'''
    fighter class
'''
from __future__ import annotations

from typing import TYPE_CHECKING
import colours
import scoring
from components.ai import ConfusedEnemy
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

# Passive regen ticks 1 HP every `regen_interval` turns, and regen_interval
# scales down as max_hp (constitution) grows, so a tankier build heals
# noticeably faster - floored at REGEN_MIN_TURNS so it can't become instant.
REGEN_BASE_TURNS = 300
REGEN_MIN_TURNS = 5


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
        self.regen_progress = 0

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
            scoring.record_score(self.engine)
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

        new_hp_value = min(self.hp + amount, self.max_hp)

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        '''
            take damage
        '''
        self.hp -= amount

    @property
    def regen_interval(self) -> int:
        '''
            turns needed per 1 HP of passive regen, based on max_hp
        '''
        return max(REGEN_MIN_TURNS, REGEN_BASE_TURNS // self.max_hp)

    @property
    def is_incapacitated(self) -> bool:
        '''
            True while a condition (e.g. confusion) should block passive regen
        '''
        return isinstance(self.parent.ai, ConfusedEnemy)

    def is_hostile_visible(self) -> bool:
        '''
            True if any other living actor is currently in this actor's FOV
        '''
        for actor in self.gamemap.actors:
            if actor is not self.parent and self.gamemap.visible[actor.x, actor.y]:
                return True
        return False

    def tick_regen(self) -> None:
        '''
            passively regenerate 1 HP every regen_interval turns, but only
            while at less than full health, not incapacitated by a
            condition, and no hostile actor is visible
        '''
        if self.hp <= 0 or self.hp >= self.max_hp:
            self.regen_progress = 0
            return

        if self.is_incapacitated or self.is_hostile_visible():
            self.regen_progress = 0
            return

        self.regen_progress += 1
        if self.regen_progress >= self.regen_interval:
            self.regen_progress = 0
            self.heal(1)

'''
    base component class
'''
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseComponent:
    '''
        base component
    '''
    parent: Entity  # Owning entity instance.

    @property
    def gamemap(self) -> GameMap:
        '''
            gamemap property
        '''
        return self.parent.gamemap

    @property
    def engine(self) -> Engine:
        '''
            the engine
        '''
        return self.gamemap.engine

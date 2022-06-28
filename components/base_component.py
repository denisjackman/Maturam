'''
    base component class
'''
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class BaseComponent:
    '''
        base component
    '''
    entity: Entity  # Owning entity instance.

    @property
    def engine(self) -> Engine:
        '''
            the engine
        '''
        return self.entity.gamemap.engine

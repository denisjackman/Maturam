'''
    This contains all the action classes
'''

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:  # pylint: disable=R0903
    '''
        This is the generic action class
    '''
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):  # pylint: disable=R0903
    '''
        this is the class for the escape button
    '''
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class MovementAction(Action):  # pylint: disable=R0903
    '''
        this is the class for a movement action
    '''
    def __init__(self, dx: int, dy: int):  # pylint: disable C0103
        super().__init__()

        self.dx = dx  # pylint: disable C0103
        self.dy = dy  # pylint: disable C0103

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        entity.move(self.dx, self.dy)

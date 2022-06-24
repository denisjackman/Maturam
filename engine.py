'''
    This is the game engine module
'''

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

from typing import Iterable, Any


class Engine:
    '''
        This is the game engine class
    '''
    def __init__(self,
                 event_handler: EventHandler,
                 game_map: GameMap,
                 player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        '''
            This handles events
        '''
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        '''
            This is the rendering function
        '''
        self.game_map.render(console)
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()

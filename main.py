#!/usr/bin/env python3
'''
    This is the main test code for the maturam game
'''

import tcod
from colours import (
    WHITE,
    YELLOW
)
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon


def main() -> None:  # pylint: disable=R0914
    '''
        This is the main function
    '''
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(
                'images/dejavu10x10_gs_tc.png',
                32,
                8,
                tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(screen_width / 2),
                    int(screen_height / 2),
                    "@", WHITE)
    npc = Entity(int(screen_width / 2 - 5),
                 int(screen_height / 2),
                 "@", YELLOW)
    entities = {npc, player}
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )

    engine = Engine(entities=entities,
                    event_handler=event_handler,
                    game_map=game_map,
                    player=player)

    with tcod.context.new(
        width=screen_width,
        height=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()

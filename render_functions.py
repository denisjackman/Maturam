'''
    render functions
'''
from __future__ import annotations

from typing import TYPE_CHECKING

import colours

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    '''
        get name at location
    '''
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()

def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    '''
        render the health bar
    '''
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0,
                      y=45,
                      width=total_width,
                      height=1,
                      ch=1,
                      bg=colours.BAR_EMPTY)

    if bar_width > 0:
        console.draw_rect(
            x=0,
            y=45,
            width=bar_width,
            height=1,
            ch=1,
            bg=colours.BAR_FILLED
        )

    console.print(
        x=1,
        y=45,
        string=f"HP: {current_value}/{maximum_value}",
        fg=colours.BAR_TEXT
    )

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    '''
        render the names to the logger
    '''
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)

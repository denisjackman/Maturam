"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
from tcod import libtcodpy

import colours
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("images/menu_background.png")[:, :, :3]

MAX_NAME_LENGTH = 20


def new_game(player_name: str = "Player") -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)
    player.name = player_name

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    engine.game_world.generate_floor()
    engine.update_fov()
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", colours.WELCOME_TEXT
    )
    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "TOMBS OF THE ANCIENT KINGS",
            fg=colours.MENU_TITLE,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By (Your name here)",
            fg=colours.MENU_TITLE,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            [
                "[N] Play a new game",
                "[C] Continue last game",
                "[L] View leaderboard",
                "[Q] Quit",
            ]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=colours.MENU_TEXT,
                bg=colours.BLACK,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(  # pylint: disable=W0221
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        ''' key down '''
        if event.sym in (tcod.event.KeySym.Q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        if event.sym == tcod.event.KeySym.C:
            try:
                return input_handlers.MainGameEventHandler(load_game("saves/savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:  # pylint: disable=W0703
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.N:
            return NamePromptEventHandler(self)
        elif event.sym == tcod.event.KeySym.L:
            return input_handlers.LeaderboardViewEventHandler(self)

        return None


class NamePromptEventHandler(input_handlers.BaseEventHandler):
    """Ask the player to name their character before a new game starts."""

    def __init__(self, parent_handler: input_handlers.BaseEventHandler):
        self.parent = parent_handler
        self.name = ""

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the parent dimmed, with a name-entry box on top."""
        self.parent.on_render(console)
        console.rgb["fg"] //= 8
        console.rgb["bg"] //= 8

        width = 40
        height = 5
        x = console.width // 2 - width // 2
        y = console.height // 2 - height // 2

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title="Name your character",
            clear=True,
            fg=colours.WHITE,
            bg=colours.BLACK,
        )
        console.print(x=x + 1, y=y + 2, string=f"{self.name}_")
        console.print(
            x=x + 1,
            y=y + 3,
            string="[Enter] confirm  [Esc] cancel",
            fg=colours.MENU_TEXT,
        )

    def ev_textinput(  # pylint: disable=W0221
        self, event: tcod.event.TextInput
    ) -> Optional[input_handlers.BaseEventHandler]:
        ''' append typed characters to the name, up to the length limit '''
        if len(self.name) < MAX_NAME_LENGTH:
            self.name += event.text

    def ev_keydown(  # pylint: disable=W0221
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        ''' backspace edits the name, enter confirms, escape cancels '''
        if event.sym == tcod.event.KeySym.BACKSPACE:
            self.name = self.name[:-1]
        elif event.sym == tcod.event.KeySym.ESCAPE:
            return self.parent
        elif event.sym in (tcod.event.KeySym.RETURN, tcod.event.KeySym.KP_ENTER):
            player_name = self.name.strip() or "Player"
            return input_handlers.MainGameEventHandler(new_game(player_name))
        return None

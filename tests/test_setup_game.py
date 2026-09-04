'''
    Tests for setup_game.py - new game setup and the character-naming prompt.
'''
import tcod.event

import input_handlers
import setup_game


def test_new_game_defaults_to_player_name():
    ''' new_game() with no name should keep the default "Player" '''
    engine = setup_game.new_game()
    assert engine.player.name == "Player"


def test_new_game_uses_the_given_player_name():
    ''' new_game() should name the player entity after the given name '''
    engine = setup_game.new_game("Thundermaw")
    assert engine.player.name == "Thundermaw"


def test_name_prompt_appends_typed_characters():
    ''' ev_textinput should build up the name one character at a time '''
    prompt = setup_game.NamePromptEventHandler(setup_game.MainMenu())

    for char in "Zara":
        prompt.ev_textinput(tcod.event.TextInput(text=char))

    assert prompt.name == "Zara"


def test_name_prompt_stops_appending_at_the_length_limit():
    ''' typed characters beyond MAX_NAME_LENGTH should be dropped '''
    prompt = setup_game.NamePromptEventHandler(setup_game.MainMenu())
    prompt.name = "a" * setup_game.MAX_NAME_LENGTH

    prompt.ev_textinput(tcod.event.TextInput(text="x"))

    assert prompt.name == "a" * setup_game.MAX_NAME_LENGTH


def test_name_prompt_backspace_removes_last_character():
    ''' backspace should trim one character off the end of the name '''
    prompt = setup_game.NamePromptEventHandler(setup_game.MainMenu())
    prompt.name = "Zara"

    prompt.ev_keydown(
        tcod.event.KeyDown(
            scancode=tcod.event.Scancode.BACKSPACE,
            sym=tcod.event.KeySym.BACKSPACE,
            mod=tcod.event.Modifier.NONE,
        )
    )

    assert prompt.name == "Zar"


def test_name_prompt_escape_returns_to_parent():
    ''' escape should cancel back to the handler that opened the prompt '''
    parent = setup_game.MainMenu()
    prompt = setup_game.NamePromptEventHandler(parent)

    result = prompt.ev_keydown(
        tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE,
            sym=tcod.event.KeySym.ESCAPE,
            mod=tcod.event.Modifier.NONE,
        )
    )

    assert result is parent


def test_name_prompt_enter_starts_a_game_with_the_typed_name():
    ''' confirming a typed name should start a new game with that character name '''
    prompt = setup_game.NamePromptEventHandler(setup_game.MainMenu())
    prompt.name = "Zara"

    result = prompt.ev_keydown(
        tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RETURN,
            sym=tcod.event.KeySym.RETURN,
            mod=tcod.event.Modifier.NONE,
        )
    )

    assert isinstance(result, input_handlers.MainGameEventHandler)
    assert result.engine.player.name == "Zara"


def test_name_prompt_enter_with_a_blank_name_falls_back_to_player():
    ''' confirming without typing a name should still start a game, as "Player" '''
    prompt = setup_game.NamePromptEventHandler(setup_game.MainMenu())

    result = prompt.ev_keydown(
        tcod.event.KeyDown(
            scancode=tcod.event.Scancode.RETURN,
            sym=tcod.event.KeySym.RETURN,
            mod=tcod.event.Modifier.NONE,
        )
    )

    assert result.engine.player.name == "Player"


def test_main_menu_n_opens_the_name_prompt():
    ''' pressing N at the main menu should open the naming prompt, not start the game directly '''
    menu = setup_game.MainMenu()

    result = menu.ev_keydown(
        tcod.event.KeyDown(
            scancode=tcod.event.Scancode.N,
            sym=tcod.event.KeySym.N,
            mod=tcod.event.Modifier.NONE,
        )
    )

    assert isinstance(result, setup_game.NamePromptEventHandler)

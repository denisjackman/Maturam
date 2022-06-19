#!/usr/bin/env python3
'''
    this is the input handlers class
'''
from typing import Optional
import tcod.event
from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    '''
        this classes handles events
    '''
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:  # pylint: disable=R0201
        '''
            this is for the quit event
        '''
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:  # pylint: disable=R0201
        '''
            this is for a key press event
        '''
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(player_x=0, player_y=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(player_x=0, player_y=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(player_x=-1, player_y=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(player_x=1, player_y=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action

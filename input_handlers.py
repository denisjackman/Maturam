#!/usr/bin/env python3
'''
    this is the input handlers class
'''
from typing import Optional
import tcod.event
from actions import Action, BumpAction, EscapeAction


class EventHandler(tcod.event.EventDispatch[Action]):
    '''
        this classes handles events
    '''
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        '''
            this is for the quit event
        '''
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        '''
            this is for a key press event
        '''
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action

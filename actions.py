'''
    This contains all the action classes
'''

class Action:  # pylint: disable=R0903
    '''
        This is the generic action class
    '''

class EscapeAction(Action):  # pylint: disable=R0903
    '''
        this is the class for the escape button
    '''

class MovementAction(Action):  # pylint: disable=R0903
    '''
        this is the class for a movement action
    '''
    def __init__(self, player_x: int, player_y: int):
        super().__init__()

        self.player_x = player_x
        self.player_y = player_y

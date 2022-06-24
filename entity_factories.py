from entity import Entity
from colours import (
    WHITE,
    ORC_GREEN,
    TROLL_GREEN
)

player = Entity(char="@",
                color=WHITE,
                name="Player",
                blocks_movement=True)

orc = Entity(char="o",
             color=ORC_GREEN,
             name="Orc",
             blocks_movement=True)
troll = Entity(char="T",
               color=TROLL_GREEN,
               name="Troll",
               blocks_movement=True)

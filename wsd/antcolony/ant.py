import random
from enum import Enum

from wsd.antcolony.graph import Node


class AntModeEnum(Enum):
    EXPLORE = 0
    RETURN = 1


class Ant:
    """Representation of an ant.

    Attributes:
        nest: home nest of the ant
        current_node: the node on which the ant is currently sitting
        life: remaining life of the ant
        energy: amount of energy the ant is carrying
        mode: expore or return
    """

    def __init__(self, nest: Node, life: int) -> None:
        self.nest = nest
        self.current_node = nest
        self.life = life
        self.energy: int = 0
        self.mode = AntModeEnum.EXPLORE

    def creates_bridge(self, next_node: Node) -> bool:
        """Check if moving the ant on the next node would generate a bridge."""
        return next_node.is_potential_friend_nest(
            self.nest
        ) and not next_node.is_adjacent(self.nest)

    def odour_deposit(self, pct: float) -> list[int]:
        """Return random odour components deposited by the ant."""
        odour = self.nest.odour
        num_deposit = int(len(odour) * pct)
        return [odour[idx] for idx in random.sample(range(len(odour)), num_deposit)]

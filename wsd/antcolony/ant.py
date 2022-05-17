from wsd.antcolony.graph import Node


class Ant:
    def __init__(self, nest: Node) -> None:
        self.nest = nest
        self.current_node = nest

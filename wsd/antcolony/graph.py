from __future__ import annotations

from enum import Enum

from nltk.corpus.reader.wordnet import Synset

from wsd.data import Document
from wsd.data.document import Item


class NodeTypeEnum(Enum):
    NEST = 0
    COMMON = 1


class Node:
    def __init__(
        self, type: NodeTypeEnum, parent: None | Node = None, syn: None | Synset = None
    ) -> None:
        self.type = type
        self.parent = parent
        self.odour: list[int] = []
        self.adj_edges: list[Edge] = []
        self.syn = syn
        self.energy: int = 0

    def add_edge(self, edge: Edge) -> None:
        self.adj_edges.append(edge)

    def remove_edge(self, edge: Edge) -> None:
        self.adj_edges.remove(edge)

    def update_odour(self, new_components: list[int], max_length: int) -> None:
        if self.type == NodeTypeEnum.NEST:
            return
        self.odour.extend(new_components)
        if len(self.odour) > max_length:
            self.odour = self.odour[-max_length:]

    def is_potential_friend_nest(self, other_nest: Node) -> bool:
        return (
            self.type == NodeTypeEnum.NEST  # is a nest
            and self is not other_nest  # is not the same nest
            and self.parent is not other_nest.parent  # is not an enemy nest
        )

    def is_adjacent(self, other_node: Node) -> bool:
        for edge in self.adj_edges:
            if other_node is edge.other(self):
                return True
        return False


class Edge:
    def __init__(self, nodes: tuple[Node, Node], pheromone: float = 0) -> None:
        self.nodes = nodes
        self.pheromone = pheromone

    def other(self, node: Node) -> Node:
        return self.nodes[0] if self.nodes[1] is node else self.nodes[1]


class Graph:
    def __init__(self, document: Document) -> None:
        root = Node(type=NodeTypeEnum.COMMON)
        self.nodes: list[Node] = [root]
        self.edges: list[Edge] = []
        self.bridges: list[Edge] = []
        self.item2node: dict[Item, Node] = {}

        for sentence in document:
            sentence_node = Node(type=NodeTypeEnum.COMMON, parent=root)
            self.nodes.append(sentence_node)
            self.add_edge(root, sentence_node)

            for item in sentence:
                word_node = Node(type=NodeTypeEnum.COMMON, parent=sentence_node)
                self.nodes.append(word_node)
                self.item2node[item] = word_node
                self.add_edge(sentence_node, word_node)

                for syn in item.synsets:
                    syn_node = Node(type=NodeTypeEnum.NEST, parent=word_node, syn=syn)
                    self.nodes.append(syn_node)
                    self.add_edge(word_node, syn_node)

    def add_edge(self, node1: Node, node2: Node) -> None:
        edge = Edge(nodes=(node1, node2))
        self.edges.append(edge)
        node1.add_edge(edge)
        node2.add_edge(edge)

    def add_bridge(self, nest1: Node, nest2: Node) -> Edge:
        bridge = Edge(nodes=(nest1, nest2))
        self.bridges.append(bridge)
        nest1.add_edge(bridge)
        nest2.add_edge(bridge)
        return bridge

    def remove_bridge(self, bridge: Edge) -> None:
        self.bridges.remove(bridge)
        bridge.nodes[0].remove_edge(bridge)
        bridge.nodes[1].remove_edge(bridge)

from __future__ import annotations

from enum import Enum

from nltk.corpus.reader.wordnet import Synset

from wsd.data import Document


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

    def add_edge(self, edge: Edge) -> None:
        self.adj_edges.append(edge)

    def update_odour(self, new_components: list[int], max_length: int) -> None:
        self.odour.extend(new_components)
        if len(self.odour) > max_length:
            self.odour = self.odour[-max_length:]


class Edge:
    def __init__(self, nodes: tuple[Node, Node], pheromone: int = 0) -> None:
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

        def add_edge(node1: Node, node2: Node):
            edge = Edge(nodes=(node1, node2))
            self.edges.append(edge)
            node1.add_edge(edge)
            node2.add_edge(edge)

        for sentence in document:
            sentence_node = Node(type=NodeTypeEnum.COMMON, parent=root)
            add_edge(root, sentence_node)

            for item in sentence:
                word_node = Node(type=NodeTypeEnum.COMMON, parent=sentence_node)
                add_edge(sentence_node, word_node)

                for syn in item.synsets:
                    syn_node = Node(type=NodeTypeEnum.NEST, parent=word_node, syn=syn)
                    add_edge(word_node, syn_node)

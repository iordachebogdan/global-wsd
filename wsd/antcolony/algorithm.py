import itertools
import math
from collections import Counter

from nltk.corpus.reader.wordnet import Synset

from wsd.antcolony.ant import Ant, AntModeEnum
from wsd.antcolony.graph import Edge, Graph, Node, NodeTypeEnum
from wsd.config.algorithmconfig import AntcolonyAlgorithmConfig
from wsd.config.leskconfig import LeskConfig
from wsd.data import Document
from wsd.data.document import Item
from wsd.lesk.leskengine import LeskEngine
from wsd.util.helpers import discrete_random_variable, normalize

EPS: float = 1e-2


class Algorithm:
    def __init__(
        self, config: AntcolonyAlgorithmConfig, lesk_config: LeskConfig
    ) -> None:
        self.config = config
        self.lesk_engine = LeskEngine(lesk_config)

    def run(self, document: Document) -> dict[Item, Synset]:
        graph = self.init_graph(document)
        ants: list[Ant] = []

        best_score: int = -1
        best_mapping: dict[Item, Synset]
        for cycle in range(self.config.total_cycles):
            if cycle % 10 == 0:
                print(f"Running cycle {cycle + 1} out of {self.config.total_cycles}...")

            # (1) eliminate dead ants and bridges with no pheromone
            ants = self.remove_dead_ants(ants)
            graph = self.remove_no_pheromone_bridges(graph)

            # (2) for each nest, potentially produce an ant
            for node in graph.nodes:
                if produced_ant := self.try_produce_ant(node):
                    ants.append(produced_ant)

            # (3) for each ant: determine its mode; make it move;
            # potentially create an interpretative bridge
            for ant in ants:
                self.move_ant(ant, graph)

            # (4) update the environmet (pheromone evaporation)
            for edge in itertools.chain(graph.edges, graph.bridges):
                edge.pheromone *= 1 - self.config.evaporation_rate
                if edge.pheromone < EPS:
                    edge.pheromone = 0

            # global evaluation
            current_mapping = self.extract_senses(graph)
            score = self.global_evaluation(list(current_mapping.values()))
            if score > best_score:
                best_score = score
                best_mapping = current_mapping

        return best_mapping

    def extract_senses(self, graph: Graph) -> dict[Item, Synset]:
        mapped_senses: dict[Item, Synset] = {}
        for item, node in graph.item2node.items():
            nests = [
                nest
                for edge in node.adj_edges
                if (nest := edge.other(node)).type == NodeTypeEnum.NEST
            ]
            max_energy = -1
            for i, nest in enumerate(nests):
                if max_energy < nest.energy:
                    max_energy = nest.energy
                    mapped_senses[item] = item.synsets[i]
        return mapped_senses

    def global_evaluation(self, senses: list[Synset]) -> int:
        score = 0
        for i, first in enumerate(senses):
            for second in senses[i + 1 :]:
                score += self.lesk_engine.compute_lesk(first, second)
        return score

    def init_graph(self, document: Document) -> Graph:
        graph = Graph(document)
        for node in graph.nodes:
            node.energy = self.config.energy_node
            if node.type == NodeTypeEnum.NEST:
                self.compute_nest_odour(node)
        return graph

    def compute_nest_odour(self, nest: Node) -> None:
        extended_gloss = self.lesk_engine.get_extended_gloss(nest.syn)
        extended_gloss_counter = Counter(extended_gloss)
        nest.odour = [
            word_index
            for word_index, _ in extended_gloss_counter.most_common(
                self.config.max_odour
            )
        ]

    def remove_dead_ants(self, ants: list[Ant]) -> list[Ant]:
        for ant in ants:
            if ant.life == 0:
                ant.current_node.energy += ant.energy
        return [ant for ant in ants if ant.life]

    def remove_no_pheromone_bridges(self, graph: Graph) -> Graph:
        bridges_to_remove = [
            bridge for bridge in graph.bridges if bridge.pheromone < EPS
        ]
        for bridge in bridges_to_remove:
            graph.remove_bridge(bridge)
        return graph

    def try_produce_ant(self, node: Node) -> None | Ant:
        if node.type == NodeTypeEnum.COMMON or node.energy == 0:
            return None
        prob_produce = math.atan(node.energy) / math.pi + 0.5
        if discrete_random_variable([prob_produce]) == 0:
            node.energy -= 1
            return Ant(nest=node, life=self.config.ant_cycles)

    def move_ant(self, ant: Ant, graph: Graph) -> None:
        if ant.mode == AntModeEnum.EXPLORE:
            if (
                ant.energy == self.config.max_energy
                or discrete_random_variable([ant.energy / self.config.max_energy]) == 0
            ):
                ant.mode = AntModeEnum.RETURN

        routes = self._compute_routes(ant)
        picked_route = discrete_random_variable([w for _, w in routes[:-1]])
        next_edge = routes[picked_route][0]
        next_node = next_edge.other(ant.current_node)
        creates_bridge = ant.creates_bridge(next_node)

        # move ant
        ant.life -= 1
        ant.current_node = next_node
        # energy exchange
        self._energy_exchange(ant, next_node)
        # odour exchange
        next_node.update_odour(
            ant.odour_deposit(self.config.odour_deposit_pct), self.config.max_odour
        )
        # update pheromone on edge
        next_edge.pheromone += self.config.theta

        if creates_bridge:
            # move to home nest
            ant.current_node = ant.nest
            # exchange energy
            self._energy_exchange(ant, ant.nest)
            # create bridge
            bridge = graph.add_bridge(ant.nest, next_node)
            # add pheromone
            bridge.pheromone += self.config.theta

    def _compute_routes(self, ant: Ant) -> list[tuple[Edge, float]]:
        next_nodes: list[Node] = [
            edge.other(ant.current_node) for edge in ant.current_node.adj_edges
        ]
        eval_nodes = normalize(
            [self._eval_node(ant, next_node) for next_node in next_nodes]
        )
        eval_edges = normalize([edge.pheromone for edge in ant.current_node.adj_edges])
        for i, next_node in enumerate(next_nodes):
            if ant.creates_bridge(next_node):
                eval_edges[i] = 0
            elif ant.mode == AntModeEnum.EXPLORE:
                eval_edges[i] = 1 - eval_edges[i]

        total_eval = normalize(
            [
                eval_node + eval_edge
                for (eval_node, eval_edge) in zip(eval_nodes, eval_edges)
            ]
        )
        return list(zip(ant.current_node.adj_edges, total_eval))

    def _eval_node(self, ant: Ant, node: Node) -> int:
        if ant.mode == AntModeEnum.EXPLORE:
            return node.energy
        else:
            self.lesk_engine.compute_overlap(ant.nest.odour, node.odour)

    def _energy_exchange(self, ant: Ant, node: Node) -> None:
        if node is not ant.nest:
            energy = min(
                0,
                self.config.energy_ant,
                self.config.max_energy - ant.energy,
                node.energy,
            )
            ant.energy += energy
            node.energy -= energy
        else:
            node.energy += ant.energy
            ant.energy = 0
            ant.mode = AntModeEnum.EXPLORE

from nltk.corpus.reader.wordnet import Synset

from wsd.antcolony.graph import Graph, Node
from wsd.config.algorithmconfig import AntcolonyAlgorithmConfig
from wsd.config.leskconfig import LeskConfig
from wsd.data import Document
from wsd.lesk.leskengine import LeskEngine


class Algorithm:
    def __init__(
        self, config: AntcolonyAlgorithmConfig, lesk_config: LeskConfig
    ) -> None:
        self.config = config
        self.lesk_engine = LeskEngine(lesk_config)

    def run(self, document: Document) -> dict[str, Synset]:
        graph = Graph(document)

    def compute_nest_odour(self, nest: Node):
        extended_gloss = self.lesk_engine.get_extended_gloss(nest.syn)

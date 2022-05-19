from typing import Any
from xml.etree import ElementTree

from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset

from wsd.config.datasetconfig import XMLDatasetConfig
from wsd.data.datasetbase import DatasetBase
from wsd.data.document import Document, Item, Sentence
from wsd.util.helpers import xml_to_wn_pos


class XMLDataset(DatasetBase):
    def __init__(self, config: XMLDatasetConfig) -> None:
        self.documents: list[Document] = []

        id2syns: dict[str, list[Synset]] = {}
        with open(config.gs_path) as f:
            content = f.read()
            lines = [line.strip().split() for line in content.strip().split("\n")]
            for line in lines:
                id = line[0]
                syns = [wn.lemma_from_key(key).synset() for key in line[1:]]
                id2syns[id] = syns

        xml_tree = ElementTree.parse(config.docs_path)
        root = xml_tree.getroot()
        for text_node in root:
            self.documents.append(self.__class__.build_document(text_node, id2syns))

    @staticmethod
    def build_document(doc_node: Any, id2syns: dict[str, list[Synset]]) -> Document:
        document: Document = []
        for sentence_node in doc_node:
            sentence: Sentence = []
            for word_node in sentence_node:
                if word_node.tag != "instance":
                    continue
                attrs = word_node.attrib
                all_syns = wn.synsets(attrs["lemma"], pos=xml_to_wn_pos(attrs["pos"]))
                sentence.append(
                    Item(
                        id=attrs["id"],
                        lemma=attrs["lemma"],
                        pos=xml_to_wn_pos(attrs["pos"]),
                        synsets=all_syns,
                        accepted_synsets=id2syns[attrs["id"]],
                    )
                )
            if sentence:
                document.append(sentence)
        return document

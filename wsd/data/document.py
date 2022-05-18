from dataclasses import dataclass
from typing import TypeAlias

from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset


@dataclass(frozen=True)
class Item:
    id: str
    lemma: str
    pos: str
    synsets: list[Synset]
    accepted_synsets: tuple[Synset]

    def __eq__(self, o: object) -> bool:
        return self.id == o.id

    def __hash__(self) -> int:
        return hash(self.id)


Sentence: TypeAlias = list[Item]

Document: TypeAlias = list[Sentence]


def test_document() -> Document:
    # They were troubled by insects while playing cricket
    return [
        [
            # Item(
            #     id="w1",
            #     lemma="be",
            #     pos="v",
            #     synsets=wn.synsets("be", pos="v"),
            #     accepted_synsets=[wn.synset("be.v.01")],
            # ),
            # Item(
            #     id="w2",
            #     lemma="trouble",
            #     pos="v",
            #     synsets=wn.synsets("trouble", pos="v"),
            #     accepted_synsets=[wn.synset("trouble.v.02")],
            # ),
            # Item(
            #     id="w3",
            #     lemma="insect",
            #     pos="n",
            #     synsets=wn.synsets("insect", pos="n"),
            #     accepted_synsets=[wn.synset("insect.n.01")],
            # ),
            Item(
                id="w4",
                lemma="play",
                pos="v",
                synsets=wn.synsets("play", pos="v"),
                accepted_synsets=[wn.synset("play.v.01")],
            ),
            Item(
                id="w5",
                lemma="cricket",
                pos="n",
                synsets=wn.synsets("cricket", pos="n"),
                accepted_synsets=[wn.synset("cricket.n.02")],
            ),
        ]
    ]

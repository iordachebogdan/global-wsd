from dataclasses import dataclass
from typing import TypeAlias

from nltk.corpus.reader.wordnet import Synset


@dataclass
class Item:
    id: None | int
    lemma: str
    pos: str
    synsets: list[Synset]
    accepted_synsets: list[Synset]


Sentence: TypeAlias = list[Item]

Document: TypeAlias = list[Sentence]

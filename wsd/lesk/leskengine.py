from copy import copy
import itertools
from typing import TypeAlias

import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset

from wsd.config.leskconfig import LeskConfig
from wsd.lesk.vocab import Vocab
from wsd.util.helpers import translate_to_wn_relations

RelationsDefinitions: TypeAlias = dict[str, list[int]]
RelationsCache: TypeAlias = dict[Synset, RelationsDefinitions]
ScoreCache: TypeAlias = dict[tuple[Synset, Synset], int]

SPECIAL_INDEX = -1


class LeskEngine:
    def __init__(self, config: LeskConfig) -> None:
        self.config = config
        self.vocab = Vocab(self.config.vocab_path)

        if self.config.relation_pairs:
            relations_set: set[str] = {p[0] for p in self.config.relation_pairs}
            relations_set |= {p[1] for p in self.config.relation_pairs}
            self.config.relations_list = list(relations_set)

        self.synset_relations_cache: RelationsCache = {}
        self.score_cache: ScoreCache = {}

    def compute_lesk(self, first_syn: Synset, second_syn: Synset) -> int:
        cached_score = self.score_cache.get((first_syn, second_syn))
        if cached_score is not None:
            return cached_score

        first_relations = self.retrieve_relations(first_syn)
        second_relations = self.retrieve_relations(second_syn)

        score: int
        if not self.config.relation_pairs:
            score = self.compute_overlap(
                first_relations["all"], second_relations["all"]
            )
        else:
            score = 0
            for first_rel, second_rel in self.config.relation_pairs:
                score += self.compute_overlap(
                    first_relations[first_rel], second_relations[second_rel]
                )

        return score

    def retrieve_relations(self, syn: Synset) -> RelationsDefinitions:
        cached_relations = self.synset_relations_cache.get(syn)
        if cached_relations is not None:
            return cached_relations

        definitions: RelationsDefinitions = {}
        for relation in self.config.relations_list:
            if relation == "definition":
                text = syn.definition()
                definitions[relation] = self.vocab.process_text(text)
            else:
                related_syns: set[Synset] = set()
                for wn_relation in translate_to_wn_relations(relation):
                    for s in syn.__getattribute__(wn_relation)():
                        related_syns.add(s)
                merged_definition: list[int] = []
                for s in related_syns:
                    merged_definition.extend(self.vocab.process_text(s.definition()))
                definitions[relation] = merged_definition

        all_definitions = list(itertools.chain.from_iterable(definitions.values()))
        definitions["all"] = all_definitions

        self.synset_relations_cache[syn] = definitions
        return definitions

    def compute_overlap(self, first: list[int], second: list[int]) -> int:
        if not self.config.use_squares:
            return len(set(first) & set(second))
        else:

            def find_longest_common_phrase(
                first: list[int], second: list[int]
            ) -> tuple[int, int, int]:
                """Find the longest common phrase contained in two lists of tokens,
                using dynamic programming (dp[i][j] := length of longest common phrase
                that ends at index i-1 in the first array and index j-1 in the second one)

                Do not match the special index.

                Returns:
                    (length, start index in first, start index in second)
                """
                n = len(first)
                m = len(second)
                dp = np.zeros((n + 1, m + 1), dtype=np.int32)
                best_match = (0, -1, -1)
                for i in range(1, n + 1):
                    for j in range(1, m + 1):
                        if (
                            first[i - 1] == second[j - 1]
                            and first[i - 1] != SPECIAL_INDEX
                        ):
                            dp[i, j] = dp[i - 1, j - 1] + 1
                            if dp[i, j] > best_match[0]:
                                best_match = (dp[i, j], i - dp[i, j], j - dp[i, j])
                return best_match

            overlap = 0
            first = copy(first)
            second = copy(second)
            while True:
                length, start1, start2 = find_longest_common_phrase(first, second)
                if not length:
                    break
                first = first[:start1] + [SPECIAL_INDEX] + first[start1 + length :]
                second = second[:start2] + [SPECIAL_INDEX] + second[start2 + length :]
                overlap += length**2
            return overlap

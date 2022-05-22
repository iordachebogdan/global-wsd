import math
import random
from copy import deepcopy

from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import Synset

from wsd.config.algorithmconfig import FireflyAlgorithmConfig
from wsd.config.leskconfig import LeskConfig
from wsd.data.document import Document, Item
from wsd.firefly.firefly import Firefly
from wsd.lesk.leskengine import LeskEngine
from wsd.util.helpers import discrete_random_variable

BROWN_IC = wordnet_ic.ic("ic-brown.dat")


class Algorithm:
    def __init__(self, config: FireflyAlgorithmConfig, lesk_config: LeskConfig) -> None:
        self.config = config
        self.lesk_engine = LeskEngine(lesk_config)

    def run(self, document: Document) -> dict[Item, Synset]:
        all_items: list[Item] = [item for sentence in document for item in sentence]
        domain: list[int] = [
            min(len(item.synsets), self.config.max_synsets) - 1 for item in all_items
        ]

        # deploy swarm of fireflies
        fireflies = self._deploy_swarm(domain)

        # compute intensities
        for firefly in fireflies:
            firefly.intensity = self._compute_intensity(firefly, all_items)

        for step in range(self.config.num_iterations):
            print(f"FA iteration {step + 1} out of {self.config.num_iterations}")
            for i, first in enumerate(fireflies):
                for second in fireflies[:i]:
                    if second.intensity > first.intensity:
                        # move first towards second
                        distance = first.distance(second)
                        beta = second.intensity * math.exp(
                            -self.config.gamma * (distance**2)
                        )
                        first.move_towards(second, beta, self.config.alpha, domain)

                        # re-compute intensity
                        first.intensity = self._compute_intensity(first, all_items)

            # sort fireflies
            sorted(fireflies, key=lambda firefly: firefly.intensity, reverse=True)

            if discrete_random_variable([self.config.lr]) == 0:
                # local search on best firefly
                print("Doing local search...")
                fireflies[0] = self._lahc(fireflies[0], domain, all_items)

        return {
            item: item.synsets[int(value)]
            for (item, value) in zip(all_items, fireflies[0].values.tolist())
        }

    def _deploy_swarm(self, domain) -> list[Firefly]:
        fireflies: list[Firefly] = [Firefly([0] * len(domain))]
        for _ in range(self.config.swarm_size - 1):
            values = [random.randint(0, num_syns) for num_syns in domain]
            fireflies.append(Firefly(values))
        return fireflies

    def _compute_intensity(self, firefly: Firefly, items: list[Item]) -> float:
        intensity: float = 0
        for center in range(len(items)):
            intensity += self._compute_window_score(firefly, center, items)
        return intensity

    def _compute_window_score(
        self, firefly: Firefly, center: int, items: list[Item]
    ) -> float:
        left = max(0, center - self.config.window_size // 2)
        right = min(len(items), center + self.config.window_size // 2 + 1)
        score = 0
        center_synset = items[center].synsets[int(firefly.values[center])]
        for i in range(left, right):
            if i == center:
                continue

            other_synset = items[i].synsets[int(firefly.values[i])]

            # extended lesk
            score += self.lesk_engine.compute_lesk(center_synset, other_synset)

            # resnik similarity
            try:
                score += center_synset.res_similarity(other_synset, BROWN_IC)
            except Exception:
                # ignore if res similarity is not available for this pair of synsets
                pass
        return score

    def _lahc(self, firefly: Firefly, domain: list[int], items: list[Item]) -> Firefly:
        best_firefly = deepcopy(firefly)
        current_firefly = deepcopy(firefly)
        fitness: list[float] = [firefly.intensity] * self.config.lfa

        for step in range(self.config.lahc_cycles):
            if step % 3000 == 0:
                print(f"\tLAHC step {step + 1} out of {self.config.lahc_cycles}")
            pos = step % self.config.lfa  # pos in fitness vector
            switches = random.sample(
                range(len(domain)), min(len(domain), self.config.lahc_num_switches)
            )  # which senses to switch

            # EFFICIENTLY UPDATE INTENSITY
            intensity_diff: float = 0
            # compute old pairs
            for switch in switches:
                intensity_diff -= 2 * self._compute_window_score(
                    current_firefly, switch, items
                )
            # switch senses
            old_senses = [current_firefly.values[switch] for switch in switches]
            for switch in switches:
                current_firefly.values[switch] = random.randint(0, domain[switch])
            # add new pairs
            for switch in switches:
                intensity_diff += 2 * self._compute_window_score(
                    current_firefly, switch, items
                )
            # update intensity
            current_firefly.intensity += intensity_diff

            if current_firefly.intensity <= fitness[pos] and intensity_diff <= 0:
                # revert perturbation
                current_firefly.intensity -= intensity_diff
                for switch, old_sense in zip(switches, old_senses):
                    current_firefly.values[switch] = old_sense

            # update best firefly if applicable
            if current_firefly.intensity > best_firefly.intensity:
                best_firefly = deepcopy(current_firefly)

            # insert intensity into fitness vector
            fitness[pos] = current_firefly.intensity

        return best_firefly

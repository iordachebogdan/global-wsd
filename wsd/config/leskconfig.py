from copy import deepcopy
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=False)
class LeskConfig:
    # where to store/load the vocabulary used for processing glosses
    vocab_path: str

    # controls if we want to compute overlaps using a squared weight for longer
    # common phrases
    use_squares: bool = False

    # corresponds to the first behaviour of the algorithm, when computing the score
    # for two synsets calculate the overlap between the entire extended gloss of
    # the first one with that of the second one. Extended glosses are computed all
    # the specified relations
    relations_list: None | list[str] = None

    # corresponds to the second behaviour; it is a list of pairs of synset relations;
    # if defined the scores will be computed by summing the overlaps calculated
    # between the gloss obtained from the relation on the first position in the
    # pair for the first synset, and the gloss obtained from the second relation
    # for the second synset.
    relation_pairs: None | list[tuple[str, str]] = None


def lesk_config_from_json(json_config: Any) -> LeskConfig:
    """Given the content of the json configuration object, return the hyperparameters
    of the extended lesk engine.
    """
    config = deepcopy(json_config)
    if "relation_pairs" in config:  # convert to tuples and ensure symmetry
        relation_pairs: list[tuple[str, str]] = [
            (t[0], t[1]) for t in config["relation_pairs"]
        ]
        relation_pairs_set: set[tuple[str, str]] = set(relation_pairs)
        for pair in relation_pairs:
            relation_pairs_set.add((pair[1], pair[0]))
        relation_pairs = list(relation_pairs_set)
        config["relation_pairs"] = relation_pairs
    return LeskConfig(**config)

from copy import deepcopy
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LeskConfig:
    vocab_path: str
    use_squares: bool = False
    relations_list: None | list[str] = None
    relation_pairs: None | list[tuple[str, str]] = None


def lesk_config_from_json(json_config: Any) -> LeskConfig:
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

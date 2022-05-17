from dataclasses import dataclass
from enum import Enum
from typing import Any


class AlgorithmEnum(Enum):
    ANTCOLONY = "antcolony"
    FIREFLY = "firefly"


@dataclass(frozen=True)
class AlgorithmConfig:
    name: AlgorithmEnum


@dataclass(frozen=True)
class AntcolonyAlgorithmConfig(AlgorithmConfig):
    energy_ant: int
    max_energy: int
    evaporation_rate: float
    energy_node: int
    ant_cycles: int
    max_odour: int
    odour_deposit_pct: float
    total_cycles: int


@dataclass(frozen=True)
class FireflyAlgorithmConfig(AlgorithmConfig):
    theta: int


def algorithm_config_from_json(name: str, json_config: Any) -> AlgorithmConfig:
    algorithm_name = AlgorithmEnum(name)
    match algorithm_name:
        case AlgorithmEnum.ANTCOLONY:
            return AntcolonyAlgorithmConfig(name=algorithm_name, **json_config)
        case AlgorithmEnum.FIREFLY:
            return FireflyAlgorithmConfig(name=algorithm_name, **json_config)

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
    energy_ant: int  # how much energy one ant can gather at one step
    max_energy: int  # maximum carry capacity of an ant
    evaporation_rate: float  # percentage for evaporation rate of pheromone trails
    energy_node: int  # initial energy in all nodes
    ant_cycles: int  # lifespan of an ant
    max_odour: int  # maximum length for odour vector
    odour_deposit_pct: float  # pct. of odour vector components deposited by an ant
    total_cycles: int  # number of iterations in the algorithm
    theta: int  # how much pheromone is left by an ant when traversing an edge


@dataclass(frozen=True)
class FireflyAlgorithmConfig(AlgorithmConfig):
    swarm_size: int  # number of fireflies
    window_size: int  # for computing the fireflies' light intensities
    max_synsets: int  # maximum number of senses to consider for a word
    num_iterations: int  # num_iterations
    gamma: float  # light absorption coefficient
    alpha: float  # percantage for randomized movement of firefiles
    lr: float  # probability of starting LAHC search at the end of a cycle
    lfa: float  # length of fitness list in LAHC
    lahc_cycles: int  # number of iterations in LAHC
    lahc_num_switches: int  # for NS, change randomly the senses of this many words


def algorithm_config_from_json(name: str, json_config: Any) -> AlgorithmConfig:
    """Given the name of the algorithm and the content of the json configuration
    object, return its hyperparameters.
    """
    algorithm_name = AlgorithmEnum(name)
    match algorithm_name:
        case AlgorithmEnum.ANTCOLONY:
            return AntcolonyAlgorithmConfig(name=algorithm_name, **json_config)
        case AlgorithmEnum.FIREFLY:
            return FireflyAlgorithmConfig(name=algorithm_name, **json_config)

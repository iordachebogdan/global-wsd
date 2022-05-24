from __future__ import annotations

import json

from wsd.config.algorithmconfig import AlgorithmConfig, algorithm_config_from_json
from wsd.config.datasetconfig import DatasetConfig, dataset_config_from_json
from wsd.config.leskconfig import LeskConfig, lesk_config_from_json


class Config:
    """Configuration object that stores the entire experiment description.

    Attributes:
        dataset_config: configuration for the WSD dataset
        algorithm_config: configuration of ACA/HFA
        lesk_config: configuration of the extended lesk engine
    """

    def __init__(
        self,
        dataset_config: DatasetConfig,
        algorithm_config: AlgorithmConfig,
        lesk_config: LeskConfig,
    ) -> None:
        self.dataset_config = dataset_config
        self.algorithm_config = algorithm_config
        self.lesk_config = lesk_config

    @classmethod
    def from_json(cls, path: str) -> Config:
        with open(path) as f:
            json_dict = json.load(f)
            dataset_config = dataset_config_from_json(
                json_dict["dataset_name"], json_dict["dataset_config"]
            )
            algorithm_config = algorithm_config_from_json(
                json_dict["algorithm_name"], json_dict["algorithm_config"]
            )
            lesk_config = lesk_config_from_json(json_dict["lesk_config"])

            return cls(dataset_config, algorithm_config, lesk_config)

    def __str__(self) -> str:
        return (
            f"dataset_config={self.dataset_config}\n"
            + f"algorithm_config={self.algorithm_config}\n"
            + f"lesk_config={self.lesk_config}"
        )

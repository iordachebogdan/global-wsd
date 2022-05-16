from __future__ import annotations
import json

from wsd.config.algorithmconfig import AlgorithmConfig, algorithm_config_from_json
from wsd.config.datasetconfig import DatasetConfig, dataset_config_from_json


class Config:
    def __init__(
        self,
        dataset_config: DatasetConfig,
        algorithm_config: AlgorithmConfig,
        vocab_path: str,
    ) -> None:
        self.dataset_config = dataset_config
        self.algorithm_config = algorithm_config
        self.vocab_path = vocab_path

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
            vocab_path = json_dict["vocab_path"]

            return cls(dataset_config, algorithm_config, vocab_path)

    def __str__(self) -> str:
        return (
            f"dataset_config={self.dataset_config}\n"
            + f"algorithm_config={self.algorithm_config}\n"
            + f"vocab_path={self.vocab_path}"
        )

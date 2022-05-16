from dataclasses import dataclass
from enum import Enum
from typing import Any


class DatasetEnum(Enum):
    SEMCOR = "semcor"
    SENSEVAL2 = "senseval2"
    SENSEVAL3 = "senseval3"


@dataclass(frozen=True)
class DatasetConfig:
    name: DatasetEnum


@dataclass(frozen=True)
class XMLDatasetConfig(DatasetConfig):
    path: str


def dataset_config_from_json(name: str, json_config: Any) -> DatasetConfig:
    dataset_name = DatasetEnum(name)
    match dataset_name:
        case DatasetEnum.SENSEVAL2 | DatasetEnum.SENSEVAL3:
            return XMLDatasetConfig(name=dataset_name, **json_config)

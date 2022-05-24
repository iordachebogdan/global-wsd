from dataclasses import dataclass
from enum import Enum
from typing import Any


class DatasetEnum(Enum):
    SEMCOR = "semcor"
    SENSEVAL2 = "senseval2"
    SENSEVAL3 = "senseval3"
    SEMEVAL = "semeval"


@dataclass(frozen=True)
class DatasetConfig:
    name: DatasetEnum


@dataclass(frozen=True)
class XMLDatasetConfig(DatasetConfig):
    docs_path: str  # path to the XML file containing the documents
    gs_path: str  # path to the gold labels


@dataclass(frozen=True)
class SemcorDatasetConfig(DatasetConfig):
    pass


def dataset_config_from_json(name: str, json_config: Any) -> DatasetConfig:
    """Given the name of the dataset and the content of the json configuration
    object, return its necessary parameters.
    """
    dataset_name = DatasetEnum(name)
    match dataset_name:
        case DatasetEnum.SENSEVAL2 | DatasetEnum.SENSEVAL3 | DatasetEnum.SEMEVAL:
            return XMLDatasetConfig(name=dataset_name, **json_config)
        case DatasetEnum.SEMCOR:
            return SemcorDatasetConfig(name=dataset_name, **json_config)

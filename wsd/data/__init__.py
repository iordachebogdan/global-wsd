from wsd.config.datasetconfig import (
    DatasetConfig,
    SemcorDatasetConfig,
    XMLDatasetConfig,
)
from wsd.data.datasetbase import DatasetBase
from wsd.data.document import Document  # noqa
from wsd.data.semcordataset import SemcorDataset
from wsd.data.xmldataset import XMLDataset


def load_dataset(config: DatasetConfig) -> DatasetBase:
    if isinstance(config, XMLDatasetConfig):
        return XMLDataset(config)
    elif isinstance(config, SemcorDatasetConfig):
        return SemcorDataset(config)

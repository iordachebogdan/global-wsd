import json
import random
from datetime import datetime

from wsd import antcolony, firefly
from wsd.config.algorithmconfig import AntcolonyAlgorithmConfig, FireflyAlgorithmConfig
from wsd.config.config import Config
from wsd.data import load_dataset

random.seed(666013)

config = Config.from_json("./config.json")
print(config)


predictions_path = (
    f"predictions/{datetime.now()}-{config.algorithm_config.name.value}"
    f"-{config.dataset_config.name.value}"
)
predictions_path = predictions_path.replace(" ", "_")

if isinstance(config.algorithm_config, AntcolonyAlgorithmConfig):
    algorithm = antcolony.Algorithm(config.algorithm_config, config.lesk_config)
elif isinstance(config.algorithm_config, FireflyAlgorithmConfig):
    algorithm = firefly.Algorithm(config.algorithm_config, config.lesk_config)

all_predictions: dict[str, dict[str, list[str]]] = {}
dataset = load_dataset(config.dataset_config)
for i, document in enumerate(dataset.documents):
    print(f"Running document {i + 1} out of {len(dataset.documents)}")
    print("=========================================================\n")
    res = algorithm.run(document)
    for item, predict in res.items():
        all_predictions[item.id] = {
            "correct": [syn.name() for syn in item.accepted_synsets],
            "predicted": [predict.name()],
            "all": [syn.name() for syn in item.synsets],
        }
    with open(predictions_path, "w") as f:
        json.dump(all_predictions, f, indent=4)
    print("\n")

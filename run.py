from datetime import datetime
import json
import random

from nltk.corpus import wordnet as wn

from wsd import antcolony
from wsd.config.config import Config
from wsd.data import load_dataset
from wsd.lesk.leskengine import LeskEngine

random.seed(666013)

config = Config.from_json("./config.json")
print(config)

lesk_engine = LeskEngine(config.lesk_config)
first = wn.synsets("paper")[0]
second = wn.synsets("decalcomania")[1]
print(first.definition(), second.definition(), sep="\n")
print(lesk_engine.compute_lesk(first, second))
print(lesk_engine.compute_lesk(first, second))

predictions_path = (
    f"predictions/{datetime.now()}-{config.algorithm_config.name.value}"
    f"-{config.dataset_config.name.value}"
)
predictions_path = predictions_path.replace(" ", "_")

# document = test_document()
# antcolony_algorithm = antcolony.Algorithm(config.algorithm_config, config.lesk_config)
# res = antcolony_algorithm.run(document)
# print(res)

antcolony_algorithm = antcolony.Algorithm(config.algorithm_config, config.lesk_config)
all_predictions: dict[str, dict[str, list[str]]] = {}
dataset = load_dataset(config.dataset_config)
for i, document in enumerate(dataset.documents):
    print(f"Running document {i + 1} out of {len(dataset.documents)}")
    print("=========================================================\n")
    res = antcolony_algorithm.run(document)
    for item, predict in res.items():
        all_predictions[item.id] = {
            "correct": [syn.name() for syn in item.accepted_synsets],
            "predicted": [predict.name()],
            "all": [syn.name() for syn in item.synsets],
        }
    with open(predictions_path, "w") as f:
        json.dump(all_predictions, f, indent=4)
    print("\n")
    break

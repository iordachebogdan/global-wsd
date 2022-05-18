import random

from nltk.corpus import wordnet as wn

from wsd import antcolony
from wsd.config.config import Config
from wsd.data.document import test_document
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

document = test_document()
antcolony_algorithm = antcolony.Algorithm(config.algorithm_config, config.lesk_config)
res = antcolony_algorithm.run(document)
print(res)

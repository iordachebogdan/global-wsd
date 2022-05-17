from wsd.config.config import Config
from wsd.lesk.leskengine import LeskEngine
from wsd.lesk.vocab import Vocab
from nltk.corpus import wordnet as wn

config = Config.from_json("./config.json")
print(config)

lesk_engine = LeskEngine(config.lesk_config)
first = wn.synsets("water")[0]
second = wn.synsets("decalcomania")[1]
print(first.definition(), second.definition(), sep="\n")
print(lesk_engine.compute_lesk(first, second))
print(lesk_engine.compute_lesk(first, second))

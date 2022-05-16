from wsd.config.config import Config
from wsd.lesk.vocab import Vocab

config = Config.from_json("./config.json")
print(config)

vocab = Vocab(config.lesk_config.vocab_path)
print(len(vocab.word2idx))
print(len(vocab.idx2word))

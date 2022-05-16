import json
import os

import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

from wsd.util.helpers import penntreebank_to_wn


class Vocab:
    def __init__(self, path: str) -> None:
        if os.path.exists(path):
            with open(path) as f:
                json_dict = json.load(f)
                self.word2idx: dict[str, int] = json_dict
        else:
            self.word2idx = Vocab.compute_vocab()
            with open(path, "w") as f:
                json.dump(self.word2idx, f)  # store vocab in cache
        self.idx2word: dict[int, str] = {v: k for k, v in self.word2idx.items()}

    @staticmethod
    def compute_vocab() -> dict[str, int]:
        vocab: dict[str, int] = {}
        lemmatizer = WordNetLemmatizer()
        for syn in wn.all_synsets():
            definition = syn.definition()
            tagged_definition = nltk.pos_tag(nltk.word_tokenize(definition))
            for word, tag in tagged_definition:
                wn_tag = penntreebank_to_wn(tag)
                if not wn_tag:
                    continue
                lemma = lemmatizer.lemmatize(word, pos=wn_tag)
                if lemma not in vocab:
                    vocab[lemma] = len(vocab)
        return vocab

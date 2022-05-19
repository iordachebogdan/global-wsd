from nltk.corpus import semcor
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.semcor import Tree
from nltk.corpus.reader.wordnet import Lemma

from wsd.config.datasetconfig import SemcorDatasetConfig
from wsd.data.datasetbase import DatasetBase
from wsd.data.document import Document, Item, Sentence

FILE_IDS = [
    "brown1/tagfiles/br-a01.xml",
    "brown1/tagfiles/br-b13.xml",
    "brown1/tagfiles/br-c01.xml",
    # "brown1/tagfiles/br-d02.xml",
    # "brown2/tagfiles/br-e22.xml",
    # "brown1/tagfiles/br-r05.xml",
    # "brown2/tagfiles/br-g14.xml",
    # "brown2/tagfiles/br-h21.xml",
    # "brown1/tagfiles/br-j01.xml",
    # "brown1/tagfiles/br-k01.xml",
    # "brown1/tagfiles/br-k11.xml",
    # "brown2/tagfiles/br-l09.xml",
    # "brown1/tagfiles/br-m02.xml",
    # "brown1/tagfiles/br-n05.xml",
    # "brown2/tagfiles/br-p07.xml",
    # "brown2/tagfiles/br-r04.xml",
    # "brown1/tagfiles/br-r06.xml",
    # "brown1/tagfiles/br-r08.xml",
    # "brown1/tagfiles/br-r09.xml",
]


class SemcorDataset(DatasetBase):
    def __init__(self, config: SemcorDatasetConfig) -> None:
        self.documents: Document = []
        for document_tag in FILE_IDS:
            tagged_sentences = semcor.tagged_sents(fileids=document_tag, tag="sem")
            document: Document = []
            for sent_idx, sent in enumerate(tagged_sentences):
                sentence: Sentence = []
                for idx, item in enumerate(sent):
                    if not isinstance(item, Tree) or not isinstance(
                        item.label(), Lemma
                    ):
                        continue
                    sentence.append(
                        Item(
                            id=f"{document_tag}.{sent_idx}.{idx}",
                            lemma=item.label().name(),
                            pos=item.label().synset().pos(),
                            synsets=wn.synsets(
                                item.label().name(), pos=item.label().synset().pos()
                            ),
                            accepted_synsets=[item.label().synset()],
                        )
                    )
                if sentence:
                    document.append(sentence)
            self.documents.append(document)

# type: ignore
# pylint: disable=unused-import

from __future__ import annotations

import numpy as np

# from ._gensim.ext_mm_corpus import ExtMmCorpus
from ._gensim.ext_text_corpus import ExtTextCorpus, SimpleExtTextCorpus

# from ._gensim.mm_corpus_save_load import exists, load_mm_corpus, store_as_mm_corpus
# from ._gensim.mm_corpus_stats import MmCorpusStatisticsService
from ._gensim.utils import (
    from_id2token_to_dictionary,
    from_stream_of_tokens_to_dictionary,
    from_stream_of_tokens_to_sparse2corpus,
    from_token2id_to_dictionary,
)
from ._gensim.wrappers import MalletTopicModel, STTMTopicModel

try:

    from gensim.corpora import MmCorpus
    from gensim.corpora.dictionary import Dictionary
    from gensim.corpora.textcorpus import TextCorpus

except ImportError:

    MmCorpus = object
    TextCorpus = object

    class Dictionary(dict):
        @staticmethod
        def from_corpus(corpus, id2word=None):
            raise ModuleNotFoundError()


try:
    from gensim.matutils import Sparse2Corpus, corpus2csc
except ImportError:

    class Sparse2Corpus:
        def __init__(self, sparse, documents_columns=True):
            if documents_columns:
                self.sparse = sparse.tocsc()
            else:
                self.sparse = sparse.tocsr().T

        def __iter__(self):
            for indprev, indnow in zip(self.sparse.indptr, self.sparse.indptr[1:]):
                yield list(zip(self.sparse.indices[indprev:indnow], self.sparse.data[indprev:indnow]))

        def __len__(self):
            return self.sparse.shape[1]

        def __getitem__(self, document_index):
            indprev = self.sparse.indptr[document_index]
            indnow = self.sparse.indptr[document_index + 1]
            return list(zip(self.sparse.indices[indprev:indnow], self.sparse.data[indprev:indnow]))

    def corpus2csc(corpus, num_terms=None, dtype=np.float64, num_docs=None, num_nnz=None, printprogress=0):
        raise ModuleNotFoundError("gensim not included in package")


try:
    import gensim.models as models
    from gensim.models import CoherenceModel
    from gensim.models.ldamodel import LdaModel
    from gensim.models.ldamulticore import LdaMulticore
    from gensim.models.lsimodel import LsiModel

    from ._gensim.wrappers import LdaMallet
except ImportError:
    ...

try:
    from gensim.utils import check_output
except ImportError:
    from subprocess import check_output

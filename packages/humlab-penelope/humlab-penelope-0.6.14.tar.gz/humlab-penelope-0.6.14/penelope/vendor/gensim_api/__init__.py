# type: ignore
# pylint: disable=unused-import

from __future__ import annotations

from loguru import logger

try:
    from gensim.models import CoherenceModel
    from gensim.models.ldamodel import LdaModel
    from gensim.models.ldamulticore import LdaMulticore
    from gensim.models.lsimodel import LsiModel

    from ._gensim.wrappers import LdaMallet

    __has_gensim: bool = True
except (ImportError, NameError):
    __has_gensim: bool = False
    logger.info("gensim not included in current installment")
    CoherenceModel = None
    LdaModel = None
    LdaMulticore = None
    LsiModel = None
    LdaMallet = None

# from ._gensim.ext_mm_corpus import ExtMmCorpus
try:
    from ._gensim.ext_text_corpus import ExtTextCorpus, SimpleExtTextCorpus
except (ImportError, NameError):
    ExtTextCorpus = None
    SimpleExtTextCorpus = None

try:
    from ._gensim.utils import (
        from_id2token_to_dictionary,
        from_stream_of_tokens_to_dictionary,
        from_stream_of_tokens_to_sparse2corpus,
    )
except (ImportError, NameError):
    from_id2token_to_dictionary = None
    from_stream_of_tokens_to_dictionary = None
    from_stream_of_tokens_to_sparse2corpus = None

try:
    from ._gensim.wrappers import MalletTopicModel, STTMTopicModel
except (ImportError, NameError):
    MalletTopicModel = None
    STTMTopicModel = None

try:

    from gensim.corpora import MmCorpus
    from gensim.corpora.textcorpus import TextCorpus

except (ImportError, NameError):

    MmCorpus = object
    TextCorpus = object

try:
    from _gensim import Dictionary, Sparse2Corpus, corpus2csc
except (ImportError, NameError):
    Dictionary = None
    Sparse2Corpus = None
    corpus2csc = None

try:
    from gensim.utils import check_output
except (ImportError, NameError):
    from subprocess import check_output

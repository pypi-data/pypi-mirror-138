from __future__ import annotations

from typing import Any, Iterable, Union

import penelope.utility as utility
from penelope.corpus.dtm.corpus import VectorizedCorpus
from penelope.vendor import gensim_api

# pylint: disable=unused-argument


@utility.deprecated
def gensim_lsi_predict(model: gensim_api.LsiModel, corpus: Any, scaled=False, chunk_size=512, **kwargs):
    """Predict using Gensim LsiModel. Corpus must be in BoW format i.e. List[List[(token_id, count)]
    BOW => Iterable
    """
    # data_iter = enumerate(model[corpus, minimum_probability]) same as:
    data_iter = enumerate(model[corpus, scaled, chunk_size])
    return data_iter


def gensim_lda_predict(
    model: gensim_api.LdaModel | gensim_api.LdaMulticore, corpus: Any, minimum_probability: float = 0.0
) -> Iterable:
    """Predict using Gensim LdaModel. Corpus must be in BoW format i.e. List[List[(token_id, count)]
    BOW => Iterable
    """
    # data_iter = enumerate(model[corpus, minimum_probability]) same as:
    data_iter = enumerate(model.get_document_topics(bow=corpus, minimum_probability=minimum_probability))
    return data_iter


def mallet_lda_predict(model: gensim_api.LdaMallet, corpus: Any, minimum_probability: float = 0.005) -> Iterable:
    # data_iter = enumerate(model.load_document_topics())
    model.topic_threshold = minimum_probability
    data_iter = enumerate(model[corpus])
    return data_iter


SupportedModels = Union[gensim_api.LdaModel, gensim_api.LdaMulticore, gensim_api.MalletTopicModel, gensim_api.LsiModel]


def predict(model: SupportedModels, corpus: Any, minimum_probability: float = 0.005, **kwargs) -> Iterable:

    if not isinstance(
        model,
        (
            gensim_api.LdaMulticore,
            gensim_api.LdaModel,
            gensim_api.LsiModel,
            gensim_api.MalletTopicModel,
            gensim_api.LdaMallet,
        ),
    ):
        raise ValueError(f"Gensim model {type(model)} is not supported")

    if isinstance(corpus, VectorizedCorpus):
        corpus = gensim_api.Sparse2Corpus(corpus.data, documents_columns=False)

    if isinstance(model, (gensim_api.LdaMulticore, gensim_api.LdaModel)):
        data_iter = gensim_lda_predict(model, corpus, minimum_probability=minimum_probability)
    elif isinstance(model, (gensim_api.MalletTopicModel, gensim_api.LdaMallet)) or hasattr(
        model, 'load_document_topics'
    ):
        data_iter = mallet_lda_predict(model, corpus, minimum_probability=minimum_probability)
    elif hasattr(model, '__getitem__'):
        data_iter = ((document_id, model[corpus[document_id]]) for document_id in range(0, len(corpus)))
    else:
        raise ValueError("unsupported or deprecated model")

    for document_id, topic_weights in data_iter:
        for (topic_id, weight) in (
            (topic_id, weight) for (topic_id, weight) in topic_weights if weight >= minimum_probability
        ):
            yield (document_id, topic_id, weight)

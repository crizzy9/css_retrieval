import os
from collections import Counter
from src.helpers import load_config, abspath, read_file
from src.tfidf import TFIDF
from src.sqlm import SQLM


class PRF:

    def __init__(self, model):
        config = load_config()
        data_dir = config.get('DIRS', 'data_dir')
        stopwords_file = abspath(data_dir, config.get('FILES', 'common_words'))
        corpus_dir = config.get('DIRS', 'corpus_dir')
        self.stopwords = read_file(stopwords_file).split('\n')
        self.parsed_dir = abspath(corpus_dir, config.get('DIRS', 'parsed_dir'))
        self.model = model

    # run model on given query and assume top 10 as relevant
    def rel_docs(self, query):
        scores = self.model.scores(query)
        rel_docs = list()
        for score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]:
            rel_docs.append(score[0])
        return rel_docs

    # get top 3 most frequent terms (excluding stop words) from relevant docs
    def get_freq_terms(self, doc_id):
        doc_path = os.path.join(self.parsed_dir, 'CACM-' + doc_id + '.txt')
        terms = read_file(doc_path).split()
        most_common = Counter(terms).most_common()
        freq_terms = [word_tuple for word_tuple in most_common if not self.is_stop_word(word_tuple[0])]
        return freq_terms[:3]

    # calculate scores for given query using the given model
    def scores(self, query):
        rel_docs = self.rel_docs(query)
        new_query = query
        for doc_id in rel_docs:
            freq_terms = self.get_freq_terms(doc_id)
            new_query = PRF.expand_query(new_query, freq_terms)
        return self.model.scores(new_query)

    # returns true iff the given word is a stop word
    def is_stop_word(self, word):
        return word in self.stopwords

    # expands the given query using the given frequent terms
    @staticmethod
    def expand_query(query, freq_terms):
        for item in freq_terms:
            query += ' ' + item[0]
        return query

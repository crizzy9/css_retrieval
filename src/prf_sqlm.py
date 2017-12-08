import os
from collections import Counter
from src.sqlm import SQLM
from src.query_parser import QueryParser
from src.helpers import load_config, abspath, read_file


class PRF:

    def __init__(self):
        config = load_config()
        data_dir = config.get('DIRS', 'data_dir')
        stopwords_file = abspath(data_dir, config.get('FILES', 'common_words'))
        corpus_dir = config.get('DIRS', 'corpus_dir')
        self.stopwords = read_file(stopwords_file).split('\n')
        self.parsed_dir = abspath(corpus_dir, config.get('DIRS', 'parsed_dir'))
        self.sqlm = SQLM()

    def rel_docs(self, query):
        scores = self.sqlm.scores(query)
        rel_docs = list()
        for score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]:
            rel_docs.append(score[0])
        return rel_docs

    def get_freq_terms(self, doc_id):
        freq_terms = []
        doc_path = os.path.join(self.parsed_dir, 'CACM-' + doc_id + '.txt')
        terms = read_file(doc_path).split()
        most_common = Counter(terms).most_common()
        for term in most_common:
            if term not in self.stopwords:
                freq_terms.append(term)
        return freq_terms

    def scores(self, query):
        rel_docs = self.rel_docs(query)
        new_query = query

        for doc_id in rel_docs:
            freq_terms = self.get_freq_terms(doc_id)
            new_query = PRF.expand_query(new_query, freq_terms)

        return self.sqlm.scores(new_query)

    def get_scores(self):
        return self.scores

    @staticmethod
    def expand_query(query, freq_terms):
        for item in freq_terms[:3]:
            query += ' ' + item[0]
        return query



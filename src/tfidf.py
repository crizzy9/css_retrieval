import os
import math
from src.helpers import load_config, abspath, file_to_dict, read_file, results_to_file, create_dir
from src.query_parser import QueryParser


class TFIDF:

    def __init__(self):
        config = load_config()
        self.parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
        self.index = file_to_dict(abspath(config.get('DIRS', 'index_dir'), config.get('FILES', 'index_file')))
        self.scores = {}
    
    def rank(self):
        qp = QueryParser()
        queries = qp.get_queries()
        docs = os.listdir(self.parsed_dir)
        corpus_len = len(docs)

        for qno, query in queries.items():
            scores = {}
            print('Ranking documents for query: ' + query + '...', end='')
            for term in query.split():
                if term in self.index.keys():
                    inv_list = self.index[term]
                    df = len(inv_list) / corpus_len

                    for entry in inv_list:
                        doc_id = entry[0]
                        doc_name = 'CACM-' + doc_id + '.txt'
                        doc_text = read_file(os.path.join(self.parsed_dir, doc_name))
                        doc_len = len(doc_text)
                        tf = entry[1] / doc_len

                        score = tf * math.log(1 / df)
                        scores[doc_id] = scores[doc_id] + score if doc_id in scores else score
            self.scores[qno] = scores
            print('Done')

        return scores


# Implementation
# ranker = Ranker()
# queries = QueryParser().get_queries()
# config = load_config()
# results_dir = abspath(config.get('DIRS', 'results'))
# create_dir(results_dir)
# results_file_path = os.path.join(results_dir, 'results_tfidf.txt')
#
# for query_id in queries:
#     q = queries[query_id]
#     s = ranker.scores(q)
#     results_to_file(results_file_path, s, 'tfidf')




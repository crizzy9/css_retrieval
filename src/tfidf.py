import os
import math
from src.helpers import load_config, abspath, file_to_dict, read_file, create_dir, get_stoplist, get_model_paths
from src.query_parser import QueryParser
from src.result_writer import ResultWriter


class TFIDF:

    def __init__(self, mode):
        paths = get_model_paths(mode)
        self.mode = mode
        self.doc_dir = paths['doc_dir']
        self.index = file_to_dict(paths['index_file'])
        self.stoplist = get_stoplist()

    def scores(self, query):
        scores = {}
        docs = os.listdir(self.doc_dir)
        corpus_len = len(docs)

        for term in query.split():

            if term in self.index.keys():

                if self.mode == 1:
                    if term in self.stoplist:
                        continue

                inv_list = self.index[term]
                df = len(inv_list) / corpus_len

                for entry in inv_list:
                    doc_id = entry[0]
                    doc_name = 'CACM-' + doc_id + '.txt'
                    doc_text = read_file(os.path.join(self.doc_dir, doc_name))
                    doc_len = len(doc_text)
                    tf = entry[1] / doc_len

                    score = tf * math.log(1 / df)
                    scores[doc_id] = scores[doc_id] + score if doc_id in scores else score

        return scores


# Implementation
# ranker = TFIDF()
# queries = QueryParser().get_queries()
# results_dir = abspath('results')
# results_path = os.path.join(results_dir, 'results_tfidf.txt')
# rw = ResultWriter()
#
# for query_id in queries:
#     q = queries[query_id]
#     s = ranker.scores(q)
#     rw.results_to_file('results_tfidf.txt', query_id, s, 'tfidf')

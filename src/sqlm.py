from math import log
import os
from src.helpers import load_config, abspath, file_to_dict, read_file, get_stoplist, get_model_paths


class SQLM:

    LAMBDA = 0.35

    # (mode = 0 -> no stopping, no stemming, mode = 1 -> stopping, no stemming, mode = 2 -> no stopping, stemming)
    def __init__(self, mode):
        paths = get_model_paths(mode)
        self.mode = mode
        self.doc_dir = paths['doc_dir']
        self.index = file_to_dict(paths['index_file'])
        self.dlens = {doc.replace('CACM-', '').replace('.txt', ''): len(read_file(os.path.join(self.doc_dir, doc)).split()) for doc in os.listdir(self.doc_dir)}
        self.clen = sum(self.dlens.values())
        self.stoplist = get_stoplist()

    # calculate scores for the given query
    def scores(self, query):
        scores = {}

        for term in query.split():

            if term in self.index.keys():
                if self.mode == 1:
                    if term in self.stoplist:
                        continue

                cqi = sum([p[1] for p in self.index[term]])

                for posting in self.index[term]:
                    doc_id = posting[0]
                    tf = posting[1]

                    score = log((((1-self.LAMBDA)*tf/self.dlens[doc_id])/(self.LAMBDA*cqi/self.clen)) + 1)
                    scores[doc_id] = scores[doc_id] + score if doc_id in scores else score

        return scores


# Implementation
# sqlm = SQLM()
# queries = QueryParser().get_queries()
# results_dir = abspath('results')
# results_path = os.path.join(results_dir, 'results_sqlm.txt')
# rw = ResultWriter()
#
# for query_id in queries:
#     q = queries[query_id]
#     s = sqlm.scores(q)
#     rw.results_to_file('results_sqlm.txt', query_id, s, 'sqlm')


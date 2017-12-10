from math import log
import os
from src.helpers import load_config, abspath, file_to_dict,read_file
from src.query_parser import QueryParser
from src.result_writer import ResultWriter


class SQLM:

    LAMBDA = 0.35

    def __init__(self, mode):
        self.mode = mode
        config = load_config()
        self.parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
        self.index = file_to_dict(abspath(config.get('DIRS', 'index_dir'), config.get('FILES', 'index_file')))
        self.dlens = {doc.replace('CACM-', '').replace('.txt', ''): len(read_file(os.path.join(self.parsed_dir, doc)).split()) for doc in os.listdir(self.parsed_dir)}
        self.clen = sum(self.dlens.values())
        self.common_words = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'common_words'))

    def scores(self, query):
        scores = {}

        with open(self.common_words) as file:
            commons = file.readlines()

        for each in commons:
            each.strip("\n")

        for term in query.split():

            if term in self.index.keys():

                if self.mode == 2:
                    if term in commons:
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


from math import log
import os
from src.helpers import load_config, abspath, file_to_dict,read_file
from src.query_parser import QueryParser
from src.result_writer import ResultWriter


class SQLM:

    LAMBDA = 0.35

    def __init__(self):
        config = load_config()
        self.parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
        self.index = file_to_dict(abspath(config.get('DIRS', 'index_dir'), config.get('FILES', 'index_file')))
        self.dlens = {doc.replace('CACM-', '').replace('.txt', ''): len(read_file(os.path.join(self.parsed_dir, doc)).split()) for doc in os.listdir(self.parsed_dir)}
        self.clen = sum(self.dlens.values())

    def scores(self, query):
        scores = {}

        for term in query.split():

            if term in self.index.keys():
                cqi = sum([p[1] for p in self.index[term]])

                for posting in self.index[term]:
                    doc_id = posting[0]
                    tf = posting[1]

                    score = log((((1-self.LAMBDA)*tf/self.dlens[doc_id])/(self.LAMBDA*cqi/self.clen)) + 1)
                    scores[doc_id] = scores[doc_id] + score if doc_id in scores else score

        return scores


# Implementation
sqlm = SQLM()
queries = QueryParser().get_queries()
results_dir = abspath('results')
results_path = os.path.join(results_dir, 'results_sqlm.txt')
rw = ResultWriter('results_sqlm.txt', 'sqlm')

for query_id in queries:
    q = queries[query_id]
    s = sqlm.scores(q)
    rw.results_to_file(query_id, s)


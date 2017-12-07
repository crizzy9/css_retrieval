from math import log
import os
from src.helpers import load_config, abspath, file_to_dict,read_file
from src.query_parser import QueryParser


class SQLM:

    LAMBDA = 0.35

    def __init__(self):
        config = load_config()
        self.parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
        self.index = file_to_dict(abspath(config.get('DIRS', 'index_dir'), config.get('FILES', 'index_file')))
        self.scores = {}

    def scores(self, query):
        dlens = {doc.replace('CACM-', '').replace('.txt', ''): len(read_file(os.path.join(self.parsed_dir, doc)).split(' ')) for doc in os.listdir(self.parsed_dir)}
        clen = sum(dlens.values())
        for qno, query in queries.items():
            for term in query.split(' '):
                if term not in self.index.keys():
                    continue
                cqi = sum([p[1] for p in self.index[term]])
                for posting in self.index[term]:
                    doc = posting[0]
                    tf = posting[1]
                    score = log((((1-self.LAMBDA)*tf/dlens[doc])/(self.LAMBDA*cqi/clen)) + 1)
                    if query not in self.scores.keys():
                        self.scores[query] = [[doc, score]]
                    else:
                        found = False
                        for s in self.scores[query]:
                            if s[0] == doc:
                                s[1] += score
                                found = True
                                break
                        if not found:
                            self.scores[query].append([doc, score])

    def get_scores(self):
        return self.scores


# Implementation
# sqlm = SQLM()
# sqlm.rank()
# print(sqlm.get_scores())


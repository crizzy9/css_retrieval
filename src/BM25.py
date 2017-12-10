import os
from math import log
from src.helpers import load_config, abspath, file_to_dict, get_stoplist, read_file
from src.query_parser import QueryParser
from src.result_writer import ResultWriter
from collections import Counter
import time


class BM25:
    k1 = 1.2
    k2 = 100
    b = 0.75

    def __init__(self, mode):
        self.mode = mode
        self.query_text = {}
        config = load_config()
        self.parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
        self.index = file_to_dict(abspath(config.get('DIRS', 'index_dir'), config.get('FILES', 'index_file')))
        self.rel_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'relevance_data'))

        self.stoplist = get_stoplist()
        self.docs = os.listdir(self.parsed_dir)
        self.N = len(self.docs)
        self.k = {}
        self.calc_k()
        self.R = {}
        self.calc_R()

    def scores(self, qid, query):
        if self.R.get(qid):
            curr_R = len(self.R[qid])
            R_docs = set(self.R.get(qid))
        else:
            curr_R = 0
            R_docs = set()
        scores = {}
        terms = query.strip().split()
        qtfs = dict(Counter(terms))
        for term in terms:
            if self.mode == 2 and term in self.stoplist:
                continue

            if self.index.get(term):
                # print("R[qid] = {}, indexStuff = {}".format(set([e[0] for e in self.index[term]]), R_docs))
                ri = len(set([e[0] for e in self.index[term]]).intersection(R_docs))
                ni = len(self.index[term])
                fp = log(((ri + 0.5) / (curr_R - ri + 0.5)) / ((ni - ri + 0.5) / (self.N - ni - curr_R - ri + 0.5)))
                lp = ((self.k2 + 1) * qtfs[term]) / (self.k2 + qtfs[term])
                for entry in self.index[term]:
                    doc = entry[0]
                    tf = entry[1]
                    mp = ((self.k1 + 1) * tf) / (self.k[doc] + tf)
                    score = fp * mp * lp

                    if scores.get(doc):
                        scores[doc] += score
                    else:
                        scores[doc] = score

        return scores

    def calc_k(self):
        doc_lens = {}
        tot_len = 0
        for doc in self.docs:
            with open(os.path.join(self.parsed_dir, doc)) as f:
                doc_lens[doc] = len(f.read().split(' '))
                tot_len += doc_lens[doc]

        avg_len = tot_len / len(self.docs)

        for doc, dlen in doc_lens.items():
            self.k[doc.replace('CACM-', '').replace('.txt', '')] = self.k1 * ((1 - self.b) + self.b * dlen / avg_len)

    def calc_R(self):
        rel_data = read_file(self.rel_file).strip().split('\n')
        for entry in rel_data:
            if entry is not '':
                data = entry.split()
                qid = int(data[0])
                doc = data[2]
                self.R.setdefault(qid, []).append(doc.replace('CACM-', ''))


bm25 = BM25(1)
results_bm25 = []
queries = QueryParser().get_queries()
for qid in queries:
    score_bm25 = bm25.scores(qid, queries.get(qid))
    results_bm25.append(score_bm25)

# Execution time:
# Old run time
# --- 512.7903730869293 seconds ---
# New run time
# --- 3.44008207321167 seconds ---

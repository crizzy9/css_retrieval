from math import log
from src.helpers import load_config, abspath, file_to_dict, get_stoplist, get_relevance_data, get_doc_lengths, doc_total
from collections import Counter


class BM25:
    k1 = 1.2
    k2 = 100
    b = 0.75

    def __init__(self, mode):
        self.mode = mode
        config = load_config()
        self.index = file_to_dict(abspath(config.get('DIRS', 'index_dir'), config.get('FILES', 'index_file')))
        self.rel_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'relevance_data'))

        self.stoplist = get_stoplist()
        self.N = doc_total()
        self.k = {}
        self.calc_k()
        self.R = get_relevance_data()

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
        doc_lens = get_doc_lengths()
        tot_len = sum(doc_lens.values())

        avg_len = tot_len / self.N

        for doc, dlen in doc_lens.items():
            self.k[doc] = self.k1 * ((1 - self.b) + self.b * dlen / avg_len)


# bm25 = BM25(1)
# results_bm25 = []
# queries = QueryParser().get_queries()
# for qid in queries:
#     score_bm25 = bm25.scores(qid, queries.get(qid))
#     results_bm25.append(score_bm25)

# Run time
# --- 3.44008207321167 seconds ---


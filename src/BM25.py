import re
import os
from math import log
from src.helpers import load_config, write_file, create_dir, abspath, file_to_dict
from src.query_parser import QueryParser
from src.data_parser import DataParser
from src.result_writer import ResultWriter
from src.indexer import Indexer
from collections import Counter


class BM25:
    q = []
    k1 = 1.2
    k2 = 100
    b = 0.75
    dl = {}
    total = 0
    ranks = {}
    avgdl = 0
    sort = []

    def __init__(self):
        self.query_text = {}
        config = load_config()
        self.index = file_to_dict(abspath(config.get('DIRS', 'index_dir'), config.get('FILES', 'index_file')))
        self.query_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'query_file'))
        self.rel_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'relevance_data'))
        self.config = load_config()
        self.dataparser = DataParser()

    def bm25(self):
        for each in self.index:
            for x in self.index[each]:
                x[0] = "CACM-" + str(x[0])

        qp = QueryParser()
        self.query_text = qp.get_queries()

        for file in os.listdir("C:\\Users\\mahal\\OneDrive\\Desktop\\PDP\\css_retrieval\\corpus\parsed"):
            with open("C:\\Users\\mahal\\OneDrive\\Desktop\\PDP\\css_retrieval\\corpus\parsed" + "/" + file, 'r') as f:
                sentence = f.read()
            words = re.findall(r'\w+', sentence)
            self.dl[file.strip(".txt")] = len(words)

        summ = 0

        for each in self.dl:
            summ += self.dl[each]
        # print(summ)

        self.total = len(self.dl)

        # print(self.total)

        self.avgdl = float(summ) / float(self.total)

        # for x in self.index:
        #     print(x, self.index[x])

        count = 1
        # print(avgdl)
        for one in self.query_text:
            self.ranks = {}
            for x in self.index:
                for y in self.index[x]:
                    self.ranks[y[0]] = 0
            # print(len(self.ranks))
            # for x in self.ranks:
            #     print(x, self.ranks[x])
            self.rank(self.query_text[one], count)
            count += 1

    def rank(self, que, count):
        qterm = que.split()
        count_dict = dict(Counter(qterm))

        for a in count_dict.keys():
            if a not in self.index.keys():
                continue
            else:
                for x in self.index[a]:
                    self.ranks[x[0]] += self.score(len(self.index[a]), x[1], count_dict[a], self.total, self.dl[x[0]],
                                                   self.avgdl, self.R_calculate(count), self.r_calculate(a, count))
        # self.sort = {}
        # self.sort = sorted(self.ranks.items(), key=lambda z: z[1], reverse=True)
        rw = ResultWriter("results_bm25.txt", "BM25")
        rw.results_to_file(count, self.ranks)

        # c = str(count)
        # with open("C:\\Users\\mahal\\OneDrive\\Desktop\\PDP\\css_retrieval\\BM25" "/" + "Q" + c + ".txt", 'w') as f:
        #     cnt = 1
        #     for x in self.sort:
        #         f.write(c + " Q0 " + str(x[0]) + " " + str(cnt) + " " + str(x[1]) + " " + "BM25_score" + "\n")
        #         cnt += 1
        # f.close()

    def score(self, n, f, qf, N, dl, avdl, R, r):
        R = float(R)
        K = self.k1 * ((1 - self.b) + self.b * (float(dl) / float(avdl)))
        first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
        second = ((self.k1 + 1) * f) / (K + f)
        third = ((self.k2 + 1) * qf) / (self.k2 + qf)
        return first * second * third

    def R_calculate(self, count):
        with open(self.rel_file) as file:
            a = file.read().split('\n')
        rel = 0
        for s in a:
            if s is not "":
                res = s.split(" ")[0]
                if res == str(count):
                    rel += 1
        return rel

    def r_calculate(self, word, qno):
        with open(self.rel_file, "r") as file:
            a = file.read().split('\n')
        res = 0
        for each in a:
            if each is not "" and each.split(" ")[0] == qno:
                for one in self.index[word]:
                    if one[0] == each.split(" ")[2].split("-")[1]:
                        res += 1
        return res


BM25().bm25()

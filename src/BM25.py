import re
import os
from math import log
from src.helpers import load_config, write_file, create_dir, abspath, file_to_dict
from src.query_parser import QueryParser
from src.data_parser import DataParser
from src.indexer import Indexer
from collections import Counter


class BM25:
    q = []
    k1 = 1.2
    k2 = 100
    b = 0.75
    r = 0.0
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
        self.config = load_config()
        self.dataparser = DataParser()


    def bm25(self):

        for each in self.index:
            for x in self.index[each]:
                x[0] = "CACM-" + str(x[0])


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

        avgdl = float(summ) / float(self.total)

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
                                                   self.avgdl, self.R_calculate(count))
        self.sort = {}
        self.sort = sorted(self.ranks.items(), key=lambda z: z[1], reverse=True)
        for x in self.sort:
            print(x)
        # with open("Q" + c + ".txt", 'w') as f:
        #     cnt = 1
        #     for x in sorts:
        #         f.write(c + " Q0 " + str(x[0]) + " " + str(cnt) + " " + str(x[1]) + " " + "BM25_score" + "\n")
        #         cnt += 1
        # f.close()

    def score(self, n, f, qf, N, dl, avdl, R):
        R = float(R)
        K = self.k1 * ((1 - self.b) + self.b * (float(dl) / float(avdl)))
        first = log(((self.r + 0.5) / (R - self.r + 0.5)) / ((n - self.r + 0.5) / (N - n - R + self.r + 0.5)))
        second = ((self.k1 + 1) * f) / (K + f)
        third = ((self.k2 + 1) * qf) / (self.k2 + qf)
        return first * second * third

    def R_calculate(self, count):
        with open("C:\\Users\\mahal\\OneDrive\\Desktop\\PDP\\css_retrieval\\data\\cacm.rel.txt") as file:
            a = file.read().split('\n')
        r = 0
        for s in a:
            if s is not "":
                res = s.split(" ")[0]
                if res == str(count):
                    r += 1
        return r


BM25().bm25()

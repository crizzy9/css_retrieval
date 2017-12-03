import re
import os
from bs4 import BeautifulSoup
import requests
import helpers


class BM25:

    def __init__(self):
        self.config = helpers.load_config()

    def create(self):
        q = []
        k1 = 1.2
        k2 = 100
        b = 0.75
        R = 0.0
        r = 0.0
        dl = {}
        total = 0
        index = {}
        ranks = {}
        avgdl = 0
        sort = []
        query_text = {}

    def bm25(self):

        c = open("cacm.query.txt", "r")
        soup = BeautifulSoup(c, "html.parser")
        soup.prettify().encode('utf-8')
        count = 1
        for each in soup.find_all('docno'):
            each.extract()
        for each in soup.find_all('doc'):
            self.query_text[count] = each.text.strip(' \t\n')
            count += 1

        for file in os.listdir("HW3_task1"):
            # print(file)
            with open("HW3_task1" "/" + file, 'r') as f:
                sentence = f.read()
            words = re.findall(r'\w+', sentence)
            self.dl[file] = len(words)

        summ = 0

        for each in self.dl:
            summ += self.dl[each]
        print(summ)
        global avgdl

        global total
        total = len(self.dl)

        avgdl = float(summ) / float(total)
        count = 1
        print(avgdl)
        for one in self.query_text:
            global ranks
            ranks = {}
            for x in self.index:
                for y in self.index[x]:
                    ranks[y[0]] = 0
            self.rank(self.query_text[one], count)
            count += 1

    def rank(que, count):
        qterm = que.split()
        for a in qterm:
            print(a)
            for x in index[a]:
                ranks[x[0]] += score(len(index[a]), x[1], 1, total, dl[x[0]], avgdl)
        global sort
        sort = {}
        sort = sorted(ranks.items(), key=lambda z: z[1], reverse=True)
        sorts = sort[:100]
        c = str(count)
        with open("Q" + c + ".txt", 'w') as f:
            cnt = 1
            for x in sorts:
                f.write(c + " Q0 " + str(x[0]) + " " + str(cnt) + " " + str(x[1]) + " " + "win" + "\n")
                cnt += 1
        f.close()

    def score(n, f, qf, N, dl, avdl):
        K = k1 * ((1 - b) + b * (float(dl) / float(avdl)))
        first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
        second = ((k1 + 1) * f) / (K + f)
        third = ((k2 + 1) * qf) / (k2 + qf)
        return first * second * third



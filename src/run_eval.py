from src.helpers import load_config, abspath, read_file
from src.rel_reader import RelevanceReader


class Evaluator:

    def __init__(self, file_name):
        config = load_config()
        self.rel_data = RelevanceReader().get_rel_data()
        self.run = Evaluator.get_run(file_name)
        self.precision = self.calc_precision()
        self.p_at_5 = self.get_p_at_k(5)
        # self.p_at_20 = self.get_p_at_k(20)
        self.recall = self.calc_recall()

    def calc_precision(self):
        precision = {}
        for query_id in self.run:
            precision[query_id] = []
            if query_id in self.rel_data:
                retrieved = []
                for doc_id in self.run[query_id]:
                    retrieved.append(doc_id)
                    p_at_k = self.rel_count(query_id, retrieved) / len(retrieved)
                    precision[query_id].append(p_at_k)
        return precision

    def calc_recall(self):
        recall = {}
        for query_id in self.run:
            recall[query_id] = []
            if query_id in self.rel_data:
                retrieved = []
                for doc_id in self.run[query_id]:
                    retrieved.append(doc_id)
                    r_at_k = self.rel_count(query_id, retrieved) / len(self.rel_data[query_id])
                    recall[query_id].append(r_at_k)
        return recall

    def get_p_at_k(self, k):
        p_at_k = {}
        for query_id in self.precision:
            print(query_id)
            print(len(self.precision[query_id]))
            # p_at_k[query_id] = self.precision[query_id][k-1]
        return p_at_k

    def calc_ap(self):
        pass

    def rel_count(self, query_id, retrieved):
        count = 0
        for doc_id in retrieved:
            if doc_id in self.rel_data[query_id]:
                count += 1
        return count

    def is_rel(self, query_id, doc_id):
        return doc_id in self.rel_data[query_id]

    @staticmethod
    def get_run(file_name):
        run = {}
        run_text = read_file(file_name)
        run_text = run_text.replace('\n\n', '\n')
        for line in run_text.split('\n')[:-1]:
            data = line.split()
            query_id = data[0]
            doc_id = data[2]
            run.setdefault(query_id, []).append(doc_id)
        return run


e = Evaluator(abspath(load_config().get('DIRS', 'results'), 'results_tfidf.txt'))

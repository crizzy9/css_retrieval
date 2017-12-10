from src.helpers import load_config, abspath, read_file
from src.rel_reader import RelevanceReader


class Evaluator:

    def __init__(self, file_name):
        config = load_config()
        self.results_file_path = abspath(config.get('DIRS', 'results'), file_name)
        self.eval_dir_path = abspath(config.get('DIRS', 'results'), config.get('DIRS', 'eval_dir'))
        self.file_name = file_name
        self.rel_data = RelevanceReader().get_rel_data()
        self.run = self.get_run()
        self.precision = {}
        self.p_at_5 = {}
        self.p_at_20 = {}
        self.recall = {}
        self.ap = {}
        self.map = 0.0
        self.rr = {}
        self.mrr = 0.0

    def evaluate(self):
        self.precision = self.__calc_precision()
        self.p_at_5 = self.__get_p_at_k(5)
        self.p_at_20 = self.__get_p_at_k(20)
        self.recall = self.__calc_recall()
        self.ap = self.__calc_ap()
        self.map = self.__calc_map()
        self.rr = self.__calc_rr()
        self.mrr = self.__calc_mrr()

    def __calc_precision(self):
        precision = {}
        for query_id in self.run:
            if query_id in self.rel_data:
                precision[query_id] = []
                retrieved = []
                for doc_id in self.run[query_id]:
                    retrieved.append(doc_id)
                    p_at_k = self.__rel_count(query_id, retrieved) / len(retrieved)
                    relevant = self.__is_rel(query_id, doc_id)
                    precision[query_id].append([doc_id, p_at_k, relevant])
        return precision

    def __calc_recall(self):
        recall = {}
        for query_id in self.run:
            if query_id in self.rel_data:
                recall[query_id] = []
                retrieved = []
                for doc_id in self.run[query_id]:
                    retrieved.append(doc_id)
                    r_at_k = self.__rel_count(query_id, retrieved) / len(self.rel_data[query_id])
                    relevant = self.__is_rel(query_id, doc_id)
                    recall[query_id].append([doc_id, r_at_k, relevant])
        return recall

    def __get_p_at_k(self, k):
        p_at_k = {}
        for query_id in self.precision:
            p_at_k[query_id] = self.precision[query_id][k-1][1]
        return p_at_k

    def __calc_ap(self):
        ap = {}
        for query_id in self.precision:
            p_list = self.precision[query_id]
            sum = 0
            count = 0
            idx = 0
            for p in p_list:
                doc_id = self.run[query_id][idx]
                idx += 1
                if self.__is_rel(query_id, doc_id):
                    sum += p[1]
                    count += 1
            if sum == 0:
                print(self.file_name + ' AP ' + str(query_id) + ': NO RELEVANT DOCS')
                print()
            ap_for_query = sum / count if count != 0 else 0
            ap[query_id] = ap_for_query
        return ap

    def __calc_map(self):
        return sum(self.ap.values()) / len(self.ap)

    def __calc_rr(self):
        rr = {}
        for query_id in self.rel_data:
            doc = next(filter(lambda doc_id: self.__is_rel(query_id, doc_id), self.run[query_id]), None)
            if doc is None:
                print(self.file_name + ' RR ' + str(query_id) + ': NO RELEVANT DOCS')
                print()
            reciprocal_rank = 1 / (self.run[query_id].index(doc) + 1) if doc is not None else 0
            rr[query_id] = reciprocal_rank
        return rr

    def __calc_mrr(self):
        return sum(self.rr.values()) / len(self.rr)

    def __rel_count(self, query_id, retrieved):
        count = 0
        for doc_id in retrieved:
            if self.__is_rel(query_id, doc_id):
                count += 1
        return count

    def __is_rel(self, query_id, doc_id):
        return doc_id in self.rel_data[query_id]

    def eval_to_file(self, run_name):
        precision_file_name = abspath(self.eval_dir_path, run_name + '_precision.txt')
        recall_file_name = abspath(self.eval_dir_path, run_name + '_recall.txt')
        p_at_5_file_name = abspath(self.eval_dir_path, run_name + '_p_at_5.txt')
        p_at_20_file_name = abspath(self.eval_dir_path, run_name + '_p_at_20.txt')
        map_mrr_file_name = abspath(self.eval_dir_path, run_name + '_map_mrr.txt')
        Evaluator.pr_to_file(self.precision, precision_file_name)
        Evaluator.pr_to_file(self.recall, recall_file_name)
        Evaluator.p_at_k_to_file(self.p_at_5, p_at_5_file_name)
        Evaluator.p_at_k_to_file(self.p_at_20, p_at_20_file_name)
        Evaluator.map_mrr_to_file(self.map, self.mrr, map_mrr_file_name)

    def get_run(self):
        run = {}
        run_text = read_file(self.results_file_path)
        run_text = run_text.replace('\n\n', '\n')
        for line in run_text.split('\n')[:-1]:
            data = line.split()
            query_id = data[0]
            doc_id = data[2]
            run.setdefault(query_id, []).append(doc_id)
        return run

    @staticmethod
    def pr_to_file(metric, file_name):
        with open(file_name, 'w+') as f:
            for query_id in metric:
                values = metric[query_id]
                rank = 0
                for value in values:
                    rank += 1
                    doc_id = str(value[0])
                    metric_value = str(value[1])
                    relevant = 'R' if value[2] else 'N'
                    f.write(str(query_id) + ' ')
                    f.write(str(rank) + ' ')
                    f.write(doc_id + ' ')
                    f.write(metric_value + ' ')
                    f.write(relevant)
                    f.write('\n')
                f.write('\n')

    @staticmethod
    def p_at_k_to_file(p_at_k, file_name):
        with open(file_name, 'w+') as f:
            for query_id in p_at_k:
                f.write(str(query_id) + ' ')
                f.write(str(p_at_k[query_id]) + '\n')
            f.write('\n')

    @staticmethod
    def map_mrr_to_file(map, mrr, file_name):
        with open(file_name, 'w+') as f:
            f.write(str(map) + ' ')
            f.write(str(mrr))


# e = Evaluator(abspath(load_config().get('DIRS', 'results'), 'results_tfidf.txt'))
# print(e.run)
# print(e.precision)
# print(e.recall)
# print(e.p_at_5)
# print(e.p_at_20)
# print(e.map)
# print(e.mrr)
# e.eval_to_file('tfidf')

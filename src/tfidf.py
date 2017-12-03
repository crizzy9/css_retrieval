import os
import math
from src.helpers import load_config, abspath, file_to_dict, read_file


class Ranker:

    def __init__(self):
        self.config = load_config()
    
    def rank(self, query):
        scores = {}
        corpus_dir = self.config.get('DIRS', 'corpus_dir')
        parsed_dir = abspath(corpus_dir, self.config.get('DIRS', 'parsed_dir'))
        index_dir = abspath(self.config.get('DIRS', 'index_dir'))
        index_file = self.config.get('FILES', 'index_file')
        docs = os.listdir(corpus_dir)
        corpus_len = len(docs)
        index = file_to_dict(os.path.join(index_dir, index_file))

        for term in query:
            print('Ranking documents for query term: ' + term + '...', end='')

            if term in index.keys():
                inv_list = index[term]
                df = len(inv_list) / corpus_len

                for entry in inv_list:
                    doc_id = entry[0]
                    doc_text = read_file(os.path.join(parsed_dir, doc_id + '.txt'))
                    doc_len = len(doc_text)
                    tf = entry[1] / doc_len

                    score = tf * math.log(1 / df)
                    scores[doc_id] = scores[doc_id] + score if doc_id in scores else score
            print('Done')

        scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return scores

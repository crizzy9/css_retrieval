import os
from src.helpers import load_config, abspath, dict_to_file, read_file, create_dir, get_model_paths
from operator import itemgetter


class Indexer:

    def __init__(self, mode):
        paths = get_model_paths(mode)
        self.mode = mode
        self.index = dict()
        self.doc_dir = paths['doc_dir']
        self.index_dir = paths['index_dir']
        self.index_file = paths['index_file']

    def create(self):
        docs = os.listdir(self.doc_dir)
        index = {}

        for doc in docs:
            file_name = os.path.join(self.doc_dir, doc)
            if file_name.endswith('.txt'):
                print('Indexing ' + file_name + '...', end='')
                doc_name = doc.replace('CACM-', '').replace('.txt', '')
                doc_text = read_file(file_name).strip().split()
                terms = set(doc_text)
                for term in terms:
                    inv_list = []
                    entry = list()
                    entry.append(doc_name)
                    entry.append(doc_text.count(term))
                    positions = [i for i, x in enumerate(doc_text) if x == term]
                    entry = entry + positions
                    if term in index.keys():
                        inv_list = index[term]
                        inv_list = sorted(inv_list, key=itemgetter(1))
                    inv_list.append(entry)
                    index[term] = inv_list
                print('Done')

        self.index = index

    def save_index(self):
        create_dir(self.index_dir)
        dict_to_file(self.index, self.index_file)
        print('Index saved to ' + self.index_file)

    def get_index(self):
        return self.index


# Implementation
# indexer = Indexer()
# indexer.create()
# indexer.save_index()
# ind = Indexer(2)
# ind.create()
# ind.save_index()
# print(ind.get_index())


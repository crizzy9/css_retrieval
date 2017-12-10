import os
from src.helpers import load_config, abspath, dict_to_file, read_file, create_dir
from operator import itemgetter


class Indexer:

    def __init__(self, mode):
        self.mode = mode
        config = load_config()
        self.index = dict()
        self.corpus_dir = config.get('DIRS', 'corpus_dir')
        self.parsed_dir = abspath(self.corpus_dir, config.get('DIRS', 'parsed_dir'))
        self.stem_dir = abspath(self.corpus_dir, config.get('DIRS', 'stem_dir'))
        self.index_dir = abspath(config.get('DIRS', 'index_dir'))
        self.index_file = config.get('FILES', 'index_file')
        self.stem_index_file = config.get('FILES', 'stem_index_file')

    def create(self):
        docs = ""
        index = {}
        if self.mode == 1:
            docs = os.listdir(self.parsed_dir)
        elif self.mode == 2:
            docs = os.listdir(self.stem_dir)

        for doc in docs:
            if self.mode == 1:
                file_name = os.path.join(self.parsed_dir, doc)
            elif self.mode == 2:
                file_name = os.path.join(self.stem_dir, doc)

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
        index_file_path = ""
        if self.mode == 1:
            index_file_path = os.path.join(self.index_dir, self.index_file)
        elif self.mode == 2:
            index_file_path = os.path.join(self.index_dir, self.stem_index_file)
        dict_to_file(self.index, index_file_path)
        print('Index saved to ' + index_file_path)

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


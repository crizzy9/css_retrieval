import os
from src.helpers import load_config, abspath, dict_to_file, read_file
from operator import itemgetter


class Indexer:

    def __init__(self):
        self.config = load_config()
        self.index = None

    def create(self):
        index = {}
        corpus_dir = self.config.get('DIRS', 'corpus_dir')
        parsed_dir = abspath(corpus_dir, self.config.get('DIRS', 'parsed_dir'))
        files = os.listdir(parsed_dir)

        for file_name in files:
            file_name = os.path.join(parsed_dir, file_name)
            
            if file_name.endswith('.txt'):
                print('Indexing ' + file_name + '...', end='')
                doc_name = file_name.split('CACM-')[1].split('.txt')[0]
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
        return index

    def save_index(self):
        index_dir = abspath(self.config.get('DIRS', 'index_dir'))
        index_file = self.config.get('FILES', 'index_file')
        index_file_path = os.path.join(index_dir, index_file)
        dict_to_file(self.index, index_file_path)
        print('Index saved to ' + index_file_path)

    def get_index(self):
        return self.index


# indexer = Indexer()
# indexer.create()
# indexer.save_index()
# print(indexer.get_index())


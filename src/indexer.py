import os
import src.helpers
from operator import itemgetter


class Indexer:

    def __init__(self):
        self.config = src.helpers.load_config()

    def create(self):
        index = {}
        index_dir = self.config.get('DEFAULT', 'index_dir')
        index_file = self.config.get('DEFAULT', 'index_file')
        index_file_path = os.path.join(index_dir, index_file)
        parsed_dir = self.config.get('DEFAULT', 'parsed_dir')
        files = os.listdir(parsed_dir)

        for file_name in files:
            file_name = os.path.join(parsed_dir, file_name)
            
            if file_name.endswith('.txt'):
                print('Indexing ' + file_name + '...', end='')
                doc = self.doc_from_file(file_name)
                doc_name = file_name.split('CACM-')[1].split('.txt')[0]
                doc_text = doc['text']
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
        
        index = sorted(index, key=lambda k: len(index[k]), reverse=True)
        src.helpers.dict_to_file(index, index_file_path)
        print('Index saved to ' + index_file_path)
        return index

    @staticmethod
    def doc_from_file(file_name):
        doc = {}
        with open(file_name, 'r') as doc_file:
            doc['text'] = doc_file.readline().strip().split()

        return doc


print(Indexer().create())
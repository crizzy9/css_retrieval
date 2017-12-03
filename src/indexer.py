import os
import helpers
from operator import itemgetter

class Indexer:

    def __init__(self):
        self.config = helpers.load_config()


    def create(self):
        index = {}
        parsed_dir = self.config.get('DEFAULT', 'parsed_dir')
        files = os.listdir(parsed_dir)

        for file_name in files:
            file_name = os.path.join(parsed_dir, file_name)
            
            if file_name.endswith('.txt'):
                doc = self.doc_from_file(file_name)
                doc_name = file_name.split('CACM-')[1].split('.txt')[0]
                doc_text = doc['text']
                terms = set(doc_text)
                
                for term in terms:
                    inv_list = []
                    entry = []
                    entry.append(doc_name)
                    entry.append(doc_text.count(term))
                    positions = [i for i, x in enumerate(doc_text) if x == term]
                    entry = entry + positions

                    if term in index.keys():
                        inv_list = index[term]
                        inv_list = sorted(inv_list, key=itemgetter(1))

                    inv_list.append(entry)
                    index[term] = inv_list
                
        return index


    def doc_from_file(self, file_name):
        doc = {}
        with open(file_name, 'r') as doc_file:
            doc['text'] = doc_file.readline().strip().split()

        return doc

# print(Indexer().create())
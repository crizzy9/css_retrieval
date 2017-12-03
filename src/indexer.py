import os
import helpers

class Indexer:

    def __init__(self, index_path, corpus_dir_path):
        self.config = helpers.load_config()
        self.index_path = index_path
        self.dir_path = corpus_dir_path


    def create(index_path, ngram):
        index = {}
        docs = os.listdir(self.dir_path)

        for file_name in files:
            file_name = '../' + self.config.get('DEFAULT', 'cacm_dir') + '/' + file_name
            
            if file_name.endswith('.txt')
                doc = doc_from_file(file_name)
                doc_name = doc['title']
                doc_text = doc['text']
                terms = set(doc_text)
                
                for term in terms:
                    inv_list = []
                    entry = []
                    entry.append(doc_name)
                    entry.append(doc_text.count(term))
                    positions = [i for i, x in enumerate(testlist) if x == 1]
                    entry = entry + positions

                    if term in index.keys():
                        inv_list = index[term]

                    inv_list.append(entry)
                    index[term] = inv_list
                
        return index


    def doc_from_file(file_name):
        doc = {}
        with open(file_name, 'r') as doc_file:
            doc[title] = doc_file.readline()
            doc[text] = doc_file.readline().split()

        return doc
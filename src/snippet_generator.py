import os
from src.data_parser import DataParser
from src.helpers import load_config, abspath, read_file, parse_stuff


class SnippetGenerator:

    def __init__(self, query):
        config = load_config()
        self.raw_docs = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'raw_docs'))
        common_words = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'common_words'))
        self.stoplist = []
        with open(common_words, 'r') as f:
            self.stoplist = f.read().split('\n')
        self.significant_words = [term for term in query.split() if term not in self.stoplist]
        self.dataparser = DataParser()

    def get_snippet(self, docs):

        for doc in docs:
            content = read_file(os.path.join(self.raw_docs, 'CACM-' + doc + '.html'))
            self.dataparser.initialize()
            self.dataparser.feed(content)
            data = []
            org_data = self.dataparser.get_data()[3].split('\n\n')[1:-2]
            # parsing document
            for line in org_data:
                data.append(parse_stuff(line, period=True))
            print(data)
            sentences = [line.split('.') for line in data]
            old_sentences = [line.split('.') for line in data]









# Implmentation
query = 'what articles exist which deal with tss time sharing system an operating system for ibm computers'
snippet_generator = SnippetGenerator(query)
docs = ['2312', '0195', '0248', '2578', '2313', '1010', '0494']
snippet_generator.get_snippet(docs)

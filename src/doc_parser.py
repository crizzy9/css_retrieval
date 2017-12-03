import os
from src.helpers import load_config, write_file, create_dir, abspath, parse_stuff
from src.data_parser import DataParser


class Parser:

    def __init__(self):
        config = load_config()
        corpus_dir = config.get('DIRS', 'corpus_dir')
        self.raw_docs = abspath(corpus_dir, config.get('DIRS', 'raw_docs'))
        self.parsed_dir = abspath(corpus_dir, config.get('DIRS', 'parsed_dir'))
        self.data_parser = DataParser()
        create_dir(self.parsed_dir)
        self.parsed_content = ""
        self.raw_corpus = os.listdir(self.raw_docs)

    def parse_documents(self):
        for doc in self.raw_corpus:
            with open(os.path.join(self.raw_docs, doc), 'r') as f:
                content = f.read()
                self.data_parser.initialize()
                self.data_parser.feed(content)
                self.parsed_content = parse_stuff(self.data_parser.get_data()[3])
            write_file(os.path.join(self.parsed_dir, doc.replace('.html', '.txt')), self.parsed_content)


# Implementation
# parser = Parser()
# parser.parse_documents()

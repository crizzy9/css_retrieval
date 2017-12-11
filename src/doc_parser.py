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
        self.stem_dir = abspath(corpus_dir, config.get('DIRS', 'stem_dir'))
        self.stem_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'stemmed_docs'))
        create_dir(self.stem_dir)
        self.docs = []

    def parse_documents(self):
        for doc in self.raw_corpus:
            with open(os.path.join(self.raw_docs, doc), 'r') as f:
                content = f.read()
                self.data_parser.initialize()
                self.data_parser.feed(content)
                self.parsed_content = parse_stuff(self.data_parser.get_data()[3])
                # to remove numbers at the end (specific for cacm corpus
                pmindex = self.parsed_content.rfind('pm')
                if pmindex == -1:
                    self.parsed_content = self.parsed_content[:self.parsed_content.rfind('am') + 2]
                else:
                    self.parsed_content = self.parsed_content[:pmindex + 2]
            write_file(os.path.join(self.parsed_dir, doc.replace('.html', '.txt')), self.parsed_content)

    def stem_parse_documents(self):
        with open(self.stem_file) as f:
            content = f.read().split('#')
            for each in content:
                self.data_parser.initialize()
                self.data_parser.feed(each)
                each = parse_stuff(each)
                pmindex = each.rfind('pm')
                if pmindex == -1:
                    each = each[:each.rfind('am') + 2]
                else:
                    each = each[:pmindex + 2]
                self.docs.append(each)
            for doc in self.docs:
                if doc is not "":
                    write_file(os.path.join(self.stem_dir, 'CACM-' + str(doc).split(" ")[0].zfill(4) + ".txt"),
                               " ".join(str(doc).split(" ")[1:]))


# Implementation
# parser = Parser()
# parser.stem_parse_documents()


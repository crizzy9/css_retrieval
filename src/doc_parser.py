import re
import os
from src.helpers import load_config, write_file, create_dir, abspath
from src.data_parser import DataParser


class Parser:

    # https://regex101.com/r/mTSaQw/3
    punc_regex = re.compile(
        r'([!"#&\'()*+/;<=>?@\\^_`{|}~])|([.:,$])(?![0-9])|(?<![0-9])([%:])|(\[[0-9a-zA-Z/]*])|([^\x00-\x7F\u2013]+)')
    whitespace_regex = re.compile(r'[ \n\t]+')

    def __init__(self):
        config = load_config()
        self.corpus_dir = config.get('DIRS', 'corpus_dir')
        self.raw_docs = abspath(self.corpus_dir, config.get('DIRS', 'raw_docs'))
        self.parsed_dir = abspath(self.corpus_dir, config.get('DIRS', 'parsed_dir'))
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
                self.parsed_content = re.sub(self.punc_regex, ' ', self.data_parser.get_data()[3])
                self.parsed_content = re.sub(self.whitespace_regex, ' ', self.parsed_content).strip().lower()
            write_file(os.path.join(self.parsed_dir, doc.replace('.html', '.txt')), self.parsed_content)


parser = Parser()
parser.parse_documents()

import re
import os
from helpers import load_config, write_file, create_dir
from data_parser import DataParser


class Parser:

    punc_regex = re.compile(
        r'([!"#&\'()*+/;<=>?@\\^_`{|}~])|([.:,$])(?![0-9])|(?<![0-9])([%:])|(\[[0-9a-zA-Z/]*])|([^\x00-\x7F\u2013]+)')
    whitespace_regex = re.compile(r'[ \n\t]+')

    def __init__(self):
        config = load_config()
        self.cacm_dir = config['DEFAULT']['cacm_dir']
        self.parsed_dir = config['DEFAULT']['parsed_dir']
        self.data_parser = DataParser()
        create_dir(self.parsed_dir)
        self.parsed_content = ""
        self.corpus = os.listdir(self.cacm_dir)

    def parse_documents(self):
        for doc in self.corpus:
            with open(os.path.join(self.cacm_dir, doc), 'r') as f:
                content = f.read()
                self.data_parser.initialize()
                self.data_parser.feed(content)
                self.parsed_content = re.sub(self.whitespace_regex, ' ', re.sub(self.punc_regex, ' ', self.data_parser.get_data()[3])).strip()
            write_file(os.path.join(os.getcwd(), self.parsed_dir, doc.replace('.html', '.txt')), self.parsed_content)


parser = Parser()
parser.parse_documents()

import re
import os
from src.helpers import load_config


class Parser:

    punc_regex = re.compile(
        r'([!"#&\'()*+/:;<=>?@\\^_`{|}~])|([.,$])(?![0-9])|(?<![0-9])(%)|(\[[0-9a-zA-Z/]*])|([^\x00-\x7F\u2013]+)')

    def __init__(self):
        config = load_config()
        self.cacm_dir = config['DEFAULT']['cacm_dir']
        self.corpus = os.listdir(self.cacm_dir)

    def parse_documents(self):
        for doc in self.corpus:
            with open(os.path.join(self.cacm_dir, doc), 'r') as f:
                content = f.read()


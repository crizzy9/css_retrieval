import os
from src.helpers import load_config, write_file, create_dir, abspath, parse_stuff
from src.data_parser import DataParser


class Stem_Corpus:

    docs = []

    def __init__(self):
        config = load_config()
        corpus_dir = config.get('DIRS', 'corpus_dir')
        self.stem_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'stemmed_docs'))
        self.stem_dir = abspath(corpus_dir, config.get('DIRS', 'stem_dir'))
        create_dir(self.stem_dir)
        self.data_parser = DataParser()


    def stem(self):
        with open(self.stem_file) as f:
            content = f.read().split('#')
            for each in content:
                self.data_parser.initialize()
                self.data_parser.feed(each)
                self.docs.append(parse_stuff(each))
            for doc in self.docs:
                if doc is not "":
                    write_file(os.path.join(self.stem_dir, 'CACM-' + str(doc).split(" ")[0].zfill(4) + ".txt"),
                               str(doc[2:]))


Stem_Corpus().stem()

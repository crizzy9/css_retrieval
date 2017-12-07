from src.helpers import load_config, abspath, read_file, parse_stuff
from src.data_parser import DataParser


class QueryParser:

    def __init__(self):
        config = load_config()
        self.query_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'query_file'))
        self.data_parser = DataParser()

    def get_queries(self):
        queries = {}
        self.data_parser.initialize()
        self.data_parser.feed(read_file(self.query_file))
        qdata = self.data_parser.get_data()
        i = 3
        while i < len(qdata):
            queries[int(qdata[i].strip())] = parse_stuff(qdata[i+2])
            i += 8
        return queries


# Implementation
qp = QueryParser()
print(qp.get_queries())

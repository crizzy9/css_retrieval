from src.helpers import load_config, abspath, read_file


class RelevanceReader:

    def __init__(self):
        config = load_config()
        data_dir = config.get('DIRS', 'data_dir')
        rel_data_file = abspath(data_dir, config.get('FILES', 'relevance_data'))
        self.rel_data_text = read_file(rel_data_file)

    def get_rel_data(self):
        rel_data = {}
        for line in self.rel_data_text.split('\n'):
            data = line.split()
            query_id = data[0]
            doc_id = data[2][-4:]
            rel_data.setdefault(query_id, []).append(doc_id)
        return rel_data


# print(RelevanceReader().get_rel_data())

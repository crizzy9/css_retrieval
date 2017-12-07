import os
from src.helpers import load_config, abspath, create_dir


class ResultWriter:

    def __init__(self, file_name, model):
        config = load_config()
        self.results_dir = abspath(config.get('DIRS', 'results'))
        create_dir(self.results_dir)
        self.file_path = os.path.join(self.results_dir, file_name)
        self.model = model
        self.clear_results()

    def results_to_file(self, query_id, scores):
        append_write = 'a' if os.path.exists(self.file_path) else 'w'
        with open(self.file_path, append_write) as f:
            rank = 0
            for score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]:
                doc_id = score[0]
                score = score[1]
                rank += 1
                f.write(query_id + ' ')
                f.write('Q0 ')
                f.write(doc_id + ' ')
                f.write(str(rank) + ' ')
                f.write(str(score) + ' ')
                f.write(self.model)
                f.write('\n')
            f.write('\n')

    def clear_results(self):
        files = os.listdir(self.results_dir)
        for f in files:
            if f.endswith('.txt'):
                os.remove(abspath(self.results_dir, f))


import os
from src.helpers import load_config, abspath


class ResultWriter:

    def __init__(self, file_name, model):
        config = load_config()
        self.results_dir = abspath(config.get('DIRS', 'results'))
        self.file_path = os.path.join(self.results_dir, file_name)
        self.model = model
        self.clear_results()

    def results_to_file(self, query_id, scores):
        with open(self.file_path, 'a') as f:
            rank = 0
            for score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]:
                doc_id = score[0]
                score = score[1]
                rank += 1
                f.write(query_id + ' ')
                f.write('Q0 ')
                f.write(doc_id + ' ')
                f.write(rank + ' ')
                f.write(score + ' ')
                f.write(self.model)
            f.write('\n')

    def clear_results(self):
        files = [f for f in os.listdir(self.results_dir) if f.endswith('.txt')]
        for f in files:
            os.remove(f)


import os
from src.helpers import load_config, abspath, create_dir


class ResultWriter:

    def __init__(self):
        config = load_config()
        self.results_dir = abspath(config.get('DIRS', 'results'), config.get('DIRS', 'ranking'))
        create_dir(self.results_dir)

    # write result to file in the following format
    # query_id Q0 doc_id rank score model
    def results_to_file(self, file_name, scores, model):
        file_path = os.path.join(self.results_dir, file_name)
        query_id = 0
        with open(file_path, 'w+') as f:
            for query_score in scores:
                rank = 0
                query_id += 1
                for score in sorted(query_score.items(), key=lambda x: x[1], reverse=True)[:100]:
                    doc_id = score[0]
                    score_value = score[1]
                    rank += 1
                    f.write(str(query_id) + ' ')
                    f.write('Q0 ')
                    f.write(str(doc_id) + ' ')
                    f.write(str(rank) + ' ')
                    f.write(str(score_value) + ' ')
                    f.write(model)
                    f.write('\n')
                f.write('\n')

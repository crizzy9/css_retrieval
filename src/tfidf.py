import helpers

class Ranker

    def __init__(self):
        self.config = helpers.load_config()

    
    def score(self, term):
        score = 0
        index_dir = self.config.get('DEFAULT', 'index_dir')
        index_file = self.config.get('DEFAULT', 'index_file')
        index = helpers.file_to_dict(os.path.join(index_dir, 'index.pickle'))
        
        if term in index.keys():
            inv_list = index[term]
            for entry in inv_list:
                 

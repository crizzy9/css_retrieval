import os
import pickle
import configparser
import re

CONFIG_FILE = 'config.ini'


# using pickle to load dict from file
def file_to_dict(file_name):
    if os.path.isfile(file_name):
        print("Loading file:", file_name)
        if os.path.getsize(file_name) > 0:
            with open(file_name, "rb") as handle:
                dic = pickle.load(handle)
            return dic
    else:
        print("Creating file:", file_name)
        f = open(file_name, "wb+")
        f.close()
        return {}


# using pickle to store dict to file
def dict_to_file(graph, file_name):
    with open(file_name, "wb") as handle:
        pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def create_dir(directory):
    if not os.path.exists(directory):
        print("Creating directory:", directory)
        os.makedirs(directory)


def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def read_file(file_name):
    with open(file_name, "r") as f:
        text = f.read()
    return text


def abspath(path, *paths):
    fpath = os.path.join(os.getcwd(), os.pardir, path)
    for p in paths:
        fpath = os.path.join(fpath, p)
    return fpath


def parse_stuff(data, period=False):
    # https://regex101.com/r/mTSaQw/3
    if period:
        puncs = ':,$'
    else:
        puncs = '.:,$'
    punc_regex = re.compile(
        r'([!"#&\'()*+/;<=>?@\\^_`{|}~])|([' + puncs + '])(?![0-9])|(?<![0-9])([%:])|(\[[0-9a-zA-Z/]*])|([^\x00-\x7F\u2013]+)')
    whitespace_regex = re.compile(r'[ \n\t]+')
    return re.sub(whitespace_regex, ' ', re.sub(punc_regex, ' ', data)).strip().lower()


def get_stoplist():
    config = load_config()
    common_words = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'common_words'))
    return read_file(common_words).split('\n')


def get_relevance_data():
    config = load_config()
    rel_file = abspath(config.get('DIRS', 'data_dir'), config.get('FILES', 'relevance_data'))
    rel_data = read_file(rel_file).strip().split('\n')
    relevance = {}
    for line in rel_data:
        data = line.split()
        query_id = data[0]
        doc_id = data[2].replace('CACM-', '')
        relevance.setdefault(query_id, []).append(doc_id)
    return relevance


def get_doc_lengths():
    config = load_config()
    parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
    docs = os.listdir(parsed_dir)
    doc_lens = {}
    for doc in docs:
        with open(os.path.join(parsed_dir, doc)) as f:
            doc_lens[doc.replace('CACM-', '').replace('.txt', '')] = len(f.read().split())

    return doc_lens


def doc_total():
    config = load_config()
    parsed_dir = abspath(config.get('DIRS', 'corpus_dir'), config.get('DIRS', 'parsed_dir'))
    return len(os.listdir(parsed_dir))


def get_model_paths(mode):
    config = load_config()
    paths = {}
    index_dir = abspath(config.get('DIRS', 'index_dir'))
    corpus_dir = abspath(config.get('DIRS', 'corpus_dir'))
    if mode == 2:
        index_file = abspath(index_dir, config.get('FILES', 'stem_index_file'))
        doc_dir = abspath(corpus_dir, config.get('DIRS', 'stem_dir'))
    else:
        index_file = abspath(index_dir, config.get('FILES', 'index_file'))
        doc_dir = abspath(corpus_dir, config.get('DIRS', 'parsed_dir'))
    paths['index_dir'] = index_dir
    paths['index_file'] = index_file
    paths['doc_dir'] = doc_dir
    return paths

import os
import pickle
import configparser

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

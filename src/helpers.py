import os
import pickle


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
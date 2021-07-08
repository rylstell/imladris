import pickle

def dump(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except:
        return None

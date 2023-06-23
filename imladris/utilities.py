from datetime import datetime
import pytz
import pickle


def save_pickle(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def segment_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]


def datetime_from_rfc3339(rfc3339):
    try:
        timestamp = datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        timestamp = datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%SZ')
    timestamp = timestamp.replace(tzinfo=pytz.utc)
    return timestamp

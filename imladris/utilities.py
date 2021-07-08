from datetime import datetime
import pytz

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

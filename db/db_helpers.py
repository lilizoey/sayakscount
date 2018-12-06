import datetime

def counts_handler(res):
    if (res is None):
        return (0, None)
    else:
        return (res[1], datetime.datetime.fromtimestamp(res[0]))
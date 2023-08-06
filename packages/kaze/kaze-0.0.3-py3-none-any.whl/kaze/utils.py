def include(d, *keys):
    return {k: d[k] for k in keys if k in d}


def omit(d, *keys):
    return {k: d[k] for k in d if k not in keys}

class DotDict(dict):
    """dot.notation access to dictionary attributes

       source:  https://stackoverflow.com/a/23689767
       NOTE: this implementation doesn't support nested dict
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def flatten_list(source: list) -> list:
    result = []
    for item in source:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

import collections.abc


def update(default, modified):
    for k, v in modified.items():
        if isinstance(v, collections.abc.Mapping):
            default[k] = update(default.get(k, {}), v)
        else:
            default[k] = v
    return default


def get(obj, key, sep='.', default=None, suppress_error=False):
    l_key = key.split(sep)
    for k in l_key:
        if not isinstance(obj, dict) or k not in obj:
            if suppress_error:
                return default

            raise KeyError(f'{k} is not in {obj}')
        obj = obj[k]

    return obj

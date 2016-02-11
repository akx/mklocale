def listify(val):
    if not val:
        return []
    if not isinstance(val, (tuple, list)):
        val = [val]
    return list(val)


def unique(iterable):
    seen = set()
    for val in iterable:
        if val not in seen:
            seen.add(val)
            yield val

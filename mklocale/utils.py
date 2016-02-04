def listify(val):
    if not val:
        return []
    if not isinstance(val, (tuple, list)):
        val = [val]
    return list(val)

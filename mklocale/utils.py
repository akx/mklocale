from collections import defaultdict

from babel.messages import Catalog


def listify(val):
    if not val:
        return []
    if not isinstance(val, (tuple, list)):
        val = [val]
    return list(val)


def merge_by_language(catalogs):
    by_locale = defaultdict(list)
    for cat in catalogs:
        by_locale[cat.locale].append(cat)
    for locale, catalogs in by_locale.items():
        merged_catalog = Catalog(locale=locale, header_comment="", charset="utf-8")
        for catalog in catalogs:
            for msg in catalog:
                if msg.string and msg.id != msg.string:
                    merged_catalog[msg.id] = msg
        yield merged_catalog

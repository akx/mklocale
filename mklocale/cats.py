import logging
import os
from collections import defaultdict

from babel.messages import Catalog
from babel.messages.mofile import write_mo
from babel.messages.pofile import write_po

log = logging.getLogger(__name__)


def write_catalog(target_file, catalog):
    target_dir = os.path.dirname(target_file)
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    with open(target_file, "wb") as outfp:
        if target_file.endswith(".po"):
            write_po(
                outfp, catalog,
                width=10000, no_location=True,
                omit_header=True, sort_output=True,
                ignore_obsolete=True
            )
        elif target_file.endswith(".mo"):
            write_mo(outfp, catalog)
        else:
            log.warn("Unknown file type: %s" % target_file)
    log.info("Wrote %s" % target_file)


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

import argparse
import hashlib
import logging
import os

import yaml

from mklocale.cats import merge_by_language, write_catalog
from mklocale.sources import transifex, local
from mklocale.utils import listify

log = logging.getLogger("mklocale")


def cmdline(argv):
    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    args = ap.parse_args()

    try:
        import requests_cache
        requests_cache.install_cache(
            os.path.realpath('./mklocale.%s.cache' % hashlib.md5(args.config).hexdigest()),
            expire_after=86400
        )
    except ImportError:
        pass
    os.chdir(os.path.dirname(args.config))
    with open(args.config, "r") as infp:
        config = yaml.safe_load(infp)
    catalogs = []

    for tx_config in listify(config.get("transifex")):
        catalogs.extend(transifex.read_catalogs(tx_config))

    for local_config in listify(config.get("local")):
        catalogs.extend(local.read_catalogs(local_config))

    for merged_catalog in merge_by_language(catalogs):
        targets = [
            t.format(lang=merged_catalog.locale)
            for t
            in listify(config["target"])
        ]
        for target_file in targets:
            write_catalog(target_file, merged_catalog)

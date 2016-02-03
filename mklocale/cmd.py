import argparse
import logging

import yaml

from mklocale import transifex
from mklocale.cats import write_catalog, merge_by_language
from mklocale.utils import listify

log = logging.getLogger("mklocale")


def cmdline(argv):
    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    args = ap.parse_args()
    with open(args.config, "r") as infp:
        config = yaml.safe_load(infp)
    catalogs = []
    for tx_config in listify(config.get("transifex")):
        catalogs.extend(transifex.read_catalogs(tx_config))
    for merged_catalog in merge_by_language(catalogs):
        targets = [
            t.format(lang=merged_catalog.locale)
            for t
            in listify(config["target"])
        ]
        for target_file in targets:
            write_catalog(target_file, merged_catalog)

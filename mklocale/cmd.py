import argparse
import os
import yaml
import logging
from babel.messages.pofile import write_po

from mklocale.utils import listify, merge_by_language
from mklocale import transifex

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
        target_file = config["target"].format(lang=merged_catalog.locale)
        target_dir = os.path.dirname(target_file)
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        with open(target_file, "w") as outfp:
            write_po(
                outfp, merged_catalog,
                width=10000, no_location=True,
                omit_header=True, sort_output=True,
                ignore_obsolete=True
            )
        log.info("Wrote %s" % target_file)

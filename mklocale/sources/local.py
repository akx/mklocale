import json
import logging

import six
import yaml
from babel import Locale
from babel.messages import Catalog
from babel.messages.mofile import read_mo
from babel.messages.pofile import read_po

log = logging.getLogger(__name__)


def read_json(fp):
    data = json.load(fp)
    catalog = Catalog(header_comment="")
    for id, msg in data.items():
        catalog.add(id, msg)
    return catalog


def read_yaml(fp):
    data = yaml.safe_load(fp)
    catalog = Catalog(header_comment="")
    for id, msg in data.items():
        catalog.add(id, msg)
    return catalog


def read_catalogs(local_config):
    if isinstance(local_config, six.string_types):
        local_config = {"file": local_config, "language": None}

    filename = local_config["file"]
    catalog = None
    with open(filename) as infp:
        if filename.endswith(".mo"):
            catalog = read_mo(infp)
        elif filename.endswith(".po"):
            catalog = read_po(infp)
        elif filename.endswith(".json"):
            catalog = read_json(infp)
        elif filename.endswith(".yaml"):
            catalog = read_yaml(infp)

    if not catalog:
        raise ValueError("Can't read: %s" % filename)

    if local_config.get("language"):
        catalog.locale = Locale.parse(local_config["language"])

    if not catalog.locale:
        raise ValueError("File %s has no language set (use `language: ...`?)" % filename)

    if not catalog.header_comment:
        catalog.header_comment = "# From %s" % filename

    yield catalog

import os

import requests
import six
import logging
from babel.messages.pofile import read_po

from mklocale.utils import listify

log = logging.getLogger(__name__)


def get_tx_auth():
    auth_string = os.environ.get("TRANSIFEX_AUTH")
    if auth_string and ":" in auth_string:
        return tuple(auth_string.split(":"))


def read_catalogs(tx_config):
    if isinstance(tx_config, six.string_types):
        tx_config = {"project": tx_config}
    project_slug = tx_config["project"]
    sess = requests.Session()
    resource_data = sess.get(
        "http://www.transifex.com/api/2/project/%s/resources/" % project_slug,
        auth=get_tx_auth()
    ).json()
    languages = listify(tx_config.get("languages"))
    resources = set(listify(tx_config.get("resources")))
    for resource_datum in resource_data:
        res_slug = resource_datum["slug"]
        if resources and res_slug not in resources:
            continue
        for lang_code in languages:
            log.info("Processing %s.%s (%s)" % (project_slug, res_slug, lang_code))
            xlate_resp = sess.get(
                "http://www.transifex.com/api/2/project/%s/resource/%s/translation/%s/" % (
                    project_slug,
                    res_slug,
                    lang_code
                ),
                params={"mode": "onlytranslated"},
                auth=get_tx_auth()
            ).json()
            sio = six.StringIO(xlate_resp["content"])
            yield read_po(sio, domain=res_slug, locale=lang_code, charset="UTF-8")

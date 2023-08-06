from __future__ import annotations

import ckan.model as model
import ckan.plugins.toolkit as tk

from ckanext.toolbelt.decorators import Collector
from ckanext.files.model import File

helper, get_helpers = Collector("thumbnailer").split()


@helper
def resource_thumbnail_url(id_: str, qualified: bool = False):
    existing = (
        model.Session.query(File)
        .filter(File.extras["thumbnailer"]["resource_id"].astext == id_)
        .one_or_none()
    )
    if not existing:
        return
    return tk.h.url_for_static(existing.path, qualified=qualified)

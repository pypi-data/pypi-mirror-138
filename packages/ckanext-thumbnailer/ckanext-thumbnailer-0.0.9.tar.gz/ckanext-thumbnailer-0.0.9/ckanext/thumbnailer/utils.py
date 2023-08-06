from __future__ import annotations
import logging

import ckan.plugins.toolkit as tk

log = logging.getLogger(__name__)

CONFIG_FORMATS = "ckanext.thumbnailer.auto_formats"
DEFAULT_FORMATS = []


def create_thumbnail(context, data_dict):
    formats = tk.aslist(tk.config.get(CONFIG_FORMATS, DEFAULT_FORMATS))
    fmt = data_dict.get("format")

    if not fmt or fmt.lower() not in formats:
        return

    try:
        result = tk.get_action("thumbnailer_resource_thumbnail_create")(context, data_dict)
        log.info("Thumbnail for %s created at %s", data_dict["id"], result["thumbnail"])
    except tk.ValidationError as e:
        log.error("Cannot create thumbnail: %s", e)

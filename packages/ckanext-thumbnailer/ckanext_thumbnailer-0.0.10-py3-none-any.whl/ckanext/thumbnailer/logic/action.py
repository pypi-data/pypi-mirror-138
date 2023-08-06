from __future__ import annotations

import tempfile
import os
import logging
import subprocess
from typing import Any, Callable
from preview_generator.exception import UnsupportedMimeType
from preview_generator.manager import PreviewManager
from werkzeug.datastructures import FileStorage

import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector
from ckanext.toolbelt.utils.fs import path_to_resource
from ckanext.files.model import File

log = logging.getLogger(__name__)
action, get_actions = Collector("thumbnailer").split()

CONFIG_MAX_REMOTE_SIZE = "ckanext.thumbnailer.max_remote_size"
DEFAULT_MAX_REMOTE_SIZE = 0



@action
def resource_thumbnail_create(context, data_dict):
    tk.check_access("thumbnailer_resource_thumbnail_create", context, data_dict)

    res = tk.get_action("resource_show")(context, {"id": data_dict["id"]})

    preview = _get_preview(res)
    upload = FileStorage(open(preview, "rb"), "-thumbnail-{}.jpeg".format(res["id"]))

    existing = (
        context["session"]
        .query(File)
        .filter(File.extras["thumbnailer"]["resource_id"].astext == res["id"])
        .one_or_none()
    )

    factory: Callable[..., Any]
    if existing:
        factory = tk.get_action("files_file_update")
        data = {
            "id": existing.id,
            "upload": upload,
        }
    else:
        factory = tk.get_action("files_file_create")
        data = {
            "name": "Resource {id} thumbnail".format(id=res["id"]),
            "kind": "thumbnail",
            "upload": upload,
            "extras": {"thumbnailer": {"resource_id": res["id"]}},
        }
    result = factory({"ignore_auth": True, "user": context["user"]}, data)

    return {
        "thumbnail": result["path"]
    }


def _get_preview(res: dict[str, Any]):
    cache = os.path.join(
        tempfile.gettempdir(), tk.config["ckan.site_id"], "ckanext-thumbnailer"
    )
    manager = PreviewManager(cache, create_folder=True)

    max_size = tk.asint(tk.config.get(CONFIG_MAX_REMOTE_SIZE, DEFAULT_MAX_REMOTE_SIZE))
    with path_to_resource(res, max_size) as path:
        if not path:
            raise tk.ValidationError({"id": ["Cannot determine path to resource"]})
        try:
            return manager.get_jpeg_preview(path)
        except (UnsupportedMimeType, subprocess.CalledProcessError) as e:
            log.error("Cannot extract thumbnail for resource %s: %s", res["id"], e)
            raise tk.ValidationError({"id": ["Unsupported media type"]})

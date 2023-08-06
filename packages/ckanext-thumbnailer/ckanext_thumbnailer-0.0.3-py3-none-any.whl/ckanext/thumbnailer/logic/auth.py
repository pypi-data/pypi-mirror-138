from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector

auth, get_auth_functions = Collector("thumbnailer").split()


@auth
def thumbnail_create(context, data_dict):
    return {"success": False}


@auth
def thumbnail_delete(context, data_dict):
    return {"success": False}


@auth
def resource_thumbnail_create(context, data_dict):
    return tk.check_access("resource_create", context, data_dict)


@auth
def resource_thumbnail_delete(context, data_dict):
    return tk.check_access("resource_delete", context, data_dict)

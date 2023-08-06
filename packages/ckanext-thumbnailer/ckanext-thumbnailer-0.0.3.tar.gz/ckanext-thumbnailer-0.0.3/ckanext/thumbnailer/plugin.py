from __future__ import annotations
import logging
from ckan.exceptions import CkanConfigurationException
import ckan.plugins as p
import ckan.plugins.toolkit as tk

from . import helpers
from .logic import action, auth

log = logging.getLogger(__name__)

CONFIG_FORMATS = "ckanext.thumbnailer.auto_formats"
DEFAULT_FORMATS = []



class ThumbnailerPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IConfigurable)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IResourceController, inherit=True)

    if tk.check_ckan_version("2.10"):
        p.implements(p.IConfigDeclaration)

        def declare_config_options(self, declaration, key):
            declaration.declare_list("ckan.upload.thumbnail.types", [])
            declaration.declare_list("ckan.upload.thumbnail.mimetypes", [])

    # IConfigurable

    def configure(self, config):
        if "files" not in config["ckan.plugins"]:
            raise CkanConfigurationException(
                f"thumbnailer plugins requires files plugin"
            )

    # IConfigurer

    def update_config(self, config_):
        ...

    # IActions
    def get_actions(self):
        return action.get_actions()

    # IAuthFunctions
    def get_auth_functions(self):
        return auth.get_auth_functions()

    # ITemplateHelpers
    def get_helpers(self):

        return helpers.get_helpers()

    # IResourceController
    def after_resource_create(self, context, data_dict):
        _create_thumbnail(context, data_dict)

    def after_resource_update(self, context, data_dict):
        _create_thumbnail(context, data_dict)

    after_create = after_resource_create
    after_update = after_resource_update



def _create_thumbnail(context, data_dict):
    formats = tk.aslist(tk.config.get(CONFIG_FORMATS, DEFAULT_FORMATS))
    fmt = data_dict.get("format")

    if not fmt or fmt.lower() not in formats:
        return

    try:
        result = tk.get_action("thumbnailer_resource_thumbnail_create")(context, data_dict)
        log.error("Thumbnail for %s created at %s", data_dict["id"], result["thumbnail"])
    except tk.ValidationError as e:
        log.error("Cannot create thumbnail: %s", e)

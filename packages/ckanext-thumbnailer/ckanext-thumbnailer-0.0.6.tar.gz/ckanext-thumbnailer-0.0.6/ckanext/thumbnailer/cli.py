from __future__ import annotations

import click
import ckan.model as model
import ckan.plugins.toolkit as tk
from . import utils

def get_commands():
    return [thumbnailer]


@click.group(short_help="ckanext-thumbnailer CLI.")
def thumbnailer():
    """ckanext-thumbnailer CLI.
    """
    pass

@thumbnailer.command()
@click.argument("ids", nargs=-1)
def process(ids: tuple[str]):
    """Create thumbnails for the given/all resources
    """
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    resources = _get_resources(ids)
    with click.progressbar(resources, length=resources.count()) as bar:
        for res in bar:
            utils.create_thumbnail({"user": user["name"]}, {
                "id": res.id,
                "format": res.format,
            })

def _get_resources(ids: tuple[str]):
    q = model.Session.query(model.Resource).filter(
        model.Resource.state == "active"
    )
    if ids:
        q = q.filter(model.Resource.id.in_(ids))

    return q

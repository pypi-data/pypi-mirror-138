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
@click.option("-o", "--offset", type=int, default=0)
def process(ids: tuple[str], offset: int):
    """Create thumbnails for the given/all resources
    """
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    resources = _get_resources(ids)
    with click.progressbar(resources, length=resources.count()) as bar:
        for res in bar:
            bar.label = bar.pos
            if bar.pos < offset:
                continue
            utils.create_thumbnail({"user": user["name"]}, {
                "id": res.id,
                "format": res.format,
            })

def _get_resources(ids: tuple[str]):
    q = model.Session.query(model.Resource).filter(
        model.Resource.state == "active"
    ).order_by(model.Resource.id)
    if ids:
        q = q.filter(model.Resource.id.in_(ids))

    return q

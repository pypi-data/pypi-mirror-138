from __future__ import annotations
from typing import Any, Callable, cast
from typing_extensions import TypeAlias
import click
from . import utils

Context: TypeAlias = 'dict[str, Any]'
DataDict: TypeAlias = 'dict[str, Any]'
ResultDict: TypeAlias = 'dict[str, Any]'

def get_commands():
    return [boe]

@click.group(short_help="boe CLI.")
def boe():
    """boe CLI.
    """
    pass



@boe.command()
@click.option("-p", "--path", default="statistics")
@click.option("-o", "--organization", default="bank-of-england")
@click.option("--allow-updates", is_flag=True)
# @click.argument()
def scrap(path: str, organization: str, allow_updates: bool):
    """Docs.
    """

    import ckan.model as model
    import ckan.plugins.toolkit as tk
    get_action = cast(Callable[[str], Callable[[Context, DataDict], ResultDict]], tk.get_action)

    user = get_action("get_site_user")({"ignore_auth": True}, {})

    for page in utils.dig(path):
        for pkg_data in page.package_data():
            action = get_action("package_create")
            if allow_updates and model.Package.get(pkg_data["name"]):
                action = get_action("package_update")

            pkg_data["owner_org"] = organization
            pkg = action(
                {"user": user["name"]},
                pkg_data
            )


@boe.command()
@click.argument("param", nargs=-1)
# @click.argument()
def db(param: tuple[str]):
    """Docs.
    """
    from .utils import db
    params = dict(p.split("=") for p in param)
    db.build_cache(params)

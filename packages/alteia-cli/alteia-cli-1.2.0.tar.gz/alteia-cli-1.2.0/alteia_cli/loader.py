import inspect
import logging
import pkgutil
from typing import Iterable, List

import typer

from alteia_cli import AppDesc

LOGGER = logging.getLogger(__name__)


def _is_app_desc(obj):
    """Check whether object is an instance of AppDesc.

    """
    return isinstance(obj, AppDesc)


def _discover(submodules_path: Iterable[str]) -> List[AppDesc]:
    """Import submodules and build list of app descriptions.

    """
    found = []
    LOGGER.debug(f'Searching for app descriptions in {submodules_path!r}')
    for loader, modname, _ in pkgutil.walk_packages(submodules_path):
        module_loader = loader.find_module(modname)  # type: ignore
        mod = module_loader.load_module(modname) if module_loader else None
        apps = inspect.getmembers(mod, _is_app_desc) if mod else []
        for _, obj in apps:
            found.append(obj)

    LOGGER.debug(f'Found {len(found)} app descriptions')
    return found


class Loader:
    def __init__(self, app: typer.Typer):
        self._app = app
        self._app_names: List[str] = []

    def extend_app(self, submodules_path: Iterable[str]):
        found = _discover(submodules_path)
        for app_desc in found:
            app_name = app_desc.name

            if app_name in self._app_names:
                typer.secho(f'Found an application conflict for {app_name!r}',
                            fg=typer.colors.RED)
                continue

            LOGGER.debug(f'Adding {app_name!r} app')
            self._app.add_typer(app_desc.app,
                                name=app_name,
                                help=app_desc.help)
            self._app_names.append(app_name)

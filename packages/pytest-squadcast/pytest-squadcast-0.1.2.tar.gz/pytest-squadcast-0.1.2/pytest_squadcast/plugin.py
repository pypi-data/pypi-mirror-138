import os
from _pytest.config import Config, PytestPluginManager
from _pytest.config.argparsing import Parser

from pytest_squadcast.squadcast import Squadcast


def pytest_addhooks(pluginmanager: PytestPluginManager):
    from . import hooks

    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser: Parser):
    parser.addoption("--squadcast", action="store_true", help="Report incident via Squadcast")


def pytest_configure(config: Config):
    if config.getoption("--squadcast") and not hasattr(config, "workerinput"):
        config._squadcast = Squadcast(config)
        config.pluginmanager.register(config._squadcast)


def pytest_unconfigure(config: Config):
    squadcast = getattr(config, "_squadcast", None)
    if squadcast:
        del config._squadcast
        config.pluginmanager.unregister(squadcast)

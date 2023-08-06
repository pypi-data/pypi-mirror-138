# -*- coding: utf-8 -*-
"""Pro Custodibus broker-credentials tool.

Generates Pro Custodibus credentials from the configured broker-setup code.

Usage:
  procustodibus-broker-credentials [--config=CONFIG] [-v | -vv | --verbosity=LEVEL]
  procustodibus-broker-credentials --help
  procustodibus-broker-credentials --version

Options:
  -h --help             Show this help
  --version             Show broker version
  -c --config=CONFIG    Config file
  --verbosity=LEVEL     Log level (ERROR, WARNING, INFO, DEBUG)
  -v                    INFO verbosity
  -vv                   DEBUG verbosity
"""
from docopt import docopt

from procustodibus_broker import __version__ as version
from procustodibus_broker.api import setup_api
from procustodibus_broker.cnf import Cnf


def main():
    """Tool entry point."""
    args = docopt(__doc__)
    if args["--version"]:
        # print version to stdout
        print("procustodibus-broker-credentials " + version)  # noqa: T001
    else:
        run(
            args["--config"],
            args["--verbosity"] or args["-v"],
        )


def run(*args):
    """Runs tool.

    Arguments:
        *args (list): List of arguments to pass to Cnf constructor.
    """
    cnf = Cnf(*args)

    if not cnf.broker and type(cnf.setup) is dict:
        cnf.broker = cnf.setup.get("broker")

    if not cnf.host:
        cnf.host = "ignored"

    setup_api(cnf)


if __name__ == "__main__":
    main()

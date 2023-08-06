# -*- coding: utf-8 -*-
"""Pro Custodibus Broker.

Pushes events from Pro Custodibus into your security management systems.

Usage:
  procustodibus-broker [--config=CONFIG] [--loop=SECONDS]
                       [-v | -vv | --verbosity=LEVEL]
  procustodibus-broker --help
  procustodibus-broker --test [--config=CONFIG] [-v | -vv | --verbosity=LEVEL]
  procustodibus-broker --test-pipe=NAME [--config=CONFIG]
                       [-v | -vv | --verbosity=LEVEL]
  procustodibus-broker --version

Options:
  -h --help             Show this help
  --test                Run connectivity check
  --test-pipe=NAME      Output test data to pipe NAME
  --version             Show broker version
  -c --config=CONFIG    Config file
  -l --loop=SECONDS     Loop indefinitely, polling every SECONDS
  --verbosity=LEVEL     Log level (ERROR, WARNING, INFO, DEBUG)
  -v                    INFO verbosity
  -vv                   DEBUG verbosity
"""
from sys import exit

from docopt import docopt

from procustodibus_broker import __version__ as version
from procustodibus_broker.broker import poll, poll_loop, test_pipe
from procustodibus_broker.cnf import Cnf
from procustodibus_broker.connectivity import check_connectivity


def main():
    """CLI Entry point."""
    args = docopt(__doc__)
    if args["--version"]:
        # print version to stdout
        print("procustodibus-broker " + version)  # noqa: T001
    elif args["--test"]:
        check(args["--config"], args["--verbosity"] or args["-v"])
    elif args["--test-pipe"]:
        check_pipe(
            args["--config"],
            args["--verbosity"] or args["-v"],
            args["--test-pipe"],
        )
    else:
        run(
            args["--config"],
            args["--verbosity"] or args["-v"],
            args["--loop"],
        )


def check(*args):
    """Runs connectivity check.

    Arguments:
        *args (list): List of arguments to pass to Cnf constructor.
    """
    cnf = Cnf(*args)
    exit(check_connectivity(cnf))


def check_pipe(cnf_file, verbosity, pipe):
    """Outputs test data to the specified pipe.

    Arguments:
        cnf_file (str): Path to configuration file. Defaults to no file.
        verbosity (str): Root log level. Defaults to 'WARNING'.
        pipe (str): Name of pipe to test.
    """
    cnf = Cnf(cnf_file, verbosity)
    test_pipe(cnf, pipe)


def run(*args):
    """Runs CLI.

    Arguments:
        *args (list): List of arguments to pass to Cnf constructor.
    """
    cnf = Cnf(*args)

    if cnf.loop:
        poll_loop(cnf)
    else:
        poll(cnf)


if __name__ == "__main__":
    main()

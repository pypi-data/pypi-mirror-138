# -*- coding: utf-8 -*-
"""Broker logic."""
from io import StringIO
from logging import getLogger
from time import sleep

from procustodibus_broker import __version__ as version
from procustodibus_broker.api import poll_api
from procustodibus_broker.connectivity import check_connectivity
from procustodibus_broker.pipe import (
    init_pipe,
    init_pipes,
    pipe_from_queues,
    pipe_from_test,
    separate_pipe_queues,
)


def is_connection_good(cnf, message="Checking connectivity", expect_error=False):
    """Runs connectivity check and logs result.

    Arguments:
        cnf (Config): Config object.
        message (str): Message to log (defaults to 'Checking connectivity').
        expect_error (bool): True if error expected (defaults to False).

    Returns:
        bool: True if connection is good.
    """
    buffer = StringIO()
    # print to buffer
    print(message, file=buffer)  # noqa: T001

    error = check_connectivity(cnf, buffer)
    if error:
        if not expect_error:
            getLogger(__name__).error(buffer.getvalue())
        return False

    getLogger(__name__).info(buffer.getvalue())
    return True


def poll_loop(cnf):
    """Polls continuously as specified by looping configuration.

    Arguments:
        cnf (Config): Config object.
    """
    good = is_connection_good(cnf, message=f"Starting broker {version}")

    while cnf.loop:
        if good:
            try:
                poll(cnf)
            except Exception:
                getLogger(__name__).exception("poll failed")
                good = is_connection_good(cnf)
            sleep(cnf.loop)
        else:
            sleep(cnf.loop)
            good = is_connection_good(cnf, expect_error=True)


def poll(cnf):
    """Gathers pipe inputs and polls api, piping output from response.

    Arguments:
        cnf (Config): Config object.
    """
    init_pipes(cnf)

    responses = {}
    for queue_type, queue in separate_pipe_queues(cnf).items():
        responses[queue_type] = poll_api(cnf, queue_type, queue["max"])

    pipe_from_queues(cnf, responses)


def test_pipe(cnf, name):
    """Outputs test data to the specified pipe.

    Arguments:
        cnf (Config): Config object.
        name (str): Name of pipe to test.
    """
    name = name.lower()
    pipe_from_test(init_pipe(name, cnf.pipes[name]))

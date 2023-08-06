# -*- coding: utf-8 -*-
"""Connectivity test."""
import os
import sys
from re import search
from socket import gethostbyname

from requests import RequestException

from procustodibus_broker import DOCS_URL
from procustodibus_broker.api import (
    get_health_info,
    hello_api,
    raise_unless_has_cnf,
    setup_api,
)


def check_connectivity(cnf, output=None):
    """Runs all connectivity checks and outputs issues.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to (defaults to stdout).

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    if not output:
        output = sys.stdout

    try:
        raise_unless_has_cnf(cnf)
    except Exception as e:
        # print to stdout or designated file
        print(str(e), file=output)  # noqa: T001
        return 1

    exit_code = (
        check_dns(cnf, output) + check_health(cnf, output) + check_queues(cnf, output)
    )

    if exit_code:
        # print to stdout or designated file
        print(  # noqa: T001
            "Issues encountered; "
            f"see {DOCS_URL}/guide/integrations/brokers/#troubleshoot to fix",
            file=output,
        )
    else:
        # print to stdout or designated file
        print("All systems go :)", file=output)  # noqa: T001

    return exit_code


def check_dns(cnf, output):
    """Checks that the local DNS resolver can resolve api.procustodib.us.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    hostname = _get_hostname(cnf.api)
    try:
        address = gethostbyname(hostname)
        _good(f"{address} is pro custodibus ip address", output)
        return 0
    except OSError as e:
        _bad(f"cannot lookup ip address for {hostname} ({e})", output)
        return 4


def check_health(cnf, output):
    """Checks connectivity to and the health of the Pro Custodibus API.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    try:
        errors = [x["error"] for x in get_health_info(cnf) if not x["healthy"]]
    except RequestException as e:
        errors = [f"server unavailable ({e})"]

    if errors:
        for error in errors:
            _bad(f"unhealthy pro custodibus api: {error}", output)
        return 8
    else:
        _good("healthy pro custodibus api", output)
        return 0


def check_queues(cnf, output):
    """Checks that the broker can access its queues through the API.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    try:
        _setup_if_available(cnf)
    except (RequestException, ValueError) as e:
        _bad(f"cannot set up access to api ({e})", output)
        return 16

    try:
        broker = hello_api(cnf)
        name = broker["data"][0]["attributes"]["name"]
        _good(f"can access queues on api for {name}", output)
        return 0
    except (RequestException, ValueError) as e:
        _bad(f"cannot access queues on api ({e})", output)
        return 16


def _setup_if_available(cnf):
    """Sets up new broker credentials if setup code is available.

    Arguments:
        cnf (Config): Config object.
    """
    if type(cnf.setup) is dict or os.path.exists(cnf.setup):
        setup_api(cnf)


def _good(message, output):
    """Prints the specified "good" message to the specified output stream.

    Arguments:
        message (str): Message to print.
        output (IOBase): Output stream to write to.
    """
    # print to stdout or designated file
    print(f"... {message} ...", file=output)  # noqa: T001


def _bad(message, output):
    """Prints the specified "bad" message to the specified output stream.

    Arguments:
        message (str): Message to print.
        output (IOBase): Output stream to write to.
    """
    # print to stdout or designated file
    print(f"!!! {message} !!!", file=output)  # noqa: T001


def _get_hostname(url):
    """Extracts the hostname from the specified URL.

    Arguments:
        url (str): URL (eg 'http://test.example.com:8080').

    Returns:
        str: Hostname (eg 'test.example.com').
    """
    match = search(r"(?<=://)[^:/]+", url)
    return match.group(0) if match else None

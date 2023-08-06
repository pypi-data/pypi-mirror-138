# -*- coding: utf-8 -*-
"""Pipe utilities."""

from datetime import datetime
from json import dumps
from logging import getLogger, makeLogRecord
from logging.handlers import SysLogHandler


def init_pipes(cnf):
    """Initializes configured pipes.

    Arguments:
        cnf (Config): Config object.
    """
    for name, pipe in cnf.pipes.items():
        init_pipe(name, pipe)


def init_pipe(name, pipe):
    """Initializes the specified pipe, if not already initialized.

    Arguments:
        name (str): Pipe name.
        pipe (dict): Pipe config.

    Returns:
        dict: Initialized pipe config.
    """
    if pipe.get("initialized"):
        return pipe

    pipe["name"] = name

    to = pipe.get("to")
    if to == "file":
        pipe = init_file_pipe(pipe)
    elif to == "syslog":
        pipe = init_syslog_pipe(pipe)
    else:
        getLogger(__name__).error(f"unknown {name} pipe to: {to}")

    pipe["initialized"] = True
    return pipe


def init_file_pipe(pipe):
    """Initializes the specified file pipe.

    Arguments:
        pipe (dict): Pipe config.

    Returns:
        dict: Initialized pipe config.
    """
    name = pipe.get("name")
    file = pipe.get("file")
    if not file:
        getLogger(__name__).error(f"missing {name} pipe file")
        return pipe

    try:
        with open(file, "a"):
            pass
    except IOError as e:
        getLogger(__name__).error(f"cannot write to {name} pipe file: {e}")
        return pipe

    return pipe


def init_syslog_pipe(pipe):
    """Initializes the specified syslog pipe.

    Arguments:
        pipe (dict): Pipe config.

    Returns:
        dict: Initialized pipe config.
    """
    address = parse_syslog_address(pipe.get("socket", "localhost:514"))
    facility = pipe.get("facility", "local0")
    priority = pipe.get("priority", "info")

    handler = SysLogHandler(address=address, facility=facility)
    handler.ident = pipe.get("tag", "procustodibus") + ": "
    handler.mapPriority = lambda level_name: priority

    pipe["handler"] = handler
    return pipe


def parse_syslog_address(address):
    """Parses the specified socket address.

    Arguments:
        address (str): Socket address (eg 'localhost:514' or '/dev/log' etc).

    Returns:
        Tuple of (host, port) or domain socket path.
    """
    if not address:
        return ("localhost", 514)

    parts = address.split(":")
    if len(parts) == 2:
        return (parts[0], int(parts[1]))
    return address


def separate_pipe_queues(cnf):
    """Extracts each individual queue config from which to pipe.

    Arguments:
        cnf (Config): Config object.

    Returns:
        dict: Dict of queue types to queue config dicts.
    """
    queues = {}
    for pipe in cnf.pipes.values():
        m = pipe.get("max", 100)
        for f in pipe["from"]:
            queue = queues.setdefault(f, {"from": f, "max": m})
            # use smallest max specified for queue
            if queue["max"] > m:
                queue["max"] = m
    return queues


def pipe_from_queues(cnf, responses):
    """Pipes JSON responses from API to the appropriate outputs.

    Arguments:
        cnf (Config): Config object.
        responses (dict): Dict of queue types to JSON responses from API.
    """
    for pipe in cnf.pipes.values():
        data = [d for f in pipe["from"] for d in responses[f]["data"]]
        pipe_from_data(pipe, data)


def pipe_from_test(pipe):
    """Sends test data to the specified pipe.

    Arguments:
        pipe (dict): Pipe config.
    """
    pipe_from_data(
        pipe,
        [
            {
                "attributes": {
                    "created": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                "id": pipe["name"],
                "type": "test",
            }
        ],
    )


def pipe_from_data(pipe, data):
    """Sends data to the specified pipe.

    Arguments:
        pipe (dict): Pipe config.
        data (list): List of data dicts to pipe.
    """
    to = pipe.get("to")
    if to == "file":
        pipe_to_file(pipe, data)
    elif to == "syslog":
        pipe_to_syslog(pipe, data)


def pipe_to_file(pipe, data):
    """Sends data to the specified file pipe.

    Arguments:
        pipe (dict): Pipe config.
        data (list): List of data dicts to pipe.
    """
    with open(pipe["file"], "a") as f:
        for d in data:
            line = dumps(d, separators=(",", ":"))
            # print to file
            print(line, file=f)  # noqa: T001


def pipe_to_syslog(pipe, data):
    """Sends data to the specified syslog pipe.

    Arguments:
        pipe (dict): Pipe config.
        data (list): List of data dicts to pipe.
    """
    for d in data:
        message = dumps(d, separators=(",", ":"))
        record = makeLogRecord({"msg": message})
        pipe["handler"].emit(record)

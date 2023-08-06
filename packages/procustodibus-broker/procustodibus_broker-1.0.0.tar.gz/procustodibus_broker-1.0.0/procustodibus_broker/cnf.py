# -*- coding: utf-8 -*-
"""Config utilities."""

import logging
import logging.config
import os
import sys
from os import environ
from pathlib import Path
from re import fullmatch, split, sub

from inflection import underscore

from procustodibus_broker import DEFAULT_API_URL

DEFAULT_CNF_DIRS = [
    ".",
    "/usr/local/etc/procustodibus/broker",
    "/usr/local/etc/procustodibus",
    "/etc/procustodibus/broker",
    "/etc/procustodibus",
]
DEFAULT_LOGGING_FORMAT = "%(asctime)s %(name)s %(levelname)s: %(message)s"
DEFAULT_LOGGING_LEVEL = "WARNING"

PROCUSTODIBUS_SPLITTABLE = {
    "from": ",",
}


# simpler to keep logic in same function even if it makes cognitive-complexity high
def init_log(root_level="", cnf=None):  # noqa: CCR001
    """Initializes python logging.

    Arguments:
        root_level (str): Root logging level. Defaults to 'WARNING'.
        cnf (str): Path to Python logging configuration file.
    """
    if not root_level:
        root_level = environ.get("PROCUSTODIBUS_LOGGING_LEVEL")

    if cnf and os.path.exists(cnf):
        logging.config.fileConfig(cnf)
        if root_level:
            logging.getLogger().setLevel(root_level.upper())
        logging.getLogger(__name__).debug("init logging configuration from %s", cnf)

    else:
        _setup_default_logging(
            environ.get("PROCUSTODIBUS_LOGGING_FORMAT") or DEFAULT_LOGGING_FORMAT,
            root_level.upper() if root_level else DEFAULT_LOGGING_LEVEL,
        )
        if root_level:
            logging.getLogger(__name__).debug("init logging at %s", root_level)


def _setup_default_logging(log_format, log_level):
    """Sets up logging if no logging config file specified.

    Arguments:
        log_format (str): Log format.
        log_level (str): Log level.
    """
    logging.basicConfig(format=log_format, level=log_level, stream=sys.stdout)


def find_default_cnf():
    """Finds the path to an existing config file.

    Returns:
        str: Path to an existing config file, or blank.
    """
    path = environ.get("PROCUSTODIBUS_CONF")
    if path:
        return path

    for directory in DEFAULT_CNF_DIRS:
        path = f"{directory}/broker.conf"
        if os.path.exists(path):
            return path

    return ""


def load_cnf(cnf_file):
    """Loads the specified procustodibus config file.

    Normalizes keys and values.

    Arguments:
        cnf_file (str): Path to config file, or blank.

    Returns:
        dict: Loaded config settings (dict of strings to normalized values).
    """
    return ini_to_dict(load_ini(cnf_file, PROCUSTODIBUS_SPLITTABLE))


def load_ini(ini_file, splittable=None):
    """Loads the specified ini config file.

    Converts section and key names to snake_case; splits and trims values.

    Arguments:
        ini_file (str): Path to config file, or blank.
        splittable (dict): Optional dict of key names whose values to split.

    Returns:
        dict: Loaded ini settings (dict of strings to list of dicts).
    """
    result = {}
    if not ini_file:
        return result

    section = {}
    _add_ini_value(result, "preface", section)
    if not splittable:
        splittable = {}

    with open(ini_file) as f:
        for line in f:
            line = sub("#.*", "", line).strip()
            section_match = fullmatch(r"\s*\[([^\]]+)\]\s*", line)
            if section_match:
                section_name = underscore(section_match[1])
                section = {}
                _add_ini_value(result, section_name, section)
            elif line:
                _add_ini_line(section, line, splittable)

    return result


def _add_ini_line(section, line, splittable):
    """Parses the specified key=value line and adds it to the specified dict.

    Trims key and value, and converts key to snake_case.

    Splits value by splitter char if key found in splittable dict.

    Arguments:
        section (dict): Dict to add parsed line to.
        line (str): Line to parse (eg 'From = alerts, endpoint_stats').
        splittable (dict): Dict of snake_case keys to splitter characters.
    """
    parts = line.split("=", maxsplit=1)
    if len(parts) < 2:
        parts.append("true")

    # snake_case keys
    # with special-case for ID to convert to id
    key = underscore(sub("ID", "Id", parts[0].strip()))
    splitter = splittable.get(key)
    if splitter:
        value = [x.strip() for x in parts[1].split(splitter)]
    else:
        value = parts[1].strip()

    _add_ini_value(section, key, value)


def _add_ini_value(container, key, value):
    """Adds specified ini value to list of values in specified dict.

    Arguments:
        container (dict): Dict to add value to.
        key (str): Key under which to add value.
        value: Value to add (string or list of strings).
    """
    existing = container.setdefault(key, [])
    if isinstance(value, list):
        existing.extend(value)
    else:
        existing.append(value)


def ini_to_dict(ini):
    """Normalizes property values in the specified dict.

    Drops empty sections, selects first value of non-known-list properties,
    coerces known boolean and number properties.

    Arguments:
        ini (dict): Dict to convert.

    Returns:
        dict: Loaded config settings (dict of strings to normalized values).
    """
    root = {}

    for section_name, section in ini.items():
        src = section[0]
        if src:
            segments = section_name.split(".")
            dst = _create_dict_by_path(root, segments)
            _normalize_cnf_section(src, dst)

    return root


def _normalize_cnf_section(src, dst):
    """Normalizes the property values of the specified config section.

    Copies normalized values from src dict to dst dict.

    Arguments:
        src (dict): Source config section.
        dst (dict): Destination config section.
    """
    for key, value in src.items():
        value = _normalize_cnf_property(key, value)

        segments = key.split(".")
        if len(segments) > 1:
            item_dst = _create_dict_by_path(dst, segments[:-1])
            item_dst[segments[-1]] = value
        else:
            dst[key] = value


def _create_dict_by_path(root, segments):
    """Creates a hierarchy of dictionaries according to the specified path.

    Arguments:
        root (dict): Root under which to create dictionaries.
        segments (list): List of path segments (eg ['foo', 'bar', 'baz']).

    Returns:
        dict: Leaf dictionary.
    """
    for segment in segments:
        root = root.setdefault(segment, {})
    return root


def apply_cnf(obj, cnf):
    """Applies the specified config settings to the specified object.

    Arguments:
        obj: Object to apply settings to.
        cnf (dict): Config settings to apply.
    """
    for key, value in cnf.items():
        if key == "broker" and isinstance(value, dict):
            apply_cnf(obj, value)
        elif key == "pipe":
            obj.pipes = value
        else:
            setattr(obj, key, value)


# keep all special-casing of values together in same function
# even if it makes cognitive-complexity high
def _normalize_cnf_property(key, value):  # noqa: CCR001, CFQ004
    """Adjusts the specified config property value if necessary.

    Arguments:
        key (str): Property name.
        value: Property value.

    Returns:
        Normalized property value.
    """
    # coerce list property values
    if key in ["from"]:
        if isinstance(value, str):
            return [x for x in split(" *, *", value) if x]
        return value

    # default to blank string, extract first list value if list
    if not value:
        value = ""
    elif isinstance(value, list):
        value = value[0] or ""

    # coerce int property values
    if key in ["max"]:
        if isinstance(value, str):
            return int(value)

    return value


class Cnf(dict):
    """Configuration object."""

    # simpler to keep logic in same function even if it makes cognitive-complexity high
    def __init__(self, cnf_file="", verbosity=None, loop=0):  # noqa: CCR001
        """Creates new configuration object.

        Arguments:
            cnf_file (str): Path to configuration file. Defaults to no file.
            verbosity: Root log level. Defaults to 'WARNING'.
                If the number 1 is specified, sets log level to 'INFO'.
                If the number 2 is specified, sets log level to 'DEBUG'.
            loop (int): Seconds to sleep before looping. Defaults to 0 (no loop).
        """
        self.api = DEFAULT_API_URL
        self.broker = ""
        self.pipes = {}
        self.credentials = ""
        self.setup = ""
        self.logging = ""
        self.loop = int(loop or 0)

        if not cnf_file:
            cnf_file = find_default_cnf()
        apply_cnf(self, load_cnf(cnf_file))

        if verbosity == 1:
            verbosity = "INFO"
        if verbosity == 2:
            verbosity = "DEBUG"
        if not self.logging:
            self.logging = _locate_extra_cnf_file(cnf_file, "logging")
        init_log(verbosity, self.logging)

        if not self.credentials:
            self.credentials = _locate_extra_cnf_file(cnf_file, "credentials")
        if not self.setup:
            self.setup = _locate_extra_cnf_file(cnf_file, "setup")


def _locate_extra_cnf_file(cnf_file, extra_type):
    """Builds path to extra conf file (like the credentials file).

    Arguments:
        cnf_file (str): Path to standard cnf file (eg '/etc/procustodibus/broker.conf').
        extra_type (str): Extra type (eg 'credentials').

    Returns:
        str: Path to cnf file (eg '/etc/procustodibus/broker-credentials.conf').
    """
    if not cnf_file:
        return ""

    p = Path(cnf_file)
    return f"{p.parent}/{p.stem}-{extra_type}{p.suffix}"

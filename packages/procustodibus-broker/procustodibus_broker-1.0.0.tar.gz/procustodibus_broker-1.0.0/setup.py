# -*- coding: utf-8 -*-
"""Setuptools script for app."""
from setuptools import setup

from procustodibus_broker import __version__ as version

with open("README.md") as f:
    description = f.read()

with open("requirements/prod.txt") as f:
    requirements = f.read().splitlines()

with open("requirements/lint.txt") as f:
    requirements_lint = f.read().splitlines()

with open("requirements/test.txt") as f:
    requirements_test = f.read().splitlines()

setup(
    name="procustodibus_broker",
    version=version,
    description=(
        "Pushes events from Pro Custodibus into your security management systems."
    ),
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://www.procustodibus.com/",
    project_urls={
        "Changelog": (
            "https://docs.procustodibus.com/guide/integrations/brokers/#changelog"
        ),
        "Documentation": "https://docs.procustodibus.com/guide/integrations/brokers/",
        "Source": "https://git.sr.ht/~arx10/procustodibus-broker",
        "Tracker": "https://todo.sr.ht/~arx10/procustodibus-broker",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="MIT",
    author="Arcem Tene",
    author_email="dev@arcemtene.com",
    packages=["procustodibus_broker"],
    entry_points={
        "console_scripts": [
            "procustodibus-broker = procustodibus_broker.cli:main",
            "procustodibus-broker-credentials = procustodibus_broker.credentials:main",
        ],
    },
    install_requires=requirements,
    extras_require={"lint": requirements_lint, "test": requirements_test},
    python_requires=">=3.8",
    zip_safe=True,
)

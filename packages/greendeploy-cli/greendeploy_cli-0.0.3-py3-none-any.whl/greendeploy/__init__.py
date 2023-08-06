"""GreenDeploy is a framework that makes it easy to build Dockerized Django projects
by providing uniform templates.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("greendeploy-cli")
except PackageNotFoundError:
    # package is not installed
    pass


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

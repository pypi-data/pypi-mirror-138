# Copyright Okera Inc.
#
#
#
# pylint: disable=wrong-import-order
from . import _version
__version__ = _version.get_versions()['version']

def version():
    """ Returns version string of this module. """
    return __version__

from okera_fs_aws.plugin.aws import awscli_initialize




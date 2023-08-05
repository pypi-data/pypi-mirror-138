# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals


def get_packages(callback=None):
    try:
        from pip import get_installed_distributions
    except ImportError:
        # pip decided to hide this internal api in version 10.0.0+
        from pip._internal.utils.misc import get_installed_distributions

    installed_packages = get_installed_distributions()
    for installed_package in installed_packages:
        if callback:
            callback(installed_package)
    return installed_packages

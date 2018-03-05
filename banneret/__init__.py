"""Banneret package source code."""

import sys

from banneret.main import BanneretMacOS, BanneretLinux, Docker

if sys.platform == 'darwin':
    Banneret = BanneretMacOS
elif sys.platform.startswith('linux'):
    Banneret = BanneretLinux
else:
    Banneret = None

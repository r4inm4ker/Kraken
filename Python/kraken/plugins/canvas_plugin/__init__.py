"""Kraken Canvas Plug-in."""

import os
import sys

def dccTest():

    # ensure we are running in python standalone
    app = os.path.split(sys.executable)[1]
    return app in ['python', 'python.exe']

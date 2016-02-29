"""Kraken Canvas Plug-in."""

import os

def dccTest():

    krakenDCC = os.environ.get('KRAKEN_DCC')
    if krakenDCC == "Canvas":
        return True
    else:
        return False

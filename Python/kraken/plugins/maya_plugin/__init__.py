"""Kraken Maya Plug-in."""

import os

def dccTest():

    krakenDCC = os.environ.get('KRAKEN_DCC')
    if krakenDCC == "Maya":
        return True
    else:
        return False
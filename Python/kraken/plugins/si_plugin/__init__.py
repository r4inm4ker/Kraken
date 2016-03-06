"""Kraken Softimage Plug-in."""

import os

def dccTest():

    krakenDCC = os.environ.get('KRAKEN_DCC')
    if krakenDCC == "Softimage":
        return True
    else:
        return False
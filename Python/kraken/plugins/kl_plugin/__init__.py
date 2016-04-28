"""Kraken KL Plug-in."""

import os

def dccTest():

    krakenDCC = os.environ.get('KRAKEN_DCC')
    if krakenDCC == "KL":
        return True
    else:
        return False

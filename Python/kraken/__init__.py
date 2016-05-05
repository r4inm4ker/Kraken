"""Kraken Framework."""

import logging

__all__ = ['core', 'helpers', 'plugins', 'ui']

logging.basicConfig(format='[KRAKEN] %(levelname)s: %(message)s', level=logging.INFO)

# Custom inform level for use with UI label getting added to the status bar.
logging.INFORM = 25
logging.addLevelName(logging.INFORM, 'INFORM')
logging.Logger.inform = lambda inst, msg, *args, **kwargs: inst.log(logging.INFORM, msg, *args, **kwargs)

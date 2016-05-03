import logging


class DCCHandler(logging.StreamHandler):
    """Logging Handler for Canvas."""

    def __init__(self, *args, **kwargs):
        super(DCCHandler, self).__init__(args, kwargs)

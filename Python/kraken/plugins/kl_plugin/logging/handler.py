import types


class Handler(logging.StreamHandler):
    """Logging Handler for KL."""

    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(args, kwargs)
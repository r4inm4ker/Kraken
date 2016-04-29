import types


class Handler(logging.StreamHandler):
    """Logging Handler for Canvas."""

    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(args, kwargs)
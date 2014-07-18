"""Kraken - Operator Binding module.

Classes:
Builder -- Component representation.

"""


class OperatorBinding(object):
    """Operator binding object."""

    __kType__ = "OperatorBinding"

    def __init__(self, inputs, outputs):
        super(OperatorBinding, self).__init__()
        self.inputs = inputs
        self.outputs = outputs
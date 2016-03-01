"""Kraken Canvas - Hash module."""

import copy


def makeHash(o):
    """Makes a hash from a dictionary, list, tuple or set to any level, that
    contains only other hashable types (including any lists, tuples, sets, and
    dictionaries).

    Args:
        o (object): Object to hash.

    Returns:
        hash: Hash of the object.

    """

    if isinstance(o, (set, tuple, list)):
        new_o = copy.deepcopy(o)
        for i in range(len(new_o)):
            new_o[i] = makeHash(new_o[i])

        return hash(tuple(frozenset(sorted(new_o))))

    elif not isinstance(o, dict):
        return hash(o)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = makeHash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))

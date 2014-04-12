"""Kraken - encoder module.

Classes:
KrakenEncoder -- Kraken JSON encoder.
KrakenDecoder -- Kraken JSON decoder.
"""

import math
import json

from kraken.core.maths import vec
from kraken.core.maths.rotation import Euler
from kraken.core.maths.rotation import Quat
from kraken.core.maths.matrix import Matrix33
from kraken.core.maths.matrix import Matrix44
from kraken.core.maths import xfo


TYPES = {
            "Vec2": vec.Vec2,
            "Vec3": vec.Vec3,
            "Vec4": vec.Vec4,
            "Euler": Euler,
            "Quat": Quat,
            "Matrix33": Matrix33,
            "Matrix44": Matrix44,
            "Xfo": xfo.Xfo,
        }


class KrakenJSONEncoder(json.JSONEncoder):
    """JSONEncoder class that can encode Kraken object types.

    Custom objects are encoded as JSON object literals (ie, dicts) with
    one key, '__TypeName__' where 'TypeName' is the actual name of the
    type to which the object belongs.  That single key maps to another
    object literal which is just the __dict__ of the object encoded.

    """

    def default(self, obj):

        if hasattr(obj, "jsonEncode"):
            key = '__%s__' % obj.__class__.__name__
            return { key: obj.jsonEncode() }

        return json.JSONEncoder.default(self, obj)
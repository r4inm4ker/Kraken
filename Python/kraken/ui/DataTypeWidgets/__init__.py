"""
Parameter Widgets are registered to the AttributeWidget base class.

The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.

"""

import AttributeWidgetImpl

# Generic widget that inspects classes, and generates a layout for editing the class values.
# from ComplexTypeWidgetImpl import *

# from DictWidgetImpl import *
# from ArrayWidgetImpl import *
# from Vec4WidgetImpl import *
# from Vec2WidgetImpl import *

# String widgets
from LineWidgetImpl import *
from StringWidgetImpl import *
# from FilepathWidgetImpl import *

# Color widgets
from ColorWidgetImpl import *

# Integer widgets
from IntegerWidgetImpl import *
from IntegerSliderWidgetImpl import *

# Scalar widgets
from ScalarWidgetImpl import *
from ScalarSliderWidgetImpl import *

from QuatWidgetImpl import *
from Vec3WidgetImpl import *
from BooleanWidgetImpl import *

# from ComboBoxWidgetImpl import *
# from ListViewWidgetImpl import *

# from Image2DWidgetImpl import *
# from OptionWidgetImpl import *

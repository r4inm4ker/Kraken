"""
Parameter Editors are registered to the BaseValueEditor base class.

The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.

"""

# Generic widget that inspects classes, and generates a layout for editing the class values.
import complex_type_editor

import dict_editor
import array_editor
import vec4_editor
import vec2_editor

# String widgets
import line_editor
import string_editor
import filepath_editor

# Color widgets
import color_editor

# Integer widgets
import integer_editor
import integer_slider_editor

# Scalar widgets
import scalar_editor
import scalar_slider_editor

import quat_editor
import vec3_editor
import boolean_editor

import combo_box_editor
import list_view_editor
import string_list_editor

# import Image2D_editor
# import Option_editor

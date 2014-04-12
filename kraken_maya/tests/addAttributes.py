from kraken.core.objects import elements
from kraken.core.objects import attributes
from kraken.kraken_maya.objects import elements

parentNull = elements.Null("parentNull")
parentNull.visibility = False
parentNull.addAttributeGroup("DisplayInfo_Arm_Settings")
parentNull.addAttribute("bool", "tweaker_toggle", False, group="DisplayInfo_Arm_Settings")

childNull = elements.Null("childNull", parentNull)
childNull.visibility = True

parentNull.build()
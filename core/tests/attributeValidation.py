from kraken.core.objects import attributes
reload(attributes)

myFloatAttr = attributes.FloatAttribute("blend", 0.5, 0.0, 1.0)
myFloatAttr.value = 0.5

myBoolAttr = attributes.BoolAttribute("extras", False)
myBoolAttr.value = True

myStringAttr = attributes.StringAttribute("name", "bob")
myStringAttr.value = "eric"

myIntAttr = attributes.IntegerAttribute("blend", 0, 0, 5)
myIntAttr.value = 1
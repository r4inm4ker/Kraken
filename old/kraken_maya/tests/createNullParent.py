from kraken.kraken_maya.objects import elements

parentNull = elements.Null("parentNull")
parentNull.visibility = False

childNull = elements.Null("childNull", parentNull)
childNull.visibility = True

parentNull.build()
from kraken.kraken_si.objects import elements

parentNull = elements.Null("parentNull")
parentNull.visibility = False

childNull = elements.Null("childNull", parentNull)
childNull.visibility = True

parentNull.build()
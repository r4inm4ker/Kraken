import json

from kraken_examples.bob_guide_data import bob_guide_data
from kraken.helpers.utility_methods import prepareToSave, prepareToLoad


pureJSON = prepareToSave(bob_guide_data)
str1 = json.dumps(pureJSON, indent=2)
print str1

bob_guide_data = prepareToLoad(pureJSON)

# Check that we can preprocess a data struct 2X
bob_guide_data = prepareToLoad(bob_guide_data)

# Re export to pure json
pureJSON = prepareToSave(bob_guide_data)
str2 = json.dumps(pureJSON, indent=2)
print str1 == str2
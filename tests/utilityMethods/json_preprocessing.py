import json

from kraken.examples.bob_guide_data import bob_guide_data
from kraken.helpers.utility_methods import prepareToSave, prepareToLoad


pureJSON = prepareToSave(bob_guide_data)
print json.dumps(pureJSON, indent=2)

bob_guide_data = prepareToLoad(pureJSON)



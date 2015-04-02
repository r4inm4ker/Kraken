
from kraken import plugins
import kraken.examples.insectleg_component
reload(kraken.examples.insectleg_component)
from kraken.examples.insectleg_component import InsectLegComponent

leg = InsectLegComponent("leg")
builder = plugins.getBuilder()
builder.build(leg)

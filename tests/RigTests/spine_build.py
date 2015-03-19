
from kraken import plugins
import kraken.examples.spine_component
reload(kraken.examples.spine_component)
from kraken.examples.spine_component import SpineComponent

spine = SpineComponent("spine")
builder = plugins.getBuilder()
builder.build(spine)

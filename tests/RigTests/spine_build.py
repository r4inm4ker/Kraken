
from kraken import plugins
from kraken.core.maths import Vec3
import kraken.examples.spine_component
from kraken.examples.spine_component import SpineComponent
from kraken.helpers.utility_methods import logHierarchy

spine = SpineComponent("spine", data={
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 6
        })
builder = plugins.getBuilder()
builder.build(spine)

logHierarchy(spine)
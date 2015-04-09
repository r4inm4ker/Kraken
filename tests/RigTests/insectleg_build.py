
from kraken import plugins
from kraken.core.maths import Vec3
import kraken.examples.insectleg_component
from kraken.examples.insectleg_component import InsectLegComponent
from kraken.helpers.utility_methods import logHierarchy

leg = InsectLegComponent("leg", data={
    "jointPositions": [
        Vec3(-0.9811, 9.769, -0.4572),
        Vec3(-5.4488, 8.4418, -0.5348),
        Vec3(-4.0, 3.1516, -1.237),
        Vec3(-6.841, 1.0, -1.237),
        Vec3(-9.841, 0.0, -1.237)
        ]
    })
builder = plugins.getBuilder()
builder.build(leg)

logHierarchy(leg)
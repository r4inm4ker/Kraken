from kraken.core.maths import Vec3, Quat, Xfo

from kraken.core.objects.container import Container

from kraken_components.biped.clavicle_component import ClavicleComponentGuide, ClavicleComponentRig
from kraken_components.biped.spine_component import SpineComponentRig

from kraken.core.profiler import Profiler


class SpineClavRig(Container):
    """Spine Clav Rig

    This example demonstrates how users can create scripted rigs that both load
    data onto a Rig class, and also loads data onto a guide class and pulls the
    data off to the associated Rig class, then builds.

    """

    def __init__(self, name):

        Profiler.getInstance().push("Construct SpineClavRig:" + name)
        super(SpineClavRig, self).__init__(name)

        # Add Components to Layers
        spineComponent = SpineComponentRig("spine", self)
        spineComponent.loadData(data={
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 4
        })

        clavicleLeftComponentGuide = ClavicleComponentGuide("clavicleGuide")
        clavicleLeftComponentGuide.loadData({
            "location": "L",
            "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
        })

        clavicleLeftComponent = ClavicleComponentRig("clavicle", self)
        clavicleLeftComponent.loadData(data=clavicleLeftComponentGuide.getRigBuildData())

        # Clavicle to Spine
        vertebraeOutputs = spineComponent.getOutputByName('spineVertebrae')
        clavicleLeftSpineEndInput = clavicleLeftComponent.getInputByName('spineEnd')
        clavicleLeftSpineEndInput.setConnection(vertebraeOutputs)
        clavicleLeftSpineEndInput.setIndex(2)

        Profiler.getInstance().pop()

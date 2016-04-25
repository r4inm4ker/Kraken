import json

from kraken import plugins
from kraken.core.maths import Xfo, Vec3, Quat
from kraken.core.profiler import Profiler
from kraken.core.configs.config import Config
from kraken.helpers.utility_methods import logHierarchy

from kraken_components.biped.arm_component import ArmComponentGuide, ArmComponentRig


class CustomConfig(Config):
    """Base Configuration for Kraken builders."""

    def __init__(self):
        super(CustomConfig, self).__init__()

    # ======================
    # Name Template Methods
    # ======================
    def initNameTemplate(self):
        """Initializes the name template.

        Returns:
            dict: name template.

        """

        nameTemplate = super(CustomConfig, self).initNameTemplate()
        nameTemplate["formats"] =  {
                                   "Container": ["name"],
                                   "Layer": ["container", "sep", "name"],
                                   "ComponentGroup": ["location", "sep", "name", "sep", "type"],
                                   "default": ["location", "sep", "component", "sep", "name", "sep", "type"],
                                  }

        return nameTemplate




armGuide = ArmComponentGuide("arm")
armGuide.loadData({
        "name": "Arm",
        "location": "L",
        "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
        "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
        "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
        "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                       ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
        "bicepFKCtrlSize": 1.75,
        "forearmFKCtrlSize": 1.5
    })

armGuideData = armGuide.getRigBuildData()

arm = ArmComponentRig()
arm.loadData(armGuideData)

builder = plugins.getBuilder()
builder.buildComponent(arm)

# Set the custom config as the new singleton value.
CustomConfig.makeCurrent()

builder = plugins.getBuilder()
builder.buildComponent(arm)


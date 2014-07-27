from kraken.core.maths.vec import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.cube_control  import CubeControl


class ClavicleComponent(BaseComponent):
    """Clavicle Component"""

    def __init__(self, name, parent=None, side='M'):
        super(ClavicleComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        claviclePosition = Vec3(0.1322, 15.403, -0.5723)
        clavicleUpV = Vec3()
        clavicleUpV.copy(claviclePosition)
        clavicleUpV = clavicleUpV.add(Vec3(0.0, 1.0, 0.0)).unit()
        clavicleEndPosition = Vec3(2.27, 15.295, -0.753)

        # Calculate Clavicle Xfo
        rootToEnd = clavicleEndPosition.subtract(claviclePosition).unit()
        rootToUpV = clavicleUpV.subtract(claviclePosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()
        clavicleXfo = Xfo()

        clavicleXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, claviclePosition)

        # Add Guide Controls
        clavicleCtrl = CubeControl('clavicle')
        clavicleCtrl.alignOnXAxis()
        clavicleLen = claviclePosition.subtract(clavicleEndPosition).length()
        clavicleCtrl.scalePoints(Vec3(clavicleLen, 1.0, 1.0))
        clavicleCtrl.xfo.copy(clavicleXfo)
        clavicleCtrl.setColor("greenBright")

        clavicleCtrlSrtBuffer = SrtBuffer('clavicle')
        clavicleCtrlSrtBuffer.xfo.copy(clavicleCtrl.xfo)
        clavicleCtrlSrtBuffer.addChild(clavicleCtrl)
        self.addChild(clavicleCtrlSrtBuffer)

        # Setup Component Xfo I/O's
        spineEndInput = Locator('spineEnd')
        spineEndInput.xfo.copy(clavicleXfo)

        clavicleOutput = Locator('clavicleEnd')
        clavicleOutput.xfo.copy(clavicleXfo)

        # Setup componnent Attribute I/O's
        armFollowBodyOutputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([clavicleCtrl.getName(), 'To', spineEndInput.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(spineEndInput)
        clavicleCtrlSrtBuffer.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        clavicleEndConstraint = PoseConstraint('_'.join([clavicleOutput.getName(), 'To', clavicleCtrl.getName()]))
        clavicleEndConstraint.addConstrainer(clavicleCtrl)
        clavicleOutput.addConstraint(clavicleEndConstraint)

        # Add Xfo I/O's
        self.addInput(spineEndInput)
        self.addOutput(clavicleOutput)

        self.addOutput(armFollowBodyOutputAttr)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    clavicleLeft = ClavicleComponent("myClavicle", side='L')
    print clavicleLeft.getNumChildren()
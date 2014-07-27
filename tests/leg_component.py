from kraken.core.maths.vec import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.pin_control import PinControl


class LegComponent(BaseComponent):
    """Leg Component"""

    def __init__(self, name, parent=None, side='M'):
        super(LegComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        if self.getSide() == "R":
            ctrlColor = "red"
            femurPosition = Vec3(-0.9811, 9.769, -0.4572)
            kneePosition = Vec3(-1.4488, 5.4418, -0.5348)
            anklePosition = Vec3(-1.841, 1.1516, -1.237)
        else:
            ctrlColor = "greenBright"
            femurPosition = Vec3(0.9811, 9.769, -0.4572)
            kneePosition = Vec3(1.4488, 5.4418, -0.5348)
            anklePosition = Vec3(1.841, 1.1516, -1.237)

        # Calculate Femur Xfo
        rootToAnkle = anklePosition.subtract(femurPosition).unit()
        rootToKnee = kneePosition.subtract(femurPosition).unit()
        bone1Normal = rootToAnkle.cross(rootToKnee).unit()
        bone1ZAxis = rootToKnee.cross(bone1Normal).unit()
        femurXfo = Xfo()
        femurXfo.setFromVectors(rootToKnee, bone1Normal, bone1ZAxis, femurPosition)

        # Calculate Shin Xfo
        kneeToAnkle = anklePosition.subtract(kneePosition).unit()
        kneeToRoot = femurPosition.subtract(kneePosition).unit()
        bone2Normal = kneeToRoot.cross(kneeToAnkle).unit()
        bone2ZAxis = kneeToAnkle.cross(bone2Normal).unit()
        shinXfo = Xfo()
        shinXfo.setFromVectors(kneeToAnkle, bone2Normal, bone2ZAxis, kneePosition)


        # Femur
        femurFKCtrl = CubeControl('femurFK')
        femurFKCtrl.alignOnXAxis()
        femurLen = femurPosition.subtract(kneePosition).length()
        femurFKCtrl.scalePoints(Vec3(femurLen, 1.0, 1.0))
        femurFKCtrl.setColor(ctrlColor)
        femurFKCtrl.xfo.copy(femurXfo)

        femurFKCtrlSrtBuffer = SrtBuffer('femurFK')
        self.addChild(femurFKCtrlSrtBuffer)
        femurFKCtrlSrtBuffer.xfo.copy(femurFKCtrl.xfo)
        femurFKCtrlSrtBuffer.addChild(femurFKCtrl)

        # Shin
        shinFKCtrl = CubeControl('shinFK')
        shinFKCtrl.alignOnXAxis()
        shinLen = kneePosition.subtract(anklePosition).length()
        shinFKCtrl.scalePoints(Vec3(shinLen, 1.0, 1.0))
        shinFKCtrl.setColor(ctrlColor)
        shinFKCtrl.xfo.copy(shinXfo)

        shinFKCtrlSrtBuffer = SrtBuffer('shinFK')
        shinFKCtrlSrtBuffer.xfo.copy(shinFKCtrl.xfo)
        shinFKCtrlSrtBuffer.addChild(shinFKCtrl)
        femurFKCtrl.addChild(shinFKCtrlSrtBuffer)

        # Ankle
        legIKCtrl = PinControl('IK')
        legIKCtrl.xfo.tr.copy(anklePosition)

        if self.getSide() == "R":
            legIKCtrl.rotatePoints(0, 90, 0)
        else:
            legIKCtrl.rotatePoints(0, -90, 0)

        legIKCtrl.setColor(ctrlColor)

        legIKCtrlSrtBuffer = SrtBuffer('IK')
        legIKCtrlSrtBuffer.xfo.copy(legIKCtrl.xfo)
        legIKCtrlSrtBuffer.addChild(legIKCtrl)
        self.addChild(legIKCtrlSrtBuffer)

        # Setup component Xfo I/O's
        legPelvisInput = Locator('pelvisInput')
        legPelvisInput.xfo.copy(femurXfo)
        legEndOutput = Locator('legEnd')
        legEndOutput.xfo.tr.copy(anklePosition)

        # Setup componnent Attribute I/O's
        legFollowPelvisInputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint inputs
        legRootInputConstraint = PoseConstraint('_'.join([legIKCtrl.getName(), 'To', legPelvisInput.getName()]))
        legRootInputConstraint.setMaintainOffset(True)
        legRootInputConstraint.addConstrainer(legPelvisInput)
        femurFKCtrlSrtBuffer.addConstraint(legRootInputConstraint)

        # Constraint outputs
        legEndOutputConstraint = PoseConstraint('_'.join([legEndOutput.getName(), 'To', legIKCtrl.getName()]))
        legEndOutputConstraint.addConstrainer(legIKCtrl)
        legEndOutput.addConstraint(legEndOutputConstraint)

        # Add Xfo I/O's
        self.addInput(legPelvisInput)
        self.addOutput(legEndOutput)

        # Add Attribute I/O's
        self.addInput(legFollowPelvisInputAttr)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    legLeft = LegComponent("myArm", side='L')
    print legLeft.getNumChildren()
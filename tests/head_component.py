from kraken.core.maths.vec import Vec3

from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.locator import Locator
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.circle_control import CircleControl
from kraken.core.objects.controls.sphere_control import SphereControl


class HeadComponent(BaseComponent):
    """Head Component"""

    def __init__(self, name, parent=None, side='M'):
        super(HeadComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        headPosition = Vec3(0.0, 17.4756, -0.421)
        headEndPosition = Vec3(0.0, 19.5, -0.421)
        eyeLeftPosition = Vec3(0.3497, 18.0878, 0.6088)
        eyeRightPosition = Vec3(-0.3497, 18.0878, 0.6088)
        jawPosition = Vec3(0.0, 17.613, -0.2731)

        # Head
        headCtrl = CircleControl('head')
        headCtrl.rotatePoints(0, 0, 90)
        headCtrl.scalePoints(Vec3(2.5, 2.5, 2.5))
        headCtrl.translatePoints(Vec3(0, 1, 0.25))
        headCtrl.xfo.tr.copy(headPosition)
        headCtrl.setColor("yellow")

        headCtrlSrtBuffer = SrtBuffer('head')
        self.addChild(headCtrlSrtBuffer)
        headCtrlSrtBuffer.xfo.copy(headCtrl.xfo)
        headCtrlSrtBuffer.addChild(headCtrl)

        # Eye Left
        eyeLeftCtrl = SphereControl('eyeLeft')
        eyeLeftCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        eyeLeftCtrl.xfo.tr.copy(eyeLeftPosition)
        eyeLeftCtrl.setColor("blueMedium")

        eyeLeftCtrlSrtBuffer = SrtBuffer('eyeLeft')
        headCtrl.addChild(eyeLeftCtrlSrtBuffer)
        eyeLeftCtrlSrtBuffer.xfo.copy(eyeLeftCtrl.xfo)
        eyeLeftCtrlSrtBuffer.addChild(eyeLeftCtrl)

        # Eye Right
        eyeRightCtrl = SphereControl('eyeRight')
        eyeRightCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        eyeRightCtrl.xfo.tr.copy(eyeRightPosition)
        eyeRightCtrl.setColor("blueMedium")

        eyeRightCtrlSrtBuffer = SrtBuffer('eyeRight')
        headCtrl.addChild(eyeRightCtrlSrtBuffer)
        eyeRightCtrlSrtBuffer.xfo.copy(eyeRightCtrl.xfo)
        eyeRightCtrlSrtBuffer.addChild(eyeRightCtrl)

        # Jaw
        jawCtrl = CubeControl('jaw')
        jawCtrl.alignOnYAxis(negative=True)
        jawCtrl.alignOnZAxis()
        jawCtrl.scalePoints(Vec3(1.45, 0.65, 1))
        jawCtrl.translatePoints(Vec3(0, 0, 0))
        jawCtrl.xfo.tr.copy(jawPosition)
        jawCtrl.setColor("orange")

        jawCtrlSrtBuffer = SrtBuffer('jawSrtBuffer')
        headCtrl.addChild(jawCtrlSrtBuffer)
        jawCtrlSrtBuffer.xfo.copy(jawCtrl.xfo)
        jawCtrlSrtBuffer.addChild(jawCtrl)

        # Setup Component Xfo I/O's
        headBaseInput = Locator('headBase')
        headBaseInput.xfo.copy(headCtrl.xfo)
        headOutput = Locator('head')
        headOutput.xfo.copy(headCtrl.xfo)

        # Setup componnent Attribute I/O's
        armFollowBodyOutputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint inputs
        headInputConstraint = PoseConstraint('_'.join([headCtrlSrtBuffer.getName(), 'To', headBaseInput.getName()]))
        headInputConstraint.setMaintainOffset(True)
        headInputConstraint.addConstrainer(headBaseInput)
        headCtrlSrtBuffer.addConstraint(headInputConstraint)

        # Add Xfo I/O's
        self.addInput(headBaseInput)

        self.addOutput(armFollowBodyOutputAttr)
        self.addOutput(headOutput)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    head = HeadComponent("myClavicle")
    print head.getNumChildren()
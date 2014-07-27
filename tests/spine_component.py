from kraken.core.maths.vec import Vec3

from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.locator import Locator
from kraken.core.objects.controls.circle_control  import  CircleControl


class SpineComponent(BaseComponent):
    """Spine Component"""

    def __init__(self, name, parent=None, side='M'):
        super(SpineComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # COG
        cogCtrl = CircleControl('cog')
        cogCtrl.scalePoints(Vec3(6.0, 6.0, 6.0))
        cogCtrl.xfo.tr = Vec3(0.0, 11.1351, -0.1382)
        cogCtrl.setColor("orange")
        self.addChild(cogCtrl)

        # Spine01
        spine01Ctrl = CircleControl('spine01')
        spine01Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine01Ctrl.xfo.tr = Vec3(0.0, 11.1351, -0.1382)
        spine01Ctrl.setColor("yellow")

        spine01CtrlSrtBuffer = Locator('spine01SrtBuffer')
        spine01CtrlSrtBuffer.xfo.copy(spine01Ctrl.xfo)
        spine01CtrlSrtBuffer.addChild(spine01Ctrl)
        cogCtrl.addChild(spine01CtrlSrtBuffer)

        # Spine02
        spine02Ctrl = CircleControl('spine02')
        spine02Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine02Ctrl.xfo.tr = Vec3(0.0, 12.3085, -0.265)
        spine02Ctrl.setColor("yellow")

        spine02CtrlSrtBuffer = Locator('spine02SrtBuffer')
        spine02CtrlSrtBuffer.xfo.copy(spine02Ctrl.xfo)
        spine02CtrlSrtBuffer.addChild(spine02Ctrl)
        spine01Ctrl.addChild(spine02CtrlSrtBuffer)

        # Spine03
        spine03Ctrl = CircleControl('spine03')
        spine03Ctrl.scalePoints(Vec3(4.0, 4.0, 4.0))
        spine03Ctrl.xfo.tr = Vec3(0.0, 13.1051, -0.4821)
        spine03Ctrl.setColor("yellow")

        spine03CtrlSrtBuffer = Locator('spine03SrtBuffer')
        spine03CtrlSrtBuffer.xfo.copy(spine03Ctrl.xfo)
        spine03CtrlSrtBuffer.addChild(spine03Ctrl)
        spine02Ctrl.addChild(spine03CtrlSrtBuffer)

        # Setup component Xfo I/O's
        spineBaseOutput = Locator('spineBase')
        spineBaseOutput.xfo.tr.copy(spine01Ctrl.xfo.tr)

        spineEndOutput = Locator('spineEnd')
        spineEndOutput.xfo.tr.copy(spine03Ctrl.xfo.tr)

        # Constraint outputs
        spineBaseOutputConstraint = PoseConstraint('_'.join([spineBaseOutput.getName(), 'To', 'spineBase']))
        spineBaseOutputConstraint.addConstrainer(spine01Ctrl)
        spineBaseOutput.addConstraint(spineBaseOutputConstraint)

        spineEndOutputConstraint = PoseConstraint('_'.join([spineEndOutput.getName(), 'To', 'spineEnd']))
        spineEndOutputConstraint.addConstrainer(spine03Ctrl)
        spineEndOutput.addConstraint(spineEndOutputConstraint)

        # Add Xfo I/O's
        self.addOutput(spineBaseOutput)
        self.addOutput(spineEndOutput)

        # Add Attribute I/O's


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    spine = SpineComponent("mySpine")
    print spine.getNumChildren()
from kraken.core.maths import Vec3

from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.helpers.utility_methods import logHierarchy
from kraken.core.profiler import Profiler


class HeadComponent(Component):
    """Head Component"""

    def __init__(self, name, parent=None, data={}):

        location = data.get('location', 'M')

        Profiler.getInstance().push("Construct Head Component:" + name + " location:" + location)
        super(HeadComponent, self).__init__(name, parent, location)


        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        headPosition = data['headPosition']
        headEndPosition = data['headEndPosition']
        eyeLeftPosition = data['eyeLeftPosition']
        eyeRightPosition = data['eyeRightPosition']
        jawPosition = data['jawPosition']

        # Head
        headCtrlSrtBuffer = SrtBuffer('head', parent=self)
        headCtrlSrtBuffer.xfo.tr = headPosition

        headCtrl = Control('head', parent=headCtrlSrtBuffer, shape="circle")
        headCtrl.rotatePoints(0, 0, 90)
        headCtrl.scalePoints(Vec3(3, 3, 3))
        headCtrl.translatePoints(Vec3(0, 1, 0.25))
        headCtrl.xfo.tr = headPosition

        # Eye Left
        eyeLeftCtrlSrtBuffer = SrtBuffer('eyeLeft', parent=headCtrl)
        eyeLeftCtrlSrtBuffer.xfo.tr = eyeLeftPosition

        eyeLeftCtrl = Control('eyeLeft', parent=eyeLeftCtrlSrtBuffer, shape="sphere")
        eyeLeftCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        eyeLeftCtrl.xfo.tr = eyeLeftPosition
        eyeLeftCtrl.setColor("blueMedium")

        # Eye Right
        eyeRightCtrlSrtBuffer = SrtBuffer('eyeRight', parent=headCtrl)
        eyeRightCtrlSrtBuffer.xfo.tr = eyeRightPosition

        eyeRightCtrl = Control('eyeRight', parent=eyeRightCtrlSrtBuffer, shape="sphere")
        eyeRightCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        eyeRightCtrl.xfo.tr = eyeRightPosition
        eyeRightCtrl.setColor("blueMedium")

        # Jaw
        jawCtrlSrtBuffer = SrtBuffer('jawSrtBuffer', parent=headCtrl)
        jawCtrlSrtBuffer.xfo.tr = jawPosition

        jawCtrl = Control('jaw', parent=jawCtrlSrtBuffer, shape="cube")
        jawCtrl.alignOnYAxis(negative=True)
        jawCtrl.alignOnZAxis()
        jawCtrl.scalePoints(Vec3(1.45, 0.65, 1.25))
        jawCtrl.translatePoints(Vec3(0, -0.25, 0))
        jawCtrl.xfo.tr = jawPosition
        jawCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========

        headDef = Joint('head')
        headDef.setComponent(self)

        jawDef = Joint('jaw')
        jawDef.setComponent(self)

        eyeLeftDef = Joint('eyeLeft')
        eyeLeftDef.setComponent(self)

        eyeRightDef = Joint('eyeRight')
        eyeRightDef.setComponent(self)

        deformersLayer = self.getLayer('deformers')
        deformersLayer.addChild(headDef)
        deformersLayer.addChild(jawDef)
        deformersLayer.addChild(eyeLeftDef)
        deformersLayer.addChild(eyeRightDef)


        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        headBaseInput = Locator('headBase')
        headBaseInput.xfo = headCtrl.xfo

        headOutput = Locator('head')
        headOutput.xfo = headCtrl.xfo
        jawOutput = Locator('jaw')
        jawOutput.xfo = jawCtrl.xfo
        eyeLOutput = Locator('eyeL')
        eyeLOutput.xfo = eyeLeftCtrl.xfo
        eyeROutput = Locator('eyeR')
        eyeROutput.xfo = eyeRightCtrl.xfo

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        headInputConstraint = PoseConstraint('_'.join([headCtrlSrtBuffer.getName(), 'To', headBaseInput.getName()]))
        headInputConstraint.setMaintainOffset(True)
        headInputConstraint.addConstrainer(headBaseInput)
        headCtrlSrtBuffer.addConstraint(headInputConstraint)

        # Constraint outputs
        headOutputConstraint = PoseConstraint('_'.join([headOutput.getName(), 'To', headCtrl.getName()]))
        headOutputConstraint.setMaintainOffset(True)
        headOutputConstraint.addConstrainer(headCtrl)
        headOutput.addConstraint(headOutputConstraint)

        jawOutputConstraint = PoseConstraint('_'.join([jawOutput.getName(), 'To', jawCtrl.getName()]))
        jawOutputConstraint.setMaintainOffset(True)
        jawOutputConstraint.addConstrainer(jawCtrl)
        jawOutput.addConstraint(jawOutputConstraint)

        eyeLOutputConstraint = PoseConstraint('_'.join([eyeLOutput.getName(), 'To', eyeLeftCtrl.getName()]))
        eyeLOutputConstraint.setMaintainOffset(True)
        eyeLOutputConstraint.addConstrainer(eyeLeftCtrl)
        eyeLOutput.addConstraint(eyeLOutputConstraint)

        eyeROutputConstraint = PoseConstraint('_'.join([eyeROutput.getName(), 'To', eyeRightCtrl.getName()]))
        eyeROutputConstraint.setMaintainOffset(True)
        eyeROutputConstraint.addConstrainer(eyeRightCtrl)
        eyeROutput.addConstraint(eyeROutputConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(headBaseInput)

        self.addOutput(headOutput)
        self.addOutput(jawOutput)
        self.addOutput(eyeLOutput)
        self.addOutput(eyeROutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        # spliceOp = SpliceOperator("headDeformerSpliceOp", "HeadConstraintSolver", "KrakenHeadConstraintSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # # Add Xfo Inputstrl)
        # spliceOp.setInput("headConstrainer", headOutput)
        # spliceOp.setInput("jawConstrainer", jawOutput)
        # spliceOp.setInput("eyeLeftConstrainer", eyeLOutput)
        # spliceOp.setInput("eyeRightConstrainer", eyeROutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("headDeformer", headDef)
        # spliceOp.setOutput("jawDeformer", jawDef)
        # spliceOp.setOutput("eyeLeftDeformer", eyeLeftDef)
        # spliceOp.setOutput("eyeRightDeformer", eyeRightDef)

        Profiler.getInstance().pop()

    def buildRig(self, parent):
        pass

from kraken.core.kraken_system import KrakenSystem
KrakenSystem.getInstance().registerComponent(HeadComponent)


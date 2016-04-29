from kraken.core.maths import Xfo
from kraken.core.maths import Vec3

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.components.component_output import ComponentOutput
from kraken.core.objects.joint import Joint
from kraken.core.objects.control import Control
from kraken.core.objects.transform import Transform

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler


class TwistComponent(BaseExampleComponent):
    """Twist Component"""

    def __init__(self, name='twist', parent=None):
        super(TwistComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.spineMainSrtInputTgt = self.createInput('mainSrt', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.originInputTgt = self.createInput('origin', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.insertInputTgt = self.createInput('insert', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.twistJointOutput = self.createOutput('twistJoints', dataType='Xfo[]')

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class TwistComponentGuide(TwistComponent):
    """Twist Component Guide"""

    def __init__(self, name='twist', parent=None):

        Profiler.getInstance().push('Construct Spine Guide Component:' + name)
        super(TwistComponentGuide, self).__init__(name, parent)

        # =========
        # Controls
        # ========
        guideSettingsAttrGrp = AttributeGroup('GuideSettings', parent=self)
        self.numDeformersAttr = IntegerAttribute('numDeformers', value=1, minValue=0, maxValue=20, parent=guideSettingsAttrGrp)
        self.blendBiasAttr = ScalarAttribute('blendBias', value=0.0, minValue=0, maxValue=1.0, parent=guideSettingsAttrGrp)

        # Guide Controls
        triangleCtrl = Control('triangle', shape='triangle')
        triangleCtrl.rotatePoints(90, 0, 0)
        triangleCtrl.scalePoints(Vec3(0.25, 0.25, 0.25))
        triangleCtrl.scalePoints(Vec3(1.0, 0.5, 1.0))
        triangleCtrl.translatePoints(Vec3(0.0, 1.25, 0.0))
        triangleCtrl.rotatePoints(0, 90, 0)

        self.originCtrl = Control('origin', parent=self.ctrlCmpGrp, shape='circle')
        self.originCtrl.rotatePoints(90, 0, 0)
        self.originCtrl.rotatePoints(0, 90, 0)
        self.originCtrl.appendCurveData(triangleCtrl.getCurveData())
        self.insertCtrl = Control('insert', parent=self.ctrlCmpGrp, shape='circle')
        self.insertCtrl.rotatePoints(90, 0, 0)
        self.insertCtrl.rotatePoints(0, 90, 0)
        self.insertCtrl.appendCurveData(triangleCtrl.getCurveData())

        self.default_data = {
            'name': name,
            'location': 'M',
            'blendBias': 0.5,
            'originXfo': Xfo(Vec3(0.0, 0.0, 0.0)),
            'insertXfo': Xfo(Vec3(5.0, 0.0, 0.0)),
            'numDeformers': 5
        }

        self.loadData(self.default_data)

        Profiler.getInstance().pop()


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = super(TwistComponentGuide, self).saveData()

        data['blendBias'] = self.blendBiasAttr.getValue()
        data['originXfo'] = self.originCtrl.xfo
        data['insertXfo'] = self.insertCtrl.xfo
        data['numDeformers'] = self.numDeformersAttr.getValue()

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(TwistComponentGuide, self).loadData(data)

        self.blendBiasAttr.setValue(data.get('blendBias', 0.0))
        self.originCtrl.xfo = data.get('originXfo', Xfo())
        self.insertCtrl.xfo = data.get('insertXfo', Xfo())
        self.numDeformersAttr.setValue(data.get('numDeformers', 5))

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(TwistComponentGuide, self).getRigBuildData()

        data['blendBias'] = self.blendBiasAttr.getValue()

        data['originXfo'] = self.originCtrl.xfo
        data['insertXfo'] = self.insertCtrl.xfo

        originUpVXfo = Xfo(Vec3(0.0, 1.0, 0.0))
        insertUpVXfo = Xfo(Vec3(0.0, 1.0, 0.0))

        data['originUpVXfo'] = self.originCtrl.xfo * originUpVXfo
        data['insertUpVXfo'] = self.insertCtrl.xfo * insertUpVXfo

        data['numDeformers'] = self.numDeformersAttr.getValue()

        return data


    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):
        """Enables introspection of the class prior to construction to determine if it is a guide component.

        Return:
        The true if this component is a guide component.

        """

        return 'Guide'

    @classmethod
    def getRigComponentClass(cls):
        """Returns the corresponding rig component class for this guide component class

        Return:
        The rig component class.

        """

        return TwistComponentRig


class TwistComponentRig(TwistComponent):
    """Twist Component"""

    def __init__(self, name="spine", parent=None):

        Profiler.getInstance().push("Construct Spine Rig Component:" + name)
        super(TwistComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        self.originTransform = Transform('origin', parent=self.ctrlCmpGrp)
        self.originUpVTransform = Transform('originUpV', parent=self.ctrlCmpGrp)
        self.insertTransform = Transform('insert', parent=self.ctrlCmpGrp)
        self.insertUpVTransform = Transform('insertUpV', parent=self.ctrlCmpGrp)

        # Add Params to origin transform
        twistSettings = AttributeGroup("DisplayInfo_TwistSettings", parent=self.originTransform)
        self.blendBiasInputAttr = ScalarAttribute('blendBias', value=0.0, minValue=0.0, maxValue=1.0, parent=twistSettings)

        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)
        self.deformerJoints = []
        self.twistOutputs = []
        self.setNumDeformers(1)

        # =====================
        # Create Component I/O
        # =====================
        # Setup component Xfo I/O's
        self.twistJointOutput.setTarget(self.twistOutputs)


        # ============
        # Constraints
        # ============
        # Constrain inputs

        # Origin and Insert
        constraintName = '_'.join([self.originTransform.getName(),
                                   'To',
                                   self.originInputTgt.getName()])

        self.originInputConstraint = self.originTransform.constrainTo(
            self.originInputTgt,
            constraintType='Position',
            maintainOffset=True,
            name=constraintName)

        constraintName = '_'.join([self.insertTransform.getName(),
                                   'To',
                                   self.insertInputTgt.getName()])

        self.insertInputConstraint = self.insertTransform.constrainTo(
            self.insertInputTgt,
            constraintType='Position',
            maintainOffset=True,
            name=constraintName)

        # Up Vectors
        constraintName = '_'.join([self.originUpVTransform.getName(),
                                   'To',
                                   self.originInputTgt.getName()])

        self.originUpVInputConstraint = self.originUpVTransform.constrainTo(
            self.originInputTgt,
            constraintType='Pose',
            maintainOffset=True,
            name=constraintName)

        constraintName = '_'.join([self.insertUpVTransform.getName(),
                                   'To',
                                   self.insertInputTgt.getName()])

        self.insertUpVInputConstraint = self.insertUpVTransform.constrainTo(
            self.insertInputTgt,
            constraintType='Pose',
            maintainOffset=True,
            name=constraintName)

        # Constrain outputs


        # ===============
        # Add Splice Ops
        # ===============
        # Add Spine Splice Op
        self.twistKLOp = KLOperator('TwistOp', 'TwistSolver', 'Kraken')
        self.addOperator(self.twistKLOp)

        # Add Att Inputs
        self.twistKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.twistKLOp.setInput('rigScale', self.rigScaleInputAttr)
        self.twistKLOp.setInput('blendBias', self.blendBiasInputAttr)

        # Add Xfo Inputs
        self.twistKLOp.setInput('origin', self.originTransform)
        self.twistKLOp.setInput('originUpV', self.originUpVTransform)
        self.twistKLOp.setInput('insert', self.insertTransform)
        self.twistKLOp.setInput('insertUpV', self.insertUpVTransform)

        # Add Xfo Outputs
        self.twistKLOp.setOutput('pose', self.twistOutputs)

        # # Add Deformer Splice Op
        self.deformersToOutputsKLOp = KLOperator('twistDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.deformersToOutputsKLOp)

        # Add Att Inputs
        self.deformersToOutputsKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.deformersToOutputsKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Outputs
        self.deformersToOutputsKLOp.setInput('constrainers', self.twistOutputs)

        # Add Xfo Outputs
        self.deformersToOutputsKLOp.setOutput('constrainees', self.deformerJoints)

        Profiler.getInstance().pop()


    def setNumDeformers(self, numDeformers):

        # Add new deformers and outputs
        for i in xrange(len(self.twistOutputs), numDeformers):
            name = 'twist' + str(i + 1).zfill(2)
            spineOutput = ComponentOutput(name, parent=self.outputHrcGrp)
            self.twistOutputs.append(spineOutput)

        for i in xrange(len(self.deformerJoints), numDeformers):
            name = 'twist' + str(i + 1).zfill(2)
            spineDef = Joint(name, parent=self.defCmpGrp)
            spineDef.setComponent(self)
            self.deformerJoints.append(spineDef)

        return True


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(TwistComponentRig, self).loadData(data)

        blendBias = data.get('blendBias')
        originXfo = data.get('originXfo')
        insertXfo = data.get('insertXfo')
        originUpVXfo = data.get('originUpVXfo')
        insertUpVXfo = data.get('insertUpVXfo')
        numDeformers = data.get('numDeformers')

        self.blendBiasInputAttr.setValue(blendBias)

        self.originTransform.xfo = originXfo
        self.originUpVTransform.xfo = originUpVXfo
        self.insertTransform.xfo = insertXfo
        self.insertUpVTransform.xfo = insertUpVXfo

        self.originInputTgt.xfo = originXfo
        self.insertInputTgt.xfo = insertXfo

        # Update number of deformers and outputs
        self.setNumDeformers(numDeformers)

        # Evaluate Constraints
        self.originInputConstraint.evaluate()
        self.insertInputConstraint.evaluate()
        self.originUpVInputConstraint.evaluate()
        self.insertUpVInputConstraint.evaluate()

        # Evaluate Operators
        # self.twistKLOp.evaluate()
        self.deformersToOutputsKLOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(TwistComponentGuide)
ks.registerComponent(TwistComponentRig)

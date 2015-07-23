from kraken.core.maths import Vec3, Vec3, Euler, Quat, Xfo

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.splice_operator import SpliceOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy


class MainSrtComponent(BaseExampleComponent):
    """MainSrt Component Base"""

    def __init__(self, name='mainSrtBase', parent=None, data=None):
        super(MainSrtComponent, self).__init__(name, parent)


        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos

        # Declare Output Xfos
        self.srtOutputTgt = self.createOutput('srt', dataType='Xfo', parent=self.outputHrcGrp)
        self.offsetOutputTgt = self.createOutput('offset', dataType='Xfo', parent=self.outputHrcGrp)

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp)

        # Declare Output Attrs
        self.rigScaleOutputAttr = self.createOutput('rigScale', dataType='Float', parent=self.cmpOutputAttrGrp)


class MainSrtComponentGuide(MainSrtComponent):
    """MainSrt Component Guide"""

    def __init__(self, name='mainSrt', parent=None, data=None):

        Profiler.getInstance().push("Construct MainSrt Guide Component:" + name)
        super(MainSrtComponentGuide, self).__init__(name, parent)

        # =========
        # Attributes
        # =========
        # Add Component Params to IK control
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.bicepFKCtrlSizeInputAttr = ScalarAttribute('mainSrtSize', value=9.0, minValue=1.0,   maxValue=50.0, parent=guideSettingsAttrGrp)

        # =========
        # Controls
        # =========
        mainSrtSize = self.bicepFKCtrlSizeInputAttr.getValue()

        # Guide Controls
        self.mainSrtCtrl = Control('mainSrt', parent=self.ctrlCmpGrp, shape="cube")
        self.mainSrtCtrl.scalePoints(Vec3(mainSrtSize, 1.0, mainSrtSize))

        if data is None:
            data = {
                    "location": 'M',
                    "mainSrtSize": self.bicepFKCtrlSizeInputAttr.getValue(),
                    "mainSrtXfo": Xfo(tr=Vec3(0.0, 0.0, 0.0))
                   }

        self.loadData(data)

        Profiler.getInstance().pop()


    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """
        data = super(MainSrtComponentGuide, self).saveData()

        data["mainSrtSize"] = self.bicepFKCtrlSizeInputAttr.getValue()
        data["mainSrtXfo"] = self.mainSrtCtrl.xfo

        return data


    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(MainSrtComponentGuide, self).loadData( data )

        self.bicepFKCtrlSizeInputAttr.setValue(data["mainSrtSize"])
        self.mainSrtCtrl.xfo = data["mainSrtXfo"]

        return True


    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(MainSrtComponentGuide, self).getRigBuildData()

        data["mainSrtSize"] = self.bicepFKCtrlSizeInputAttr.getValue()
        data["mainSrtXfo"] = self.mainSrtCtrl.xfo

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

        return MainSrtComponentRig

class MainSrtComponentRig(MainSrtComponent):
    """MainSrt Component Rig"""

    def __init__(self, name='mainSrt', parent=None):

        Profiler.getInstance().push("Construct MainSrt Rig Component:" + name)
        super(MainSrtComponentRig, self).__init__(name, parent)


        # =========
        # Controls
        # =========
        # Add Controls
        self.mainSRTCtrlSpace = CtrlSpace('SRT', parent=self.ctrlCmpGrp)
        self.mainSRTCtrl = Control('SRT', shape='circle', parent=self.mainSRTCtrlSpace)

        self.offsetCtrlSpace = CtrlSpace('Offset', parent=self.mainSRTCtrl)
        self.offsetCtrl = Control('Offset', shape='circle', parent=self.offsetCtrlSpace)
        self.offsetCtrl.setColor("orange")

        # Add Component Params to IK control
        mainSrtSettingsAttrGrp = AttributeGroup('DisplayInfo_MainSrtSettings', parent=self.mainSRTCtrl)
        self.rigScaleAttr = ScalarAttribute('rigScale', value=1.0, parent=mainSrtSettingsAttrGrp, minValue=0.1, maxValue=100.0)

        self.rigScaleOutputAttr.connect(self.rigScaleAttr)

        # ==========
        # Deformers
        # ==========


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        srtConstraint = PoseConstraint('_'.join([self.srtOutputTgt.getName(), 'To', self.mainSRTCtrl.getName()]))
        srtConstraint.addConstrainer(self.mainSRTCtrl)
        self.srtOutputTgt.addConstraint(srtConstraint)

        offsetConstraint = PoseConstraint('_'.join([self.offsetOutputTgt.getName(), 'To', self.mainSRTCtrl.getName()]))
        offsetConstraint.addConstrainer(self.offsetCtrl)
        self.offsetOutputTgt.addConstraint(offsetConstraint)


        # ===============
        # Add Splice Ops
        # ===============
        #Add Rig Scale Splice Op
        self.rigScaleSpliceOp = SpliceOperator('rigScaleSpliceOp', 'RigScaleSolver', 'Kraken')
        self.addOperator(self.rigScaleSpliceOp)

        # Add Att Inputs
        self.rigScaleSpliceOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.rigScaleSpliceOp.setInput('rigScale', self.rigScaleOutputAttr)

        # Add Xfo Inputs

        # Add Xfo Outputs
        self.rigScaleSpliceOp.setOutput('target', self.mainSRTCtrlSpace)


        Profiler.getInstance().pop()


    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(MainSrtComponentRig, self).loadData( data )

        # ================
        # Resize Controls
        # ================
        self.mainSRTCtrl.scalePoints(Vec3(data["mainSrtSize"], 1.0, data["mainSrtSize"]))
        self.offsetCtrl.scalePoints(Vec3(data["mainSrtSize"] - 0.5, 1.0, data["mainSrtSize"] - 0.5))

        # =======================
        # Set Control Transforms
        # =======================
        self.mainSRTCtrlSpace.xfo = data["mainSrtXfo"]
        self.mainSRTCtrl.xfo = data["mainSrtXfo"]
        self.offsetCtrlSpace.xfo = data["mainSrtXfo"]
        self.offsetCtrl.xfo = data["mainSrtXfo"]

        # ============
        # Set IO Xfos
        # ============
        self.srtOutputTgt = data["mainSrtXfo"]
        self.offsetOutputTgt = data["mainSrtXfo"]

        self.rigScaleSpliceOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(MainSrtComponentGuide)
ks.registerComponent(MainSrtComponentRig)

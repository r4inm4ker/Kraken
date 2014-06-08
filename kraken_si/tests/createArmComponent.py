from kraken.kraken_si.utils import *
from kraken.kraken_si.utils import splice
from kraken.kraken_core.components import arm
reload (arm)


# ==================
# Create an Arm Rig
# ==================
comp = arm.ArmComponent("arm_L_hrc", side="L")
comp.buildGuide()

comp.initDataFromGuide(comp.guidea)
comp.build()


# ==================
# Setup Splice Op
# ==================
# Get splice inputs
ioHrc = comp.findChild("arm_io_hrc").object3D
bone1FKCtrl = comp.findChild("arm_" + comp.side + "_bicepFK_ctrl").object3D
bone2FKCtrl = comp.findChild("arm_" + comp.side + "_forearmFK_ctrl").object3D
ikHandleCtrl = comp.findChild("arm_" + comp.side + "_ikHandle_ctrl").object3D
armUpVCtrl = comp.findChild("arm_" + comp.side + "_upV_ctrl").object3D
clavicleKineIn = comp.findChild("arm_" + comp.side + "_clavicle_kineIn").object3D
bicepKineOut = comp.findChild("arm_" + comp.side + "_bicep_kineOut").object3D
forearmKineOut = comp.findChild("arm_" + comp.side + "_forearm_kineOut").object3D
wristKineOut = comp.findChild("arm_" + comp.side + "_wrist_kineOut").object3D

# Create Splice Builder
spliceBuilder = splice.SpliceBuilder("D:/dev/rigging/fabric/Splice/armRig.splice")
spliceBuilder.connectDirectNode = ioHrc.Properties("DisplayInfo_Arm_Settings")

# Add Input Connections
spliceBuilder.addConnection("input", "matrix", bone1FKCtrl, "bone1FKCtrl")
spliceBuilder.addConnection("input", "matrix", bone2FKCtrl, "bone2FKCtrl")
spliceBuilder.addConnection("input", "matrix", ikHandleCtrl, "ikHandle")
spliceBuilder.addConnection("input", "matrix", armUpVCtrl, "upV")
spliceBuilder.addConnection("input", "matrix", clavicleKineIn, "rootMat")

# Add Output Connections
spliceBuilder.addConnection("output", "matrix", bicepKineOut, "matrices")
spliceBuilder.addConnection("output", "matrix", forearmKineOut, "matrices")
spliceBuilder.addConnection("output", "matrix", wristKineOut, "matrices")

# Build Splice Node
spliceBuilder.build()
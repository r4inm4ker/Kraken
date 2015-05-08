
from kraken.core.maths import Vec2, Vec3, Euler, Quat, Xfo


bob_guide_data = {
    "components":[
        {
            "class": "kraken.examples.spine_component.SpineComponentGuide",
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 6
        },
        {
            "class": "kraken.examples.neck_component.NeckComponentGuide",
            "neckPosition": Vec3(0.0, 16.5572, -0.6915),
            "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
        }
        # ,
        # {
        #     "class": "kraken.examples.head_component.HeadComponentGuide",
        #     "headPosition": Vec3(0.0, 17.4756, -0.421),
        #     "headEndPosition": Vec3(0.0, 19.5, -0.421),
        #     "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
        #     "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
        #     "jawPosition": Vec3(0.0, 17.613, -0.2731)
        # },
        # {
        #     "class": "kraken.examples.clavicle_component.ClavicleComponentGuide",
        #     "location": "L",
        #     "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
        #     "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
        #     "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
        # },
        # {
        #     "class": "kraken.examples.clavicle_component.ClavicleComponentGuide",
        #     "location": "R",
        #     "clavicleXfo": Xfo(Vec3(-0.1322, 15.403, -0.5723)),
        #     "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
        #     "clavicleEndXfo": Xfo(Vec3(-2.27, 15.295, -0.753))
        # },
        # {
        #     "class": "kraken.examples.arm_component.ArmComponentGuide",
        #     "location": "L",
        #     "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
        #     "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
        #     "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
        #     "bicepFKCtrlSize": 1.75,
        #     "forearmFKCtrlSize": 1.5
        # },
        # {
        #     "class": "kraken.examples.arm_component.ArmComponentGuide",
        #     "location": "R",
        #     "bicepXfo": Xfo(Vec3(-2.27, 15.295, -0.753)),
        #     "forearmXfo": Xfo(Vec3(-5.039, 13.56, -0.859)),
        #     "wristXfo": Xfo(Vec3(-7.1886, 12.2819, 0.4906)),
        #     "bicepFKCtrlSize": 1.75,
        #     "forearmFKCtrlSize": 1.5
        # },
        # {
        #     "class": "kraken.examples.hand_component.HandComponentGuide",
        #     "location": "L",
        #     "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906), 
        #                     ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
        # },
        # {
        #     "class": "kraken.examples.hand_component.HandComponentGuide",
        #     "location": "R",
        #     "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906),
        #                     ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623))
        # },
        # {
        #     "class": "kraken.examples.leg_component.LegComponentGuide",
        #     "location": "L",
        #     "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
        #     "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
        #     "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237))
        # },
        # {
        #     "class": "kraken.examples.foot_component.FootComponentGuide",
        #     "location": "L",
        #     "footXfo": Xfo(tr=Vec3(1.841, 1.1516, -1.237),
        #                    ori=Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190))
        # },
        # {
        #     "class": "kraken.examples.leg_component.LegComponentGuide",
        #     "location": "R",
        #     "femurXfo": Xfo(Vec3(-0.9811, 9.769, -0.4572)),
        #     "kneeXfo": Xfo(Vec3(-1.4488, 5.4418, -0.5348)),
        #     "ankleXfo": Xfo(Vec3(-1.841, 1.1516, -1.237))
        # },
        # {
        #     "class": "kraken.examples.foot_component.FootComponentGuide",
        #     "location": "R",
        #     "footXfo": Xfo(tr=Vec3(-1.841, 1.1516, -1.237),
        #                    ori=Quat(Vec3(0.5695, -0.6377, 0.4190), 0.3053))
        # }
    ],
    "connections": [
        {
            "_comment": "Neck to Spine",
            "source": "spine.spineEnd",
            "target": "neck.neckBase"
        }
        # ,
        # {
        #     "_comment": "Head to Neck",
        #     "source": "neck.neckEnd",
        #     "target": "head.headBase"
        # },
        # {
        #     "_comment": "LClavicle to Spine",
        #     "source": "spine.spineEnd",
        #     "target": "L_ClavicleComponent.spineEnd"
        # },
        # {
        #     "_comment": "LArm to LClavicle",
        #     "source": "L_ClavicleComponent.clavicleEnd",
        #     "target": "L_ArmComponent.clavicleEnd"
        # },
        # {
        #     "_comment": "RArm to RClavicle",
        #     "source": "R_ClavicleComponent.clavicleEnd",
        #     "target": "R_ArmComponent.clavicleEnd"
        # },
        # {
        #     "_comment": "RClavicle to Spine",
        #     "source": "spine.spineEnd",
        #     "target": "R_ClavicleComponent.spineEnd"
        # },
        # {
        #     "_comment": "LHand To LArm Connections. armEndXfo",
        #     "source": "L_ArmComponent.armEndXfo",
        #     "target": "L_HandComponent.armEndXfo"
        # },
        # {
        #     "_comment": "LHand To LArm Connections. armEndPos",
        #     "source": "L_ArmComponent.armEndPos",
        #     "target": "L_HandComponent.armEndPos"
        # },
        # {
        #     "_comment": "RHand To RArm Connections. armEndXfo",
        #     "source": "R_ArmComponent.armEndXfo",
        #     "target": "R_HandComponent.armEndXfo"
        # },
        # {
        #     "_comment": "RHand To RArm Connections. armEndPos",
        #     "source": "R_ArmComponent.armEndPos",
        #     "target": "R_HandComponent.armEndPos"
        # },
        # {
        #     "_comment": "LLeg To Pelvis Connections",
        #     "source": "spine.spineBase",
        #     "target": "L_LegComponent.pelvisInput"
        # },
        # {
        #     "_comment": "RLeg To Pelvis Connections",
        #     "source": "spine.spineBase",
        #     "target": "R_LegComponent.pelvisInput"
        # },
        # {
        #     "_comment": "LFoot To LLeg Connections: legEndXfo",
        #     "source": "L_LegComponent.legEndXfo",
        #     "target": "L_FootComponent.legEndXfo"
        # },
        # {
        #     "_comment": "LFoot To LLeg Connections: legEndPos",
        #     "source": "L_LegComponent.legEndPos",
        #     "target": "L_FootComponent.legEndPos"
        # },
        # {
        #     "_comment": "RFoot To RLeg Connections: legEndXfo",
        #     "source": "R_LegComponent.legEndXfo",
        #     "target": "R_FootComponent.legEndXfo"
        # },
        # {
        #     "_comment": "RFoot To RLeg Connections: legEndPos",
        #     "source": "R_LegComponent.legEndPos",
        #     "target": "R_FootComponent.legEndPos"
        # }
    ]
}


from kraken.core.maths import Vec2, Vec3, Euler, Quat, Xfo


bob_guide_data = {
    "layers":[
        "deformers",
        "controls",
        "geometry"
    ],
    "components":[
        {
            "class":"kraken.examples.spine_component.SpineComponent",
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 6
        },
        {
            "class":"kraken.examples.neck_component.NeckComponent",
            'neckPosition': Vec3(0.0, 16.5572, -0.6915),
            'neckUpVOffset': Vec3(0.0, 0.0, -1.0),
            'neckEndPosition': Vec3(0.0, 17.4756, -0.421)
        },
        {
            "class":"kraken.examples.head_component.HeadComponent",
            "headPosition": Vec3(0.0, 17.4756, -0.421),
            "headEndPosition": Vec3(0.0, 19.5, -0.421),
            "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
            "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
            "jawPosition": Vec3(0.0, 17.613, -0.2731)
        },
        {
            "class":"kraken.examples.clavicle_component.ClavicleComponent",
            "name": "L_Clavicle",
            "location": "L",
            "claviclePosition": Vec3(0.1322, 15.403, -0.5723),
            "clavicleUpVOffset": Vec3(0.0, 1.0, 0.0),
            "clavicleEndPosition": Vec3(2.27, 15.295, -0.753)
        },
        {
            "class":"kraken.examples.arm_component.ArmComponent",
            "name": "L_Arm",
            "location": "L",
            "bicepPosition": Vec3(2.27, 15.295, -0.753),
            "forearmPosition": Vec3(5.039, 13.56, -0.859),
            "wristPosition": Vec3(7.1886, 12.2819, 0.4906),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        },
        {
            "class":"kraken.examples.hand_component.HandComponent",
            "name":"L_Hand",
            "location": "L",
            "handPosition": Vec3(7.1886, 12.2819, 0.4906),
            "handUpV": Vec3(7.7463, 13.1746, 0.4477),
            "handEndPosition": Vec3(7.945, 11.8321, 0.9655),
            "handQuat": Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331),
            "handPos": Vec3(7.1886, 12.2819, 0.4906)
        },
        {
            "class":"kraken.examples.clavicle_component.ClavicleComponent",
            "name":"R_Clavicle",
            "location": "R",
            "claviclePosition": Vec3(-0.1322, 15.403, -0.5723),
            "clavicleUpVOffset": Vec3(0.0, 1.0, 0.0),
            "clavicleEndPosition": Vec3(-2.27, 15.295, -0.753)
        },
        {
            "class":"kraken.examples.arm_component.ArmComponent",
            "name":"R_Arm",
            "location": "R",
            "bicepPosition": Vec3(-2.27, 15.295, -0.753),
            "forearmPosition": Vec3(-5.039, 13.56, -0.859),
            "wristPosition": Vec3(-7.1886, 12.2819, 0.4906),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        },
        {
            "class":"kraken.examples.hand_component.HandComponent",
            "name":"R_Hand",
            "location": "R",
            "handPosition": Vec3(-7.1886, 12.2819, 0.4906),
            "handUpV": Vec3(-7.7463, 13.1746, 0.4477),
            "handEndPosition": Vec3(-7.945, 11.8321, 0.9655),
            "handQuat": Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623),
            "handPos": Vec3(-7.1886, 12.2819, 0.4906)
        },
        {
            "class":"kraken.examples.leg_component.LegComponent",
            "name":"L_Leg",
            "location": "L",
            "femurPosition": Vec3(0.9811, 9.769, -0.4572),
            "kneePosition": Vec3(1.4488, 5.4418, -0.5348),
            "anklePosition": Vec3(1.841, 1.1516, -1.237)
        },
        {
            "class":"kraken.examples.foot_component.FootComponent",
            "name":"L_Foot",
            "location": "L",
            "footQuat": Quat(Vec3(0.6377, -0.5695, 0.3053), 0.4190),
            "footPos": Vec3(1.841, 1.1516, -1.237)
        },
        {
            "class":"kraken.examples.leg_component.LegComponent",
            "name":"R_Leg",
            "location": "R",
            "femurPosition": Vec3(-0.9811, 9.769, -0.4572),
            "kneePosition": Vec3(-1.4488, 5.4418, -0.5348),
            "anklePosition": Vec3(-1.841, 1.1516, -1.237)
        },
        {
            "class":"kraken.examples.foot_component.FootComponent",
            "name":"R_Foot",
            "location": "R",
            "footQuat": Quat(Vec3(0.5695, -0.6377, 0.4190), 0.3053),
            "footPos": Vec3(-1.841, 1.1516, -1.237)
        }
    ],
    "connections": [
        {
            "_comment": "Neck to Spine",
            "source": "SpineComponent.spineEnd",
            "target": "NeckComponent.neckBase"
        },
        {
            "_comment": "Head to Neck",
            "source": "NeckComponent.neckEnd",
            "target": "HeadComponent.headBase"
        },
        {
            "_comment": "LClavicle to Spine",
            "source": "SpineComponent.spineEnd",
            "target": "L_ClavicleComponent.spineEnd"
        },
        {
            "_comment": "LArm to LClavicle",
            "source": "L_ClavicleComponent.clavicleEnd",
            "target": "L_ArmComponent.clavicleEnd"
        },
        {
            "_comment": "RArm to RClavicle",
            "source": "R_ClavicleComponent.clavicleEnd",
            "target": "R_ArmComponent.clavicleEnd"
        },
        {
            "_comment": "RClavicle to Spine",
            "source": "SpineComponent.spineEnd",
            "target": "R_ClavicleComponent.spineEnd"
        },
        {
            "_comment": "LHand To LArm Connections. armEndXfo",
            "source": "L_ArmComponent.armEndXfo",
            "target": "L_HandComponent.armEndXfo"
        },
        {
            "_comment": "LHand To LArm Connections. armEndPos",
            "source": "L_ArmComponent.armEndPos",
            "target": "L_HandComponent.armEndPos"
        },
        {
            "_comment": "RHand To RArm Connections. armEndXfo",
            "source": "R_ArmComponent.armEndXfo",
            "target": "R_HandComponent.armEndXfo"
        },
        {
            "_comment": "RHand To RArm Connections. armEndPos",
            "source": "R_ArmComponent.armEndPos",
            "target": "R_HandComponent.armEndPos"
        },
        {
            "_comment": "LLeg To Pelvis Connections",
            "source": "SpineComponent.spineBase",
            "target": "L_LegComponent.pelvisInput"
        },
        {
            "_comment": "RLeg To Pelvis Connections",
            "source": "SpineComponent.spineBase",
            "target": "R_LegComponent.pelvisInput"
        },
        {
            "_comment": "LFoot To LLeg Connections: legEndXfo",
            "source": "L_LegComponent.legEndXfo",
            "target": "L_FootComponent.legEndXfo"
        },
        {
            "_comment": "LFoot To LLeg Connections: legEndPos",
            "source": "L_LegComponent.legEndPos",
            "target": "L_FootComponent.legEndPos"
        },
        {
            "_comment": "RFoot To RLeg Connections: legEndXfo",
            "source": "R_LegComponent.legEndXfo",
            "target": "R_FootComponent.legEndXfo"
        },
        {
            "_comment": "RFoot To RLeg Connections: legEndPos",
            "source": "R_LegComponent.legEndPos",
            "target": "R_FootComponent.legEndPos"
        }
    ]
}

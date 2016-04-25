"""Example data that can be loaded onto a guide rig."""

from kraken.core.maths import Vec2, Vec3, Euler, Quat, Xfo


bob_guide_data = {
    "components":[
        {
            "class": "kraken_components.biped.spine_component.SpineComponentGuide",
            'cogPosition': Vec3(0.0, 11.1351, -0.1382),
            'spine01Position': Vec3(0.0, 11.1351, -0.1382),
            'spine02Position': Vec3(0.0, 11.8013, -0.1995),
            'spine03Position': Vec3(0.0, 12.4496, -0.3649),
            'spine04Position': Vec3(0.0, 13.1051, -0.4821),
            'numDeformers': 6
        },
        {
            "class": "kraken_components.biped.neck_component.NeckComponentGuide",
            "neckPosition": Vec3(0.0, 16.5572, -0.6915),
            "neckEndPosition": Vec3(0.0, 17.4756, -0.421)
        },
        {
            "class": "kraken_components.biped.head_component.HeadComponentGuide",
            "headPosition": Vec3(0.0, 17.4756, -0.421),
            "headEndPosition": Vec3(0.0, 19.5, -0.421),
            "eyeLeftPosition": Vec3(0.3497, 18.0878, 0.6088),
            "eyeRightPosition": Vec3(-0.3497, 18.0878, 0.6088),
            "jawPosition": Vec3(0.0, 17.613, -0.2731)
        },
        {
            "class": "kraken_components.biped.clavicle_component.ClavicleComponentGuide",
            "name": "Clavicle",
            "location": "L",
            "clavicleXfo": Xfo(Vec3(0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(2.27, 15.295, -0.753))
        },
        {
            "class": "kraken_components.biped.clavicle_component.ClavicleComponentGuide",
            "name": "Clavicle",
            "location": "R",
            "clavicleXfo": Xfo(Vec3(-0.1322, 15.403, -0.5723)),
            "clavicleUpVXfo": Xfo(Vec3(0.0, 1.0, 0.0)),
            "clavicleEndXfo": Xfo(Vec3(-2.27, 15.295, -0.753))
        },
        {
            "class": "kraken_components.biped.arm_component.ArmComponentGuide",
            "name": "Arm",
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(7.1886, 12.2819, 0.4906)),
            "handXfo": Xfo(tr=Vec3(7.1886, 12.2819, 0.4906),
                           ori=Quat(Vec3(-0.0865, -0.2301, -0.2623), 0.9331)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        },
        {
            "class": "kraken_components.biped.arm_component.ArmComponentGuide",
            "name": "Arm",
            "location": "R",
            "bicepXfo": Xfo(Vec3(-2.27, 15.295, -0.753)),
            "forearmXfo": Xfo(Vec3(-5.039, 13.56, -0.859)),
            "wristXfo": Xfo(Vec3(-7.1886, 12.2819, 0.4906)),
            "handXfo": Xfo(tr=Vec3(-7.1886, 12.2819, 0.4906),
                           ori=Quat(Vec3(-0.2301, -0.0865, -0.9331), 0.2623)),
            "bicepFKCtrlSize": 1.75,
            "forearmFKCtrlSize": 1.5
        },
        {
            "class": "kraken_components.biped.leg_component.LegComponentGuide",
            "name": "Leg",
            "location": "L",
            "femurXfo": Xfo(Vec3(0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(1.841, 1.1516, -1.237)),
            "toeXfo": Xfo(Vec3(1.85, 0.4, 0.25)),
            "toeTipXfo": Xfo(Vec3(1.85, 0.4, 1.5))
        },
        {
            "class": "kraken_components.biped.leg_component.LegComponentGuide",
            "name": "Leg",
            "location": "R",
            "femurXfo": Xfo(Vec3(-0.9811, 9.769, -0.4572)),
            "kneeXfo": Xfo(Vec3(-1.4488, 5.4418, -0.5348)),
            "ankleXfo": Xfo(Vec3(-1.841, 1.1516, -1.237)),
            "toeXfo": Xfo(Vec3(-1.85, 0.4, 0.25)),
            "toeTipXfo": Xfo(Vec3(-1.85, 0.4, 1.5))
        }
    ],
    "connections": [
        {
            "_comment": "Neck to Spine",
            "source": "spine:M.spineEnd",
            "target": "neck:M.neckBase"
        },
        {
            "_comment": "Head to Neck",
            "source": "neck:M.neckEnd",
            "target": "head:M.headBase"
        },
        {
            "_comment": "LClavicle to Spine",
            "source": "spine:M.spineEnd",
            "target": "Clavicle:L.spineEnd"
        },
        {
            "_comment": "LArm to LClavicle",
            "source": "Clavicle:L.clavicleEnd",
            "target": "Arm:L.root"
        },
        {
            "_comment": "RArm to RClavicle",
            "source": "Clavicle:R.clavicleEnd",
            "target": "Arm:R.root"
        },
        {
            "_comment": "RClavicle to Spine",
            "source": "spine:M.spineEnd",
            "target": "Clavicle:R.spineEnd"
        },
        {
            "_comment": "LLeg To Pelvis Connections",
            "source": "spine:M.pelvis",
            "target": "Leg:L.pelvisInput"
        },
        {
            "_comment": "RLeg To Pelvis Connections",
            "source": "spine:M.pelvis",
            "target": "Leg:R.pelvisInput"
        }
    ]
}

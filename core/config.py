import json

envConfig = {
                "app": "xsi",
                "namingTemplate": {
                                    "suffixes": {
                                                    "null":"null",
                                                    "control":"ctrl",
                                                    "zero":"zero",
                                                    "srt":"srt",
                                                    "geometry":"geo",
                                                    "curve":"crv",
                                                    "visualCue":"visCue",
                                                    "implicit":"imp",
                                                    "hierarchy":"hrc",
                                                    "upVector":"upV",
                                                    "envelope":"env",
                                                    "group":"grp",
                                                    "parameterIn":"paramIn",
                                                    "parameterOut":"paramOut",
                                                    "kineIn":"kineIn",
                                                    "kineOut":"kineOut",
                                                    "srtIn":"srtIn",
                                                    "srtOut":"srtOut",
                                                    "root":"rt",
                                                    "effector":"eff",
                                                    "bone":"bone",
                                                    "iceHost":"iceHost",
                                                    "pointCloud":"pcloud"
                                                },
                                    "locations": {
                                                    "left":"L",
                                                    "medial":"M",
                                                    "right":"R"
                                                }
                                  }
            }


def setEnvConfigFromFile(filePath):
    """Sets the 'envConfig' from a json file.

    Arguments:
    filePath -- String, path on disk of json config file.

    """

    with file(filePath, "r") as configFile:
        config = json.load(filePath)

    global envConfig
    envConfig = config

    return
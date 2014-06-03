from kraken.plugins.si_plugin.utils import *
from kraken.plugins.si_plugin import interfaces

interfaces.patch()

# class Scene(object):
#     """Softimage Scene Root."""

#     def __init__(self, app="si"):
#         super(Scene, self).__init__()
#         self.app = app
#         self.object3D = si.ActiveProject3.ActiveScene.Root


#     def __str__(self):
#         return str("Kraken Scene: " + self.object3D.Name)


# class Dispatcher(object):
#     """Softimage Dispatcher"""

#     def __init__(self, kObject):
#         super(Dispatcher, self).__init__()
#         self.kObject = kObject


#     def _checkParent(self, kObject):
#         """Check if parent is set, if not set to scene root."""

#         if kObject.parent is None:
#             kObject.parent = Scene()

#         return

#     # =====================
#     # Transform Operations
#     # =====================
#     def _initTransform(self, kObject):
#         """Set the transform in Softimage.

#         Return:
#         True if successful.
#         """

#         xfo = XSIMath.CreateTransform()
#         scl = XSIMath.CreateVector3(kObject.xfo.scl.x, kObject.xfo.scl.y, kObject.xfo.scl.z)
#         quat = XSIMath.CreateQuaternion(kObject.xfo.rot.w, kObject.xfo.rot.v.x, kObject.xfo.rot.v.y, kObject.xfo.rot.v.z)
#         tr = XSIMath.CreateVector3(kObject.xfo.tr.x, kObject.xfo.tr.y, kObject.xfo.tr.z)

#         xfo.SetScaling(scl)
#         xfo.SetRotationFromQuaternion(quat)
#         xfo.SetTranslation(tr)

#         kObject.object3D.Kinematics.Global.PutTransform2(None, xfo)

#         return True


#     def getTranslation(self, kObject):
#         """Get the translation in Softimage.

#         Return:
#         vec3 position.
#         """

#         obj = kObject.object3D
#         position = Vec3(obj.Kinematics.Global.Transform.Translation.X,
#                         obj.Kinematics.Global.Transform.Translation.Y,
#                         obj.Kinematics.Global.Transform.Translation.Z)
#         return position


#     # ====================
#     # Name operations
#     # ====================
#     def _setObjName(self, kObject):
#         """Sets object3D name.

#         Return:
#         True if successful.

#         """

#         kObject.object3D.Name = kObject.buildName()

#         return True


#     # =====================
#     # Visibility operations
#     # =====================
#     def _setVisibility(self, kObject):
#         """Sets object3D visibility.

#         Return:
#         True if successful.

#         """

#         kObject.object3D.Properties("Visibility").Parameters("viewvis").Value = kObject.visibility
#         kObject.object3D.Properties("Visibility").Parameters("rendvis").Value = kObject.visibility

#         return True


#     # ===================
#     # Display operations
#     # ===================
#     def _setDisplay(self, kObject):
#         """Sets object3D display properties.

#         Return:
#         True if successful.

#         """

#         colors = {
#                     "red":[1.0,0.0,0.0],
#                     "green":[0.0,1.0,0.0],
#                     "blue":[0.0,1.0,0.0],
#                     "yellow":[1.0,1.0,0.0],
#                     "orange":[1.0,0.5,0.0],
#                     "purple":[0.5,0.0,1.0],
#                     "magenta":[1.0,0.0,1.0]
#                  }

#         if kObject.color is not None and type(kObject.color) is str and kObject.color in colors.keys():
#             displayProp = kObject.object3D.AddProperty("Display Property")

#             displayProp.Parameters("wirecolorr").Value = colors[kObject.color][0]
#             displayProp.Parameters("wirecolorg").Value = colors[kObject.color][1]
#             displayProp.Parameters("wirecolorb").Value = colors[kObject.color][2]

#         return True


#     # =====================
#     # Attribute Operations
#     # =====================
#     def _buildAttributes(self, kObject):
#         """Builds the attributes on the object3D. Implement in sub-classes."""

#         attrTypeMap = {
#                         "bool": constants.siBool,
#                         "string": constants.siString,
#                         "integer": constants.siInt4,
#                         "float": constants.siFloat,
#                       }

#         for eachGroup in kObject.attributes.keys():

#             if len(kObject.attributes[eachGroup].keys()) < 1:
#                 continue

#             if eachGroup == "default":
#                 propGroup = kObject.object3D.AddProperty("CustomParameterSet", False, kObject.name + "_setttings")
#             else:
#                 propGroup = kObject.object3D.AddProperty("CustomParameterSet", False, eachGroup)

#             attributes = kObject.attributes[eachGroup]
#             for eachAttribute in attributes.keys():
#                 attribute = attributes[eachAttribute]

#                 minValue = ""
#                 maxValue = ""

#                 if hasattr(attribute, "min"):
#                     minValue = attribute.min

#                 if hasattr(attribute, "max"):
#                     maxValue = attribute.max

#                 attribute = attributes[eachAttribute]
#                 newAttribute = propGroup.AddParameter3(attribute.name, attrTypeMap[attribute.attrType], attribute.value, minValue, maxValue, True, False)
#                 newAttribute.Keyable = True

#         return


#     # =====================
#     # Constraint Operations
#     # =====================
#     def _buildConstraints(self, kObject):
#         """Builds the constraints on the object3D. Implement in sub-classes."""

#         constraintTypeMap = {
#                         "scale": "Scaling",
#                         "orientation": "Orientation",
#                         "position": "Position",
#                         "pose": "Pose",
#                       }

#         for eachConstraint in kObject.constraints.keys():

#             constraint = kObject.constraints[eachConstraint]
#             constrainers = getCollection()
#             for eachItem in constraint.constrainers:
#                 constrainers.Add(eachItem.object3D)

#             newConstraint = kObject.object3D.Kinematics.AddConstraint(constraintTypeMap[constraint.constraintType], constrainers, constraint.maintainOffset)


#     # =================
#     # Build operations
#     # =================
#     def _preBuild(self, kObject):
#         """Pre-build operations.

#         Return:
#         True if successful.

#         """

#         self._checkParent(kObject)

#         return


#     def _build(self, kObject):
#         """Builds element definition.

#         Implement in sub-classes.

#         Return:
#         definition of the element.

#         """

#         if kObject.__kType__ == "Null":
#             kObject.object3D = kObject.parent.object3D.AddNull(kObject.name)

#         return True


#     def build(self, kObject):
#         """Method sequence to build the element's desription.

#         Return:
#         self.definition

#         """

#         self._preBuild(kObject)
#         # self._build(kObject)
#         if kObject.__kType__ == "Null":
#             kObject.object3D = kObject.parent.object3D.AddNull(kObject.name)

#         self._postBuild(kObject)

#         return


#     def _postBuild(self, kObject):
#         """Post-build operations.

#         Return:
#         True if successful.

#         """

#         self._initTransform(kObject)
#         self._setObjName(kObject)
#         self._setVisibility(kObject)
#         self._setDisplay(kObject)
#         self._buildAttributes(kObject)
#         self._buildConstraints(kObject)

#         for eachChild in kObject.children:
#             self.build(kObject.children[eachChild])
#             # self.cls.children[eachChild].build()

#         return


#     def create(self):
#         self.build(self.kObject)
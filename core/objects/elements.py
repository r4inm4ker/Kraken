"""Kraken - objects.elements module.

Classes:
Scene -- Scene root representation.
BaseObj -- Base 3d object.
Group -- Object used to group objects together.
Null -- Basic 3d transform with basic graphical representation.
Asset -- Namespace object.

"""

import json
from collections import OrderedDict

from kraken.core.objects import attributes
from kraken.core.objects import constraints
from kraken.core.maths import vec
from kraken.core.maths import rotation
from kraken.core.maths import xfo


class SceneObject(object):
    """Scene object representation. All elements sub-class off this."""

    __kType__ = "SceneObject"

    def __init__(self, name, parent=None):
        """Initializes base scene object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(SceneObject, self).__init__()
        self.description = None
        self.name = name
        self.parent = parent
        self.layer = None
        self.children = OrderedDict()
        self._addDefaultProperties()
        self.visibility = True
        self.color = None
        self.attributes = OrderedDict()
        self.attributes["default"] = OrderedDict()
        self.xfo = xfo.Xfo()
        self.constraints = OrderedDict()

        if parent:
            parent.addChild(self)


    def __repr__(self):
        return 'Kraken %s: %s' % (self.__kType__, self.name)


    # ================
    # Init operations
    # ================
    def initFromScnObj(self, sceneObj):
        """Initializes this object from an object in the scene."""

        return


    # ====================
    # Property operations
    # ====================
    def _checkParent(self):
        """Check if parent is set, if not set to scene root.

        Implement in sub-class.

        """

        return


    def _addDefaultProperties(self):
        """Add default object properties to the object.

        Implement in sub-classes.

        Return:
        True if successful.

        """


    # =====================
    # Visibility operations
    # =====================
    def _setVisibility(self):
        """Sets object3D visibility.

        Return:
        True if successful.

        """

        return True


    # ===================
    # Display operations
    # ===================
    def _setDisplay(self):
        """Sets object3D display properties.

        Return:
        True if successful.

        """

        return True


    # =====================
    # Attribute Operations
    # =====================
    def addAttributeGroup(self, name):
        """Add attribute group to object.

        Arguments:
        name -- String, Name of the attribute.

        Return:
        New attribute group.

        """

        if name in self.attributes.keys():
            raise KeyError("Attribute group with name " + name + " already exists.")
            return False

        self.attributes[name] = OrderedDict()

        return


    def addAttribute(self, attrType, name, value, minValue=0, maxValue=1, group=None, createGroup=False):
        """Adds a new attribute to the property.

        Arguments:
        name -- String, Name of the attribute.
        attrType -- String, Type of attribute; see attribute object for types.
        value -- Variant, Initial value of the attribute.

        Return:
        New attribute object.

        """

        if group is None:
            targetGroup = "default"
        else:
            targetGroup = group

        if targetGroup not in self.attributes.keys():
            if createGroup is True:
                self.attributes[targetGroup] = OrderedDict()
            else:
                raise KeyError("'" + targetGroup + "' is not a valid attribute group!")

        if name in self.attributes[targetGroup].keys():
            raise KeyError(name + " is already a attribute in attribute group: " + targetGroup + ". On object: " + self.name)

        if attrType == "bool":
            newAttribute = attributes.BoolAttribute(name, value)
        elif attrType == "float":
            newAttribute = attributes.FloatAttribute(name, value, minValue, maxValue)
        elif attrType == "int":
            newAttribute = attributes.BoolAttribute(name, value)
        elif attrType == "string":
            newAttribute = attributes.StringAttribute(name, value)
        else:
            raise ValueError("Invalid attribute type: " + attrType)

        self.attributes[targetGroup][name] = newAttribute

        return newAttribute


    def setAttribute(self, name, value, group="default"):
        """Returns attribute object if found.

        Arguments:
        name -- String, Name of the attribute you're looking for. (Not droids)
        group -- String, Name of group that the attribute belongs to.

        Return:
        Attribute if found. Error if not.
        """

        if group not in self.attributes.keys():
            print "'" + group +"' is not a valid attribute group on " + self.name + "."
            return None

        if name not in self.attributes[group].keys():
            print "'" + name + "' is not a valid attribute in attribute group '" + group + "'."
            return None

        self.attributes[group][name]

        return self.attributes[group][name]


    def getAttribute(self, name, group="default"):
        """Returns attribute object if found.

        Arguments:
        name -- String, Name of the attribute you're looking for. (Not droids)
        group -- String, Name of group that the attribute belongs to.

        Return:
        Attribute if found. Error if not.
        """

        if group not in self.attributes.keys():
            print "'" + group +"' is not a valid attribute group on " + self.name + "."
            return None

        if name not in self.attributes[group].keys():
            print "'" + name + "' is not a valid attribute in attribute group '" + group + "'."
            return None

        return self.attributes[group][name]


    def removeAttribute(self, name, group="default"):
        """Removes attribute from property.

        Arguments:
        name -- String, name of the attribute to remove.
        group -- String, name of the group to remove the attribute from.

        Return:
        True if successful.

        """

        if group not in self.attributes.keys():
            raise KeyError("'" + group +"' is not a valid attribute group on " + self.name)

        if name not in self.attributes[group].keys():
            raise KeyError("'" + name + "' is not a valid attribute in attribute group '" + group + "'.")

        del self.attributes[group][name]


    def _buildAttributes(self):
        """Builds the attributes on the object3D. Implement in sub-classes."""

        return


    # ===============
    # Xfo operations
    # ===============
    def _initTransform(self):
        """Set the transform in DCC. Implement in sub-classes.

        Return:
        True if successful.
        """

        return True


    def setLocalXfo(self, inXfo):
        """Sets local transform on object and updates global transforms.

        Return:
        True if successful.

        """

        if not isinstance(inXfo, xfo.Xfo):
            raise TypeError("Kraken: input 'inXfo' is not a transform!")

        if self.parent is not None:
            self.xfo = self.parent.xfo.multiply(inXfo)
        else:
            self.xfo = inXfo

        return True


    def setLocalScale(self, inVec):
        """Sets local scale on object.

        Return:
        True if successful.

        """

        if not isinstance(inVec, vec.Vec3):
            raise TypeError("Kraken: input 'inVec' is not a vector!")

        localXfo = xfo.Xfo()
        localXfo.scl.set(inVec.x, inVec.y, inVec.z)

        if self.parent is not None:
            self.xfo = self.parent.xfo.multiply(localXfo)
        else:
            self.xfo = localXfo

        return True


    def setLocalRotation(self, inRot):
        """Sets local scale on object.

        Return:
        True if successful.

        """

        if not isinstance(inRot, (rotation.Euler, rotation.Quat)):
            raise TypeError("Kraken: input 'inRot' is not a Euler or Quaternion!")

        localXfo = xfo.Xfo()

        if isinstance(inRot, rotation.Quat):
            localXfo.rot.set(v=inRot.v, w=inRot.w)
        elif isinstance(inRot, rotation.Euler):
            utilQuat = rotation.Quat()
            utilQuat.setFromEuler(inRot)
            localXfo.rot.set(v=utilQuat.v, w=utilQuat.w)

        if self.parent is not None:
            self.xfo = self.parent.xfo.multiply(localXfo)
        else:
            self.xfo = localXfo

            return True


    def setLocalTranslation(self, inVec):
        """Sets local translation on object.

        Return:
        True if successful.

        """

        if not isinstance(inVec, vec.Vec3):
            raise TypeError("Kraken: input 'inVec' is not a vector!")

        localXfo = xfo.Xfo()
        localXfo.tr.set(inVec.x, inVec.y, inVec.z)

        if self.parent is not None:
            self.xfo = self.parent.xfo.multiply(localXfo)
        else:
            self.xfo = localXfo

        return True


    def setGlobalXfo(self, inXfo):
        """Sets global transform on object.

        Return:
        True if successful.

        """

        if not isinstance(inXfo, xfo.Xfo):
            raise TypeError("Kraken: input 'inXfo' is not a transform!")

        self.xfo = inXfo

        return True


    def setGlobalScale(self, inVec):
        """Sets global scale on object.

        Return:
        True if successful.

        """

        if not isinstance(inVec, vec.Vec3):
            raise TypeError("Kraken: input 'inVec' is not a vector!")

        self.xfo.scl.set(inVec.x, inVec.y, inVec.z)

        return True


    def setGlobalRotation(self, inRot):
        """Sets global scale on object.

        Return:
        True if successful.

        """

        if not isinstance(inRot, (rotation.Euler, rotation.Quat)):
            raise TypeError("Kraken: input 'inRot' is not a Euler or Quaternion!")

        if isinstance(inRot, rotation.Quat):
            self.xfo.rot.set(v=inRot.v, w=inRot.w)
        elif isinstance(inRot, rotation.Euler):
            utilQuat = rotation.Quat()
            utilQuat.setFromEuler(inRot)
            self.xfo.rot = utilQuat #.set(v=utilQuat.v, w=utilQuat.w)

        return True


    def setGlobalTranslation(self, inVec):
        """Sets global translation on object.

        Return:
        True if successful.

        """

        if not isinstance(inVec, vec.Vec3):
            raise TypeError("Kraken: input 'inVec' is not a vector!")

        self.xfo.tr.set(inVec.x, inVec.y, inVec.z)

        return True


    # =====================
    # Constraint Operations
    # =====================
    def addConstraint(self, name, constraintType, constrainers, maintainOffset=False):
        """Adds a new constraint to the property.

        Arguments:
        name -- String, Name of the constraint.
        constraintType -- String, Type of constraint; see constraint object for types.
        constrainers -- List, objects to act as constrainers.
        maintainOffset -- Boolean, to keep the offset from the constrainers or not.

        Return:
        New constraint object.

        """

        if name in self.constraints.keys():
            raise KeyError(name + " is already a constraint on object: " + self.name)

        if constraintType == "scale":
            newConstraint = constraints.ScaleConstraint(name, constraintType, constrainers)
        elif constraintType == "orientation":
            newConstraint = constraints.OrientationConstraint(name, constraintType, constrainers)
        elif constraintType == "position":
            newConstraint = constraints.PositionConstraint(name, constraintType, constrainers)
        elif constraintType == "pose":
            newConstraint = constraints.PoseConstraint(name, constraintType, constrainers)
        else:
            raise ValueError("Invalid constraint type: " + constraintType)

        self.constraints[name] = newConstraint

        return newConstraint


    def getConstraint(self, name):
        """Returns constraint object if found.

        Arguments:
        name -- String, Name of the constraint you're looking for. (Not droids)

        Return:
        Constraint if found. Error if not.

        """

        if name not in self.constraints.keys():
            print "'" + name + "' is not a valid constraint."
            return None

        return self.constraints[group][name]


    def removeConstraint(self, name):
        """Removes constraint from property.

        Arguments:
        name -- String, name of the constraint to remove.

        Return:
        True if successful.

        """

        if name not in self.constraints.keys():
            raise KeyError("'" + name + "' is not a valid constraint.")

        del self.constraints[group][name]


    def _buildConstraints(self):
        """Builds the constraints on the object3D. Implement in sub-classes."""

        return


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations.

        Return:
        True if successful.

        """

        self._checkParent()

        return


    def _build(self):
        """Builds element description.

        Implement in sub-classes.

        Return:
        Description of the element.

        """

        return True


    def build(self):
        """Method sequence to build the element's desription.

        Return:
        self.description

        """

        self._preBuild()
        self._build()
        self._postBuild()

        return self.description


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        self._initTransform()
        self._setObjName()
        self._setVisibility()
        self._setDisplay()
        self._buildAttributes()
        self._buildConstraints()

        for eachChild in self.children:
            self.children[eachChild].build()

        return


    # =================
    # Name operations
    # =================
    def buildName(self):
        """Compiles name for object3D.

        Return:
        String, name of object3D

        """

        return self.name


    def _setObjName(self):
        """Sets object3D name.

        Implement in sub-classes.

        Return:
        True if successful.

        """

        return True


    # =================
    # Child operations
    # =================
    def addChild(self, child):
        """Add child object to this object.

        Arguments:
        child -- child object of SceneObject type.

        Return:
        True if successful.

        """

        if child.name in self.children.keys():
            raise KeyError("Kraken: " + child.name + " is already a child of this object!")

        if child.parent and child.parent.name != self.name:
            child.parent.removeChild(child.name)

        self.children[child.name] = child
        child.parent = self

        if self.__kType__ == "Layer":
            child.layer = self

        return True


    def removeChild(self, childName):
        """Remove a child from this object."

        Arguments:
        childName -- Name of the object to remove.

        Return:
        True if successful.

        """

        if childName not in self.children.keys():
            raise KeyError("Kraken: " + childName + " is not a child of this object!")

        del self.children[childName]

        return True


    def findChild(self, childName, recursive=True):
        """Find a child object by name.

        Arguments:
        childName -- String, name of the object to find.
        recursive -- Boolean, whether to search recursively down the hierarchy.

        Return:
        Object if found, None otherwise.

        """

        if childName in self.children.keys():
            return self.children[childName]
        else:

            if recursive is True:

                foundChild = None
                for eachChild in self.children.keys():
                    child = self.children[eachChild]
                    foundChild = child.findChild(childName)

                    if foundChild is not None:
                        break

                return foundChild

            else:
                return None


    # =====================
    # JSON Encode / Decode
    # =====================
    def jsonEncode(self):
        """Encodes object to JSON.

        Return:
        JSON string.

        """

        d = {
                "__class__":self.__class__.__name__,
            }

        attrs = {}
        for eachItem in self.__dict__.items():

            if eachItem[0] == "object3D":
                attrs[eachItem[0]] = None

            elif eachItem[0] == "parent":
                if self.parent is not None:
                    attrs[eachItem[0]] = self.parent.name
                else:
                    attrs[eachItem[0]] = None

            elif eachItem[0] == "properties":
                attrs[eachItem[0]] = {}

                for propName, propObj in eachItem[1].iteritems():
                    if hasattr(propObj, "jsonEncode") and callable(getattr(propObj, "jsonEncode")):
                        attrs[eachItem[0]][propName] = propObj.jsonEncode()

            elif eachItem[0] == "constraints":
                attrs[eachItem[0]] = {}

                for conName, conObj in eachItem[1].iteritems():
                    if hasattr(conObj, "jsonEncode") and callable(getattr(conObj, "jsonEncode")):
                        attrs[eachItem[0]][conName] = conObj.jsonEncode()

            elif eachItem[0] == "parameters":
                attrs[eachItem[0]] = {}

                for paramName, paramObj in eachItem[1].iteritems():
                    if hasattr(paramObj, "jsonEncode") and callable(getattr(paramObj, "jsonEncode")):
                        attrs[eachItem[0]][paramName] = paramObj.jsonEncode()

            elif eachItem[0] == "groups":
                attrs[eachItem[0]] = {}

                for groupName, groupObj in eachItem[1].iteritems():
                    if hasattr(groupObj, "jsonEncode") and callable(getattr(groupObj, "jsonEncode")):
                        attrs[eachItem[0]][groupName] = groupObj.jsonEncode()

            elif eachItem[0] == "members":
                attrs[eachItem[0]] = {}

                for memberName, memberObj in eachItem[1].iteritems():
                    attrs[eachItem[0]][memberName] = eachItem[1].keys()

            elif eachItem[0] == "children":
                attrs[eachItem[0]] = {}

                for childName, childObj in eachItem[1].iteritems():
                    if hasattr(childObj, "jsonEncode") and callable(getattr(childObj, "jsonEncode")):
                        attrs[eachItem[0]][childName] = childObj.jsonEncode()

            else:
                if hasattr(eachItem[1], "jsonEncode") and callable(getattr(eachItem[1], "jsonEncode")):
                    attrs[eachItem[0]] = eachItem[1].jsonEncode()
                else:
                    attrs[eachItem[0]] = eachItem[1]

        d.update(attrs)

        return d


    def buildDef(self):
        """Builds the Rig Definition and stores to rigDef attribute.

        Return:
        Dictionary of object data.
        """

        pass


class Group(SceneObject):
    """Group / locator object."""

    __kType__ = "Group"

    def __init__(self, name, parent=None):
        """Initializes Group object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Group, self).__init__(name, parent=parent)


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Group, self)._preBuild()

        return True


    def build(self):
        """Build element's description."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.description


    def _postBuild(self):
        """Post-build operations."""

        super(Group, self)._postBuild()

        return True


class Null(SceneObject):
    """Null / locator object."""

    __kType__ = "Null"

    def __init__(self, name, parent=None):
        """Initializes Null object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Null, self).__init__(name, parent=parent)


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Null, self)._preBuild()

        return True


    def build(self):
        """Build element's description."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.description


    def _postBuild(self):
        """Post-build operations."""

        super(Null, self)._postBuild()

        return True


class Control(SceneObject):
    """Control object."""

    __kType__ = "Control"

    shapes = {
                "arrows":
                            [
                                [-0.1, -0.3, 0.0],
                                [-0.1, -0.1, 0.0],
                                [-0.3, -0.1, 0.0],
                                [-0.3, -0.2, 0.0],
                                [-0.5, 0.0, 0.0],
                                [-0.3, 0.2, 0.0],
                                [-0.3, 0.1, 0.0],
                                [-0.1, 0.1, 0.0],
                                [-0.1, 0.3, 0.0],
                                [-0.2, 0.3, 0.0],
                                [0.0, 0.5, 0.0],
                                [0.2, 0.3, 0.0],
                                [0.1, 0.3, 0.0],
                                [0.1, 0.1, 0.0],
                                [0.3, 0.1, 0.0],
                                [0.3, 0.2, 0.0],
                                [0.5, 0.0, 0.0],
                                [0.3, -0.2, 0.0],
                                [0.3, -0.1, 0.0],
                                [0.1, -0.1, 0.0],
                                [0.1, -0.3, 0.0],
                                [0.2, -0.3, 0.0],
                                [0.0, -0.5, 0.0],
                                [-0.2, -0.3, 0.0],
                                [-0.1, -0.3, 0.0]
                            ],
                "circle":
                            [
                                [-0.3512, -0.3512, 0.0],
                                [-0.4966, 0.0, 0.0],
                                [-0.3512, 0.3512, 0.0],
                                [0.0, 0.4966, -17.4068],
                                [0.3512, 0.3512, 0.0],
                                [0.4966, 0.0, 0.0],
                                [0.3512, -0.3512, 0.0],
                                [0.0, -0.4966, 0.0],
                                [-0.3512, -0.3512, 0.0]
                            ],
                "circleDouble":
                            [
                                [0.3512, -0.3512, 0.0],
                                [0.4966, 0.0, 0.0],
                                [0.3512, 0.3512, 0.0],
                                [0.0, 0.4966, 0.0],
                                [-0.3512, 0.3512, 0.0],
                                [-0.4966, 0.0, 0.0],
                                [-0.3512, -0.3512, 0.0],
                                [0.0, -0.4966, 0.0],
                                [0.3512, -0.3512, 0.0],
                                [0.3233, -0.3233, 0.0],
                                [0.4571, 0.0, 0.0],
                                [0.3233, 0.3233, 0.0],
                                [0.0, 0.4571, 0.0],
                                [-0.3233, 0.3233, 0.0],
                                [-0.4571, 0.0, 0.0],
                                [-0.3233, -0.3233, 0.0],
                                [0.0, -0.4571, 0.0],
                                [0.3233, -0.3233, 0.0]
                            ],
                "circleHalf":
                            [
                                [0.0, 0.4965, 0.0],
                                [0.3511, 0.3511, 0.0],
                                [0.4965, 0.0, 0.0],
                                [0.3511, -0.3511, 0.0],
                                [0.0, -0.4965, 0.0]
                            ],
                "cube":
                            [
                                [-0.5, 0.5, -0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, 0.5, 0.5],
                                [0.5, 0.5, -0.5],
                                [-0.5, 0.5, -0.5],
                                [-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, 0.5, 0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [0.5, 0.5, -0.5]
                            ],
                "cubeXAligned":
                            [
                                [0.0, 0.5, -0.5],
                                [0.0, 0.5, 0.5],
                                [1.0, 0.5, 0.5],
                                [1.0, 0.5, -0.5],
                                [0.0, 0.5, -0.5],
                                [0.0, -0.5, -0.5],
                                [0.0, -0.5, 0.5],
                                [1.0, -0.5, 0.5],
                                [1.0, -0.5, -0.5],
                                [0.0, -0.5, -0.5],
                                [0.0, -0.5, 0.5],
                                [0.0, 0.5, 0.5],
                                [1.0, 0.5, 0.5],
                                [1.0, -0.5, 0.5],
                                [1.0, -0.5, -0.5],
                                [1.0, 0.5, -0.5]
                            ],
                "line":
                            [
                                [0.0, 0.0, 0.0],
                                [1.0, 0.0, 0.0]
                            ],
                "pin":
                            [
                                [0.0, 0.0, 0.602],
                                [-0.1406, 0.0, 0.6603],
                                [-0.1989, 0.0, 0.8009],
                                [-0.1406, 0.0, 0.9415],
                                [0.0, 0.0, 0.9998],
                                [0.1406, 0.0, 0.9415],
                                [0.1989, 0.0, 0.8009],
                                [0.1406, 0.0, 0.6603],
                                [0.0, 0.0, 0.602],
                                [0.0, 0.0, 0.0]
                            ],
                "rotate":
                            [
                                [-0.4105, 0.3472, -0.1844],
                                [-0.5008, 0.2001, 0.0],
                                [-0.4105, 0.3472, 0.1844],
                                [-0.4105, 0.3472, 0.0965],
                                [-0.2462, 0.4636, 0.0965],
                                [0.0, 0.5212, 0.0965],
                                [0.2462, 0.4636, 0.0965],
                                [0.4105, 0.3472, 0.0965],
                                [0.4105, 0.3472, 0.1844],
                                [0.5008, 0.2001, 0.0],
                                [0.4105, 0.3472, -0.1844],
                                [0.4105, 0.3472, 0.0965],
                                [0.2462, 0.4636, 0.0965],
                                [0.0, 0.5212, 0.0965],
                                [-0.2462, 0.4636, 0.0965],
                                [-0.4105, 0.3472, 0.0965],
                                [-0.4105, 0.3472, -0.1844]
                            ],
                "sphere":
                            [
                                [0.0, 0.0, -0.498],
                                [-0.3522, 0.0, -0.3522],
                                [-0.498, 0.0, 0.0],
                                [-0.3522, 0.0, 0.3522],
                                [0.0, 0.0, 0.498],
                                [0.3522, 0.0, 0.3522],
                                [0.498, 0.0, 0.0],
                                [0.3522, 0.0, -0.3522],
                                [0.0, 0.0, -0.498],
                                [0.0, 0.3522, -0.3522],
                                [0.0, 0.498, 0.0],
                                [0.0, 0.3522, 0.3522],
                                [0.0, 0.0, 0.498],
                                [0.0, -0.3522, 0.3522],
                                [0.0, -0.498, 0.0],
                                [0.0, -0.3522, -0.3522],
                                [0.0, 0.0, -0.498],
                                [-0.3522, 0.0, -0.3522],
                                [-0.498, 0.0, 0.0],
                                [-0.3522, 0.3522, 0.0],
                                [0.0, 0.498, 0.0],
                                [0.3522, 0.3522, 0.0],
                                [0.498, 0.0, 0.0],
                                [0.3522, -0.3522, 0.0],
                                [0.0, -0.498, 0.0],
                                [-0.3522, -0.3522, 0.0],
                                [-0.498, 0.0, 0.0]
                            ],
                "square":
                            [
                                [0.5, 0.0, -0.5],
                                [0.5, 0.0, 0.5],
                                [-0.5, 0.0, 0.5],
                                [-0.5, 0.0, -0.5],
                                [0.5, 0.0, -0.5]
                            ],
                "squareXAligned":
                            [
                                [1.0, 0.0, -0.5],
                                [1.0, 0.0, 0.5],
                                [0.0, 0.0, 0.5],
                                [0.0, 0.0, -0.5],
                                [1.0, 0.0, -0.5]
                            ],
                "triangle":
                            [
                                [1.0, 0.0, 0.0],
                                [0.0, 0.0, -0.5],
                                [0.0, 0.0, 0.5],
                                [1.0, 0.0, 0.0]
                            ],
            }


    def __init__(self, name, shape, parent=None):
        """Initializes Control object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Control, self).__init__(name, parent=parent)
        self.shape = shape
        self.sclOffset = [1,1,1]
        self.rotOffset = [0,0,0]
        self.posOffset = [0,0,0]


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Control, self)._preBuild()

        return True


    def build(self):
        """Build element's description."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.description


    def _postBuild(self):
        """Post-build operations."""

        super(Control, self)._postBuild()

        return True


class Chain(SceneObject):
    """Joint Chain object."""

    __kType__ = "Chain"

    def __init__(self, name, positions, parent=None):
        """Initializes Chain object.

        Arguments:
        name -- String, Name of model object.
        positions -- List, List of [x,y,z] values of joint positions.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Chain, self).__init__(name, parent=parent)
        self.positions = positions


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Chain, self)._preBuild()

        return True


    def build(self):
        """Build element's description."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.description


    def _postBuild(self):
        """Post-build operations."""

        super(Chain, self)._postBuild()

        return True


class Joint(SceneObject):
    """Joint Joint object."""

    __kType__ = "Joint"

    def __init__(self, name, parent=None):
        """Initializes Joint object.

        Arguments:
        name -- String, Name of model object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Joint, self).__init__(name, parent=parent)


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Joint, self)._preBuild()

        return True


    def build(self):
        """Build element's description."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.description


    def _postBuild(self):
        """Post-build operations."""

        super(Joint, self)._postBuild()

        return True


class Asset(SceneObject):
    """Asset object."""

    __kType__ = "Asset"

    def __init__(self, name, parent=None):
        """Initializes Asset / namespace object.

        Arguments:
        name -- String, Name of Asset object.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(Asset, self).__init__(name, parent=parent)
        self.groups = {}


    # =================
    # Build operations
    # =================
    def _preBuild(self):
        """Pre-build operations."""

        super(Asset, self)._preBuild()

        return True


    def _build(self):
        """Builds element in Softimage

        Return:
        True if successful.

        """

        return True


    def build(self):
        """Build element's description."""

        self._preBuild()
        self._build()
        self._postBuild()

        return self.description


    def _postBuild(self):
        """Post-build operations."""

        super(Asset, self)._postBuild()

        return True
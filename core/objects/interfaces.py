import json
from collections import OrderedDict

from kraken.core.maths import vec
from kraken.core.maths import rotation
from kraken.core.maths import xfo


class BaseInterface(object):

    def __init__(self, *args):
        pass


class AttributeInterface(BaseInterface):
    """Interface adding functions for interacting with Attributes."""

    def __init__(self):
        super(AttributeInterface, self).__init__()
        self.attributes = OrderedDict()
        self.attributes["default"] = OrderedDict()

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


class BuildInterface(BaseInterface):
    """Interface for constructing the object in the 3D application."""

    def __init__(self):
        super(BuildInterface, self).__init__()

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
        """Builds element definition.

        Implement in sub-classes.

        Return:
        definition of the element.

        """

        return True


    def build(self):
        """Method sequence to build the element's desription.

        Return:
        self.definition

        """

        self._preBuild()
        self._build()
        self._postBuild()

        return


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


class ChildInterface(BaseInterface):
    """Interface for interacting with child objects."""

    def __init__(self, parent=None):
        super(ChildInterface, self).__init__()
        self.parent = parent
        self.children = OrderedDict()

        if self.parent is not None:
            self.parent.addChild(self)

    # =================
    # Parent Operations
    # =================
    def _checkParent(self):
        """Check if parent is set, if not set to scene root.

        Implement in sub-class.

        """

        return


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


class ConstraintInterface(BaseInterface):
    """Interface for interacting with an object's constraints."""

    def __init__(self):
        super(ConstraintInterface, self).__init__()
        self.constraints = OrderedDict()

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
            newConstraint = constraints.ScaleConstraint(name, constrainers)
        elif constraintType == "orientation":
            newConstraint = constraints.OrientationConstraint(name, constrainers)
        elif constraintType == "position":
            newConstraint = constraints.PositionConstraint(name, constrainers)
        elif constraintType == "pose":
            newConstraint = constraints.PoseConstraint(name, constrainers)
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


class DisplayInterface(BaseInterface):
    """Interface for interacting with Display and Visibility of the object."""

    def __init__(self):
        super(DisplayInterface, self).__init__()
        self.visibility = True
        self.color = None

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


class JSONInterface(BaseInterface):
    """Interface for generating and parsing JSON."""

    def __init__(self):
        super(JSONInterface, self).__init__()
        self.definition = {}

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

        self.build()

        self.definition["type"] = self.__kType__

        if self.parent is not None and self.parent.__kType__ != "Layer":
            self.definition["parent"] = self.parent.name

        if self.layer is not None:
            self.definition["layer"] = self.layer.name

        self.definition["attributes"] = self.attributes
        self.definition["xfo"] = {
                                  "scl":self.xfo.scl.toArray(),
                                  "rot":[self.xfo.rot.v.toArray(),self.xfo.rot.w],
                                  "tr":self.xfo.tr.toArray(),
                                  "ro":self.xfo.ro
                                 }

        return self.definition


class NameInterface(BaseInterface):
    """Interface for interacting with the object's name."""

    def __init__(self):
        super(NameInterface, self).__init__()

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


class TransformInterface(BaseInterface):
    """Interface adding functionality for interacting with an objects
    transform."""

    def __init__(self):
        super(TransformInterface, self).__init__()
        self.xfo = xfo.Xfo()

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
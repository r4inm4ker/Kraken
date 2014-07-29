"""Kraken - objects.scene_item module.

Classes:
SceneItem - Base SceneItem Object.

"""

from kraken.core.maths.xfo import Xfo
from kraken.core.objects.attributes.attribute_group import AttributeGroup


class SceneItem(object):
    """Kraken base object type for any 3D object."""

    __kType__ = "SceneItem"

    def __init__(self, name, parent=None):
        super(SceneItem, self).__init__()
        self.name = name
        self.parent = parent
        self.component = None
        self.children = []
        self.flags = {}
        self.attributeGroups = []
        self.constraints = []
        self.xfo = Xfo()
        self.color = None
        self.visibility = True
        self.shapeVisibility = True

        defaultAttrGroup = AttributeGroup("")
        self.addAttributeGroup(defaultAttrGroup)


    # =============
    # Name methods
    # =============
    def getName(self):
        """Returns the name of the object as a string.

        Return:
        String of the object's name.

        """

        return self.name


    def getFullName(self):
        """Returns the full hierarchical path to this object.

        Return:
        String, full name of the object.

        """

        if self.parent is not None:
            return self.parent.getFullName() + '.' + self.getName() 

        return self.getName()



    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """

        if self.component is not None:
            return self.component.getComponentName() + '_' + self.getName() 

        return self.getName()


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the parent of the object as an object.

        Return:
        Parent of this object.

        """

        return self.parent


    def setParent(self, parent):
        """Sets the parent attribute of this object.

        Arguments:
        parent -- Object, object that is the parent of this one.

        Return:
        True if successful.

        """

        self.parent = parent

        return True

    # ===============
    # Component Methods
    # ===============
    def getComponent(self):
        """Returns the component of the object as an object.

        Return:
        Component of this object.

        """

        return self.component


    def setComponent(self, component):
        """Sets the component attribute of this object.

        Arguments:
        component -- Object, object that is the component of this one.

        Return:
        True if successful.

        """

        self.component = component

        return True


    # ==============
    # Child Methods
    # ==============
    def checkChildIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, child index to check.

        """

        if index > len(self.children):
            raise IndexError("'" + str(index) + "' is out of the range of the 'children' array.")

        return True


    def addChild(self, child):
        """Adds a child to this object.

        Arguments:
        child -- Object, object that will be a child of this object.

        Return:
        True if successful.

        """

        if child.name in [x.name for x in self.children]:
            raise IndexError("Child with " + child.name + " already exists as a child.")

        self.children.append(child)
        child.setParent(self)

        # Assign the child the same component. 
        if self.component is not None:
            child.setComponent(self.component)

        return True


    def removeChildByIndex(self, index):
        """Removes a child from this object by index.

        Arguments:
        index -- Integer, index of child to remove.

        Return:
        True if successful.

        """

        if self.checkChildIndex(index) is not True:
            return False

        del self.children[index]

        return True


    def removeChildByName(self, name):
        """Removes a child from this object by name.

        Arguments:
        name -- String, name of child to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachChild in enumerate(self.children):
            if eachChild.getName() == name:
                removeIndex = i

        if removeIndex is None:
            raise ValueError("'" + name + "' is not a valid child of this object.")

        self.removeChildByIndex(removeIndex)

        return True


    def getNumChildren(self):
        """Returns the number of children this object has.

        Return:
        Integer, number of children of this object.

        """

        return len(self.children)


    def getChildByIndex(self, index):
        """Returns the child object at specified index.

        Arguments:
        index -- Integer, index of the child to find.

        Return:
        Child object at specified index.

        """

        if self.checkChildIndex(index) is not True:
            return False

        return self.children[index]


    def getChildByName(self, name):
        """Returns the child object with the specified name.

        Return:
        Object if found.
        None if not found.

        """

        for eachChild in self.children:
            if eachChild.getName() == name:
                return eachChild

        return None


    def getChildrenByType(self, childType):
        """Returns all children that are of the specified type.

        Arguments:
        childType -- Class, type of children to find.

        Return:
        Array of child objects of the specified type.
        None if no objects of specified type are found.

        """

        childrenOfType = []
        for eachChild in self.children:
            if type(eachChild) is childType:
                childrenOfType.append(eachChild)

        return childrenOfType


    def findChild(self, name, targetObj=None):
        """Finds a child by recursively searching the hierarhcy for a child with
        the given name.

        Arguments:
        name -- String, name of the child to find.
        targetObj -- Object, object to search under. Used for recursive searching.

        Return:
        Object, child if found.

        """

        foundChild = None

        if targetObj == None:
            targetObj = self

        # Build children
        for i in xrange(targetObj.getNumChildren()):
            child = targetObj.getChildByIndex(i)

            if child.getName() == name:
                foundChild = child
            else:
                foundChild = self.findChild(name, child)

            if foundChild is not None:
                break

        return foundChild


    def findChildrenByType(self, objectType, targetObj=None):
        """Finds a child by recursively searching the hierarhcy for a child with
        the given name.

        Arguments:
        objectType -- Class, type of children to find.
        targetObj -- Object, object to search under. Used for recursive searching.

        Return:
        List, children of the searched type if found.

        """

        childrenOfType = []

        self._findChildByType(objectType, childrenOfType)

        return childrenOfType


    def _findChildByType(self, objectType, foundArray, targetObj=None):
        """Protected find child by type method.

        Arguments:
        objectType -- Class, type of children to find.
        foundArray -- List, list of found children to append to.
        targetObj -- Object, object to search under. Used for recursive searching.

        Return:
        True if successful.

        """

        if targetObj == None:
            targetObj = self

        # Build children
        for i in xrange(targetObj.getNumChildren()):
            child = targetObj.getChildByIndex(i)

            if type(child) is objectType:
                foundArray.append(child)

            newFoundChildren = self._findChildByType(objectType, foundArray, child)

        return


    # =============
    # Flag Methods
    # =============
    def setFlag(self, name):
        """Sets the flag of the specified name.

        Return:
        True if successful.

        """

        self.flags[name] = True

        return True


    def testFlag(self, name):
        """Tests if the specified flag is set.

        Arguments:
        name -- String, name of the flag to test.

        Return:
        True if flag is set, false otherwise.

        """

        if name in self.flags:
            return True

        return False


    def clearFlag(self, name):
        """Clears the flag of the specified name.

        Arguments:
        name -- String, name of the flag to clear.

        Return:
        True if successful.

        """

        if name in self.flags:
            del self.flags[name]
            return True

        return False


    # ========================
    # Attribute Group Methods
    # ========================
    def checkAttributeGroupIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, attribute index to check.

        Return:
        True if successful.

        """

        if index > len(self.attributeGroups):
            raise IndexError("'" + str(index) + "' is out of the range of 'attributeGroups' array.")

        return True


    def addAttributeGroup(self, attributeGroup):
        """Adds an attributeGroup to this object.

        Arguments:
        attributeGroup -- Object, Attribute Group object to add to this object.

        Return:
        True if successful.

        """

        if attributeGroup.getName() in [x.getName() for x in self.attributeGroups]:
            raise IndexError("Child with " + attributeGroup.getName() + " already exists as a attributeGroup.")

        self.attributeGroups.append(attributeGroup)
        attributeGroup.setParent(self)

        return True


    def removeAttributeGroupByIndex(self, index):
        """Removes attribute at specified index.

        Arguments:
        index -- Integer, index of attribute to remove.

        Return:
        True if successful.

        """

        if self.checkAttributeGroupIndex(index) is not True:
            return False

        del self.attributeGroups[index]

        return True


    def removeAttributeGroupByName(self, name):
        """Removes the attribute with the specified name.

        Arguments:
        name -- String, name of the attribute to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachAttributeGroup in enumerate(self.attributeGroups):
            if eachAttributeGroup.getName() == name:
                removeIndex = i

        if removeIndex is None:
            return False

        self.removeAttributeGroupByIndex(removeIndex)

        return True


    def getNumAttributeGroups(self):
        """Returns the number of attributeGroups as an integer.

        Return:
        Integer of the number of attributeGroups on this object.

        """

        return len(self.attributeGroups)


    def getAttributeGroupByIndex(self, index):
        """Returns the attribute at the specified index.

        Arguments:
        index -- Integer, index of the attribute to return.

        Return:
        AttributeGroup at the specified index.
        False if not a valid index.

        """

        if self.checkAttributeGroupIndex(index) is not True:
            return False

        return self.attributeGroups[index]


    def getAttributeGroupByName(self, name):
        """Return the attribute group with the specified name.

        Arguments:
        name -- String, name of the attribute group to return.

        Return:
        Attribute with the specified name.
        None if not found.

        """

        for eachAttributeGroup in self.attributeGroups:
            if eachAttributeGroup.getName() == name:
                return eachAttributeGroup

        return None


    # ========================
    # Constraint Methods
    # ========================
    def checkConstraintIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, constraint index to check.

        Return:
        True if successful.

        """

        if index > len(self.constraints):
            raise IndexError("'" + str(index) + "' is out of the range of 'constraints' array.")

        return True


    def addConstraint(self, constraint):
        """Adds an constraint to this object.

        Arguments:
        constraint -- Object, Constraint object to add to this object.

        Return:
        True if successful.

        """

        if constraint.name in [x.name for x in self.constraints]:
            raise IndexError("Constraint with name '" + constraint.name + "'' already exists as a constraint.")

        self.constraints.append(constraint)
        constraint.setParent(self)
        constraint.setConstrainee(self)

        return True


    def removeConstraintByIndex(self, index):
        """Removes constraint at specified index.

        Arguments:
        index -- Integer, index of constraint to remove.

        Return:
        True if successful.

        """

        if self.checkConstraintIndex(index) is not True:
            return False

        del self.constraints[index]

        return True


    def removeConstraintByName(self, name):
        """Removes the constraint with the specified name.

        Arguments:
        name -- String, name of the constraint to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachConstraint in enumerate(self.constraints):
            if eachConstraint.getName() == name:
                removeIndex = i

        if removeIndex is None:
            return False

        self.removeConstraintByIndex(removeIndex)

        return True


    def getNumConstraints(self):
        """Returns the number of constraints as an integer.

        Return:
        Integer of the number of constraints on this object.

        """

        return len(self.constraints)


    def getConstraintByIndex(self, index):
        """Returns the constraint at the specified index.

        Arguments:
        index -- Integer, index of the constraint to return.

        Return:
        Constraint at the specified index.
        False if not a valid index.

        """

        if self.checkConstraintIndex(index) is not True:
            return False

        return self.constraints[index]


    def getConstraintByName(self, name):
        """Return the constraint group with the specified name.

        Arguments:
        name -- String, name of the constraint group to return.

        Return:
        Attribute with the specified name.
        None if not found.

        """

        for eachConstraint in self.constraints:
            if eachConstraint.getName() == name:
                return eachConstraint

        return None


    # ==============
    # kType Methods
    # ==============
    def getKType(self):
        """Returns the kType of this object.

        Return:
        True if successful.

        """

        return self.__kType__


    # ===================
    # Visibility Methods
    # ===================
    def getVisibility(self):
        """Returns the visibility status of the scene item.

        Return:
        Boolean, visible or not.

        """

        return self.visibility


    def setVisibility(self, value):
        """Sets the visibility of the scene object.

        Arguments:
        value -- Boolean, value of the visibility of the object.

        Return:
        True if successful.

        """

        self.visibility = value

        return True


    def getShapeVisibility(self):
        """Returns the shape visibility status of the scene item.

        Return:
        Boolean, visible or not.

        """

        return self.shapeVisibility


    def setShapeVisibility(self, value):
        """Sets the shape visibility of the scene object.

        Arguments:
        value -- Boolean, value of the visibility of the object.

        Return:
        True if successful.

        """

        self.shapeVisibility = value

        return True


    # ================
    # Display Methods
    # ================
    def setColor(self, color):
        """Sets the color of this object.

        Arguments:
        color -- String, name of the color you wish to set.

        Return:
        True if successful.

        """

        self.color = color

        return True


    def getColor(self):
        """Returns the color of the object.

        Return:
        String, color of the object.

        """

        return self.color



    # ================
    # Persistence Methods
    # ================

    def jsonEncode(self, saver):
        """Returns the data for this object encoded as a JSON hierarchy.

        Arguments:

        Return:
        A JSON structure containing the data for this SceneItem.

        """

        classHierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break;
            classHierarchy.append(cls.__name__)

        jsonData = {
            '__typeHierarchy__': classHierarchy,
            'name': self.name,
            'parent': None,
            'children': [],
            'flags': self.flags,
            'attributeGroups': [],
            'constraints': [],
            'xfo': self.xfo.jsonEncode(),
            'color': self.color,
            'visibility': self.visibility,
            'shapeVisibility': self.shapeVisibility,
        }

        if self.parent is not None:
            jsonData['parent'] = self.parent.getName()

        if self.color is not None:
            jsonData['color'] = saver.encodeValue(self.color)

        for child in self.children:
            jsonData['children'].append(child.jsonEncode(saver))

        for attrGroup in self.attributeGroups:
            jsonData['attributeGroups'].append(attrGroup.jsonEncode(saver))

        for constr in self.constraints:
            jsonData['constraints'].append(constr.jsonEncode(saver))

        return jsonData


    def jsonDecode(self, loader, jsonData):
        """Returns the color of the object.

        Return:
        True if decoding was successful

        """

        self.parent =  loader.getParentItem()
        self.flags =  jsonData['flags']
        self.xfo =  loader.decodeValue(jsonData['xfo'])
        if 'color' in jsonData and jsonData['color'] is not None:
            self.color =  loader.decodeValue(jsonData['color'])
        self.visibility =  jsonData['visibility']
        self.shapeVisibility =  jsonData['shapeVisibility']

        for child in jsonData['children']:
            self.addChild(loader.construct(child))

        for attrGroup in jsonData['attributeGroups']:
            # There is one default attribute group assigned to each scene item. 
            # Load data into the existing item instead of constructing a new one.
            if attrGroup['name'] == '':
                loader.registerItem(self.attributeGroups[0])
                self.attributeGroups[0].jsonDecode(loader, attrGroup)
            else:
                self.addAttributeGroup(loader.construct(attrGroup))

        for constr in jsonData['constraints']:
            self.addConstraint(loader.construct(constr))

        return True

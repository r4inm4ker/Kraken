


class UndoRedoManager(object):
    """An UndoManager manages the undo/redo stack for an application. 
    Usually only a single undo manager is instantiated for a given application, 
    but it is possible to instantiate multiple undomanagers, each one responsible for a separate undo stack. 

    """

    __instance = None
    
    def __init__(self):
        super(UndoRedoManager, self).__init__()
        self.__undoStack = []
        self.__redoStack = []
        self.__currentBracket = None
        self.__isUndoingOrRedoing = False
        self.__enabled = True
        
        self.__fireUpdateCallback()
    
    def enable(self):
        """Enables the UndoManager so that new brackets can be opened and commands added""" 
        self.__enabled = True
            
    def disable(self):
        """Disables the UndoManager so that no new brackets can be opened or commands added""" 
        self.__enabled = False
            
    def enabled(self):
        """Returns true if the UndoManager is enabled"""
        return self.__enabled

    def canAddCommand(self):
        """Returns True if the undo manager is in a state where a command can be added. 
        A command can only be added if the undo manager is enabled, a bracket has been opened, and the undo manager is not currently undoing or redoing commands. 
        """
        return not self.__isUndoingOrRedoing
    

    def isUndoingOrRedoing(self):
        """Returns true if the undo manager is currently undoing or redoing."""
        return self.__isUndoingOrRedoing
     

    def openBracket(self, desc):
        """Opens a new undo bracket so that subsequent updo commands are added to the new bracket.

        When a command bracket it opened, all subsequent commands are added to the
        command bracket, which will be treated as a single undo on command the stack.
        openBracket can be called multiple times creating nested brackets. For each call to openBracket, 
        closeBracket must also be called to ensure the undo manager is left in a valid state.

        :param desc: A string to describe the new bracket. This string can be used to populate undo widgets.
        """
        self.__currentBracket = CommandBracket(desc, self.__currentBracket)
        
        if not self.__currentBracket.getParentCommandBracket():
            # Append the command if it is a root command bracket.
            self.__undoStack.append(self.__currentBracket)
        self.__clearRedoStack()
            
        # print ">>>openBracket:" + desc
     
    def closeBracket(self):
        """
        Closes the currently open undo bracket, encapsulating all added commands into a single undable action. 
        If multiple levels of brackets have been opened, the parent bracked is made the current active bracket. 
        """
        assert not self.__currentBracket is None, "UndoRedoManager.closeBracket() called but bracket has not been opened"
        # print "<<<closeBracket:" + self.__currentBracket.shortDesc()

        if self.__currentBracket.getNumCommands() == 0:
            print "Warning: UndoBracket closed with no commands added:" + self.__currentBracket.shortDesc()
            if self.__currentBracket.getParentCommandBracket() is not None:
                self.__currentBracket.getParentCommandBracket().popCommand()
            else:
                self.__undoStack.pop()
            # When a bracket is closed, the parent command backet is re-instated. 
            self.__currentBracket = self.__currentBracket.getParentCommandBracket()
        else:
            self.__currentBracket.finalize()
            # When a bracket is closed, the parent command backet is re-instated. 
            self.__currentBracket = self.__currentBracket.getParentCommandBracket()
            if not self.__currentBracket:
                # Fire the update only if the root level command bracket is closed. 
                self.__fireUpdateCallback()


    def cancelBracket(self):
        """
        Cancels the currently open bracket, reverting all changes added to the bracket since openBracket was called.
        """
        assert not self.__currentBracket is None, "UndoRedoManager.cancelBracket() called but bracket has not been opened"
        #print "<<<closeBracket:" + self.__currentBracket.shortDesc()

        if self.__currentBracket.getNumCommands() > 0:
            self.closeBracket()
            self.undo()
            command = self.__redoStack.pop()
            command.destroy()
        else:
            self.__currentBracket = self.__currentBracket.getParentCommandBracket()
        self.__fireUpdateCallback()
            
        
    def bracketOpened(self):
        """Returns True if a bracket has been opened. 
        """
        return not self.__currentBracket is None
        

    def addCommand(self, command, invokeRedoOnAdd=False):
        """
        Adds a new command to the currently opened undo bracket.
        :param command: A command object which encapsulates the revertable action.
        """

        if not self.__enabled:
            if invokeRedoOnAdd:
                command.redo()
            return

        if self.__isUndoingOrRedoing:
            raise Exception("Adding command when undoing or redoing existing commands.")

        if self.__currentBracket is not None:
            self.__currentBracket.addCommand(command, invokeRedoOnAdd=invokeRedoOnAdd)
        else:
            if invokeRedoOnAdd:
                command.redo()
            if len(self.__undoStack) > 0:
                if self.__undoStack[len(self.__undoStack)-1].mergeWith(command):
                    # the command was merged with the previous, so does not need to be applied separately
                    return

            self.__undoStack.append(command)
        self.__clearRedoStack()
    

    def haveUndo(self):
        """Returns Ture if the undo stack currently contains an undoable action"""
        return len(self.__undoStack) > 0
    

    def canUndo(self):
        """Returns Ture if the undo stack currently contains an undoable action"""
        return self.haveUndo()
    

    def undo(self):
        """Reverts the action at the top of the undo stack"""
        if self.haveUndo():
            self.__isUndoingOrRedoing = True
            command = self.__undoStack.pop()
            command.undo()
            self.__redoStack.append(command)
            self.__fireUpdateCallback()
            self.__isUndoingOrRedoing = False
    

    def haveRedo(self):
        """Returns Ture if the redo stack currently contains an redoable action"""
        return len(self.__redoStack) > 0
    

    def canRedo(self):
        """Returns Ture if the redo stack currently contains an redoable action"""
        return self.haveRedo()
    

    def redo(self):
        """Reapplies the action at the top of the redo stack"""
        if self.haveRedo():
            self.__isUndoingOrRedoing = True
            command = self.__redoStack.pop()
            command.redo()
            self.__undoStack.append(command)
            self.__fireUpdateCallback()
            self.__isUndoingOrRedoing = False
        

    def __clearUndoStack(self):
        for command in self.__undoStack:
            command.destroy()
        self.__undoStack = []
            

    def __clearRedoStack(self):
        for command in self.__redoStack:
            command.destroy()
        self.__redoStack = []
            

    def reset(self):
        """Resets the undo manager, clearing both the undo and redo stacks"""
        self.__clearUndoStack()
        self.__clearRedoStack()
        self.__fireUpdateCallback()
        

    def destroy(self):
        """Destroys all data in the undo manager."""
        self.reset()
        

    def __fireUpdateCallback(self):
        haveUndo = self.haveUndo()
        if haveUndo:
            undoShortDesc = self.__undoStack[-1].shortDesc()
            canUndo = True
        else:
            undoShortDesc = None
            canUndo = False
        haveRedo = self.haveRedo()
        if haveRedo:
            redoShortDesc = self.__redoStack[-1].shortDesc()
            canRedo = True
        else:
            redoShortDesc = None
            canRedo = False


    def logDebug(self):
        """Prints debug strings to help debug the state of the undo manager""" 
        print "bracketOpened:" + str(self.bracketOpened())
        print "undoStack:"
        for command in self.__undoStack:
            command.logDebug(1)
        print "redoStack:"
        for command in self.__redoStack:
            command.logDebug(1)
        print "-------------"

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = UndoRedoManager()
        return cls.__instance


class Command(object):
    """The command class encapsulats a change that is made in to data in the scene. 
        The undo command is constructed at the same time as the change is made, and is used to undo/redo changes to the scene. 
        Developers can derive custom undo commands to undo/redo complex changes to the scene in a performant manner.
        
        e.g. the following code defines a custom command that can undo a change to a python member made whne calling the 'changeValue' method.
        
        .. code-block:: python
            
            def changeValue(self, newValue):
                
                undoManager = UndoRedoManager.getCurrentUndoManager()
                if undoManager and undoManager.canAddCommand():
                    
                    class MyCommand(Command):
                        def __init__(self, owner, oldValue, newValue):
                            self._owner = owner
                            self._oldValue = oldValue
                            self._newValue = newValue
                            
                        def shortDesc(self):
                            return "My Command"
                        
                        def redo(self):
                            # update value to the new value. 
                            self._owner.value = self._newValue
                        
                        def undo(self):
                            # revert value to the old value. 
                            self._owner.value = self._oldValue
                            
                    def mergeWith(self, command):
                        # check if we can merge the new command with the previous one on the stack.
                        if isinstance(command, MyCommand) or True:
                            if command._owner == self._owner:
                                self._newValue = command._newValue
                                return True
                        return False
                    
                    undoManager.addCommand(MyCommand(owner, self.value, newValue))
                
                self.value = newValue
    """


    # @classmethod
    # def __instancecheck__(cls, inst):
    #     """Implement isinstance(inst, cls)."""
    #     print "__instancecheck__"
    #     return False# any(cls.__subclasscheck__(c) for c in { type(inst), inst.__class__})

    # def __subclasscheck__(cls, sub):
    #   """Implement issubclass(sub, cls)."""
    #   candidates = cls.__dict__.get("__subclass__", set()) | {cls}
    #   return any(c in candidates for c in sub.mro())

    def __init__(self):
        super(Command, self).__init__()

    def shortDesc(self):
        """Returns a short description of this undo command"""
        assert False, "derived class must defined shortDesc()"
        
    def fullDesc(self):
        """Returns a long description of this undo command"""
        return self.shortDesc()
        
    def undo(self):
        """Reverts the changes to the data in the scene.
        Note: this method is considered pure virtual, and must be overridded by derived Command classes. 
        """
        raise Exception("undo() function not defined on " + self.__class__.__name__)
        
    def redo(self):
        """Makes the changes to the data in the scene.
        Note: this method is considered pure virtual, and must be overridded by derived Command classes. 
        """
        raise Exception("redo() function not defined on " + self.__class__.__name__)

    def mergeWith(self, command):
        """Attempts to merge the command with the previous command in the undo stack.
        During interactive manipuation of values in the scene, many undo commands can be generated. 
        The mergeWith function attempts to merge a command with the previous command so that the new 
        command can be discarded, reducing the number of commands in the stack, and reducing the 
        number of actions that needs to be performed during undo/redo. 
        e.g. 
        During interactive maniplation of a value, only the initial and final values are of interest.
        The many changes that were made during the manipulation do not need to be stored, and the 
        generated command can be safely discarded, keeping only the first command. 
        """

        return False

    def finalize(self):
        """Called when the undo bracked is being closed. 

        This function is invoked on commands that were added to the stack. Any commands discarded due
        to being merged with previous commands have already been discarded. 
        """
        pass

    def destroy(self):
        """Prior to a Command being discarded from the stack, the destry method is called. The destroy method
        can be used to clean up any state data assocated with this command. The case where this is important, 
        is when a command references deleted Core objects that must be freed. In general, this mthod does not 
        need to be implimented by derived Command classes.
        """
        pass

    def logDebug(self, indent):
        """ Prints debug information about this command"""
        print str(" ".join([' '] * indent)) + self.shortDesc()


class CommandBracket(Command):
    """A command bracket combines multiple Commands into a single undoable command. """
    def __init__(self, desc, parentCommandBracket):
        super(CommandBracket, self).__init__()
        self.__desc = desc
        self.__parentCommandBracket = parentCommandBracket
        self.__commands = []
        
        if self.__parentCommandBracket:
            self.__parentCommandBracket.addCommand(self)
        
        
    def shortDesc(self):
        """Returns a short description of this undo command"""
        return self.__desc
    
    def getParentCommandBracket(self):
        """If the command bracket is nested under another command bracket, returns the parent brackes."""
        return self.__parentCommandBracket
        
    def getNumCommands(self):
        """Returns the number of commands stored in the command bracket"""
        return len(self.__commands)
        
    def addCommand(self, command, invokeRedoOnAdd=False):
        """Adds a new command to the command bracket

        :param command: The command to add to the command bracket
        """
        # this test fails based on the order of import of the file where the command was defined. 
        # if not isinstance(command, Command):
        #     import inspect
        #     raise Exception("Command class not derrived from 'Command':" + str(inspect.getmro(command.__class__)))

        if invokeRedoOnAdd:
            command.redo()
        if self.getNumCommands() > 0:
            if self.__commands[len(self.__commands)-1].mergeWith(command):
                # the command was merged with the previous, so does not need to be applied separately
                return
        #print "addCommand %s" % command.shortDesc()
        self.__commands.append(command)


    def finalize(self):
        """Called when the command is about to be appended to the stack

        This function is only invoked if the 'mergWith' of the previous command returned False
        This callback is used to notify the command that it can finalize itself. This enables optimizations
        where a command can do expesive operations only if it is not merged with previous commands.
        """
        for command in self.__commands:
            #print "Undo %s" % command.shortDesc()
            command.finalize()
        
    def popCommand(self):
        """Removes the last command from the command bracket"""
        if self.getNumCommands() > 0:
            self.__commands.pop()

    def redo(self):
        """Redo all commands in the command bracket"""
        for command in self.__commands:
            #print "Redo %s" % command.shortDesc()
            command.redo()
    
    def undo(self):
        """Undo all commands in the command bracket"""
        for command in reversed(self.__commands):
            # print "Undo %s" % command.shortDesc()
            command.undo()
    
    def destroy(self):
        """Destroys all commands in the command bracket"""
        for command in self.__commands:
            command.destroy()

    def logDebug(self, indent=0):
        """ Prints debug information about this command bracket"""
        print str("".join(['>'] * indent)) + self.shortDesc()
        for command in self.__commands:
            command.logDebug(indent+1)
        print str("".join(['<'] * indent))
        
    
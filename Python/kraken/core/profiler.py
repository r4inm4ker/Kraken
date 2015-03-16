"""Kraken - objects.profiler module.

Classes:
Profiler - Profiler Object.

"""
import time




class Profiler(object):
    """Kraken profiler object for debugging performance issues."""

    __instance = None

    class ProfilerItem(object):

        def __init__(self, label):
            super(Profiler.ProfilerItem, self).__init__()

            t = time.time()
            self.label = label
            self.start = t
            self.end = t
            self.children = []

        def addChild(self, item):
            self.children.append(item)

        def endProfiling(self):
            self.end = time.time()

    def __init__(self, label='Root'):
        super(Profiler, self).__init__()
        self.reset(label=label)

    def reset(self, label='Root'):
        """Resets the profiler for generating a new report

        Return:
        None

        """
        self.__roots = []
        self.__stack = []

    def push(self, label):
        """Adds a new child to the profiling tree and activates it.

        Return:
        None

        """

        item = Profiler.ProfilerItem(label)
        if len(self.__stack) == 0:
            self.__roots.append(item)
        else:
            self.__stack[-1].addChild(item)
        self.__stack.append(item)


    def pop(self):
        """Deactivates the current item in the tree and returns the profiler to the parent item

        Return:
        None

        """
        end = time.time()
        if len(self.__stack) == 0:
            raise Exception("Unable to close bracket. Pop has been called more times than push.") 
             
        self.__stack[-1].endProfiling()
        self.__stack.pop()
        
    def generateReport(self):
        """Returns a json object that encodes the data gathered during profiling.

        Return:
        the json object

        """
        if len(self.__stack) != 0:
            raise Exception("Profiler brackets not closed properly. pop must be called for every call to push. Pop needs to be called another " + str(len(self.__stack)) + " times") 
        report = {
            'tree': None
        }
        functions = {}
        def reportItem(item):
            itemReport  = {
                'label': item.label,
                'duration' : item.end - item.start
            }
            if item.label not in functions:
                functions[item.label] = itemReport['duration']
            else:
                functions[item.label] += itemReport['duration']

            for childItem in item.children:
                if 'children' not in itemReport:
                    itemReport['children'] = []
                itemReport['children'].append(reportItem(childItem))
            return itemReport

        report['tree'] = []
        for rootItem in self.__roots:
            report['tree'].append(reportItem(rootItem))
        return report

    @classmethod
    def getInstance(cls):
        """This class method returns the singleton instance for the Profiler

        Return:
        The singleton instance.

        """

        if cls.__instance is None:
            cls.__instance = Profiler()

        return cls.__instance

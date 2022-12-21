"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD - Toonkit
    Copyright (C) 2014-2017 Toonkit
    http://toonkit-studio.com/

    Toonkit Module Lite is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Toonkit Module Lite is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Toonkit Module Lite.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""
import os
import sys

from .tkOptions import Options 

__author__ = "Cyril GIBAUD - Toonkit"

DEBUG_PREFIX = "DEBUG"
WARNING_PREFIX = "WARNING"

DEFAULT_CATEGORY = "Miscellaneous"

class Tool(object):
    """
    Base class for tools, encapsulating tkOptions instance
    """

    def __init__(self, inName="newTool", inDescription="", inUsage="", inVersion="0.0.0.0", inContext=None, inDebug=False, inOptions=Options()):
        self.name = inName
        self.description = inDescription
        self.usage = inUsage
        self.version = inVersion
        self.context = inContext
        self.debug = inDebug
        self.options = inOptions

        self.arguments = []

        self.parent = None
        self.children = {}

        self.hasUI = False

        self.logDebug("initializing...")

    #####################################################
    #                 MAIN                              #
    #####################################################

    def getFullName(self):
        return "{0} v{1}".format(self.name, self.version)

    def setChildTool(self, inTool):
        self.children[type(inTool).__name__] = inTool
        inTool.parent = self

        return inTool

    def getToolsRepos(self):
        return ["tkToolOptions", "tkMayaTools"]

    def getChildTool(self, inToolName):
        if inToolName in self.children:
            return self.children[inToolName]

        mod = None

        if sys.version_info >= (2,7):
            import importlib
            for repo in self.getToolsRepos():
                try:
                    mod = importlib.import_module("{0}.{1}".format(repo, inToolName))
                    break
                except:
                    pass
        else:
            mod = __import__(inToolName)

        toolClass = getattr(mod, inToolName)

        return self.setChildTool(toolClass(inDebug=self.debug))

        #return None

    #####################################################
    #                 LOGGING                           #
    #####################################################

    def log(self, *args, **kwargs):
        inPrefix = ""
        if "inPrefix" in kwargs:
            inPrefix = kwargs["inPrefix"]

        print (((inPrefix + " ") if len(inPrefix) > 0 else "") + "{0} : {1}".format(self.name, " ".join([str(arg) for arg in args])))

    def logDebug(self, *args):
        if not self.debug and (not self.parent or not self.parent.debug):
            return

        self.log(*args, inPrefix=DEBUG_PREFIX)

    def warning(self, *args, **kwargs):
        self.log(*args, inPrefix=WARNING_PREFIX)

    #####################################################
    #                 OPTIONS                           #
    #####################################################

    def getOptionsPath(self):
        folderPath = os.path.dirname(os.path.realpath(__file__))

        return os.path.abspath(os.path.join(folderPath, os.pardir, "CorePreferences", "{0}.json".format(type(self).__name__)))

    def saveOptions(self):
        if self.options.path is None:
            self.options.path = self.getOptionsPath()

        self.logDebug("Saving options to {0}".format(self.options.path))

        return self.options.save()

    def loadOptions(self):
        if self.options.path is None:
            self.options.path = self.getOptionsPath()

        self.logDebug("Loading options from {0}".format(self.options.path))

        return self.options.load()

    def defaultOptions(self):
        for option in self.options.options:
            self.options[option.name] = option.defaultValue

    #####################################################
    #                 EXECUTION                         #
    #####################################################

    def getArguments(self, *args, **kwargs):
        defaults = [v if not k in kwargs else kwargs[k] for k, v in self.options.iteritems()]
        for i in range(len(args)):
            if len(defaults) > i:
                defaults[i] = args[i]

        return defaults

    def executeUI(self, *args):
        self.execute()

    def execute(self, *args, **kwargs):
        self.arguments = self.getArguments(*args, **kwargs)
        self.logDebug("Executing {0} ({1})".format(self.getFullName(), ",".join([str(obj) for obj in self.arguments])))



    def getExecuteCode(self, *args):
        raise NotImplementedError("Not implemented on base class !")

    def getShowUICode(self, *args):
        raise NotImplementedError("Not implemented on base class !")

    def addToShelf(self, *args):
        raise NotImplementedError("Not implemented on base class !")

    #####################################################
    #                 UI                                #
    #####################################################
    def getWindowName(self):
        return "{0}UI".format(self.name)

    def getOption(self, inName):
        return self.options.getOption(inName, inCreate=False)

    def getCategorizedOptions(self):
        categs = []
        unorderedDict = {}
        for opt in self.options.options:
            if not opt.category in categs:
                categs.append(opt.category)
                unorderedDict[opt.category] = [opt]
            else:
                unorderedDict[opt.category].append(opt)

        categs.sort(key = lambda e: e or " ")

        ordered = Options.OrderedDict()

        for categ in categs:
            ordered[categ] = unorderedDict[categ]

        return ordered


    def checkBoxValueChanged(self, inControlName, inOptionName, uiArg):
        raise NotImplementedError("Not implemented on base class !")

    def textValueChanged(self, inControlName, inOptionName, uiArg):
        raise NotImplementedError("Not implemented on base class !")

    def intValueChanged(self, inControlName, inOptionName, uiArg):
        raise NotImplementedError("Not implemented on base class !")

    def floatValueChanged(self, inControlName, inOptionName, uiArg):
        raise NotImplementedError("Not implemented on base class !")

    def setOptionItem(self, inOption):
        raise NotImplementedError("Not implemented on base class !")

    def createOptionItem(self, inOption):
        raise NotImplementedError("Not implemented on base class !")


    def saveOptionsUI(self, *args):
        self.saveOptions()

    def defaultOptionsUI(self, *args):
        self.defaultOptions()

        for option in self.options.options:
            self.setOptionItem(option)

    def buildWindow(self, inExecutable=True):
        raise NotImplementedError("Not implemented on base class !")

    def showPrefs(self, *args):
        raise NotImplementedError("Not implemented on base class !")

    def showUI(self, *args):
        raise NotImplementedError("Not implemented on base class !")
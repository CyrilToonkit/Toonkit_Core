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

__author__ = "Cyril GIBAUD - Toonkit"

import os
import re
import sys
from imp import reload

from . import tkContext as ctx
from . import tkPipeline as tkpipe
from .dbEngines.dbEngine import dbEngine

from .tkProjectObj import tkProjectObj
from .. import tkLogger, tkCore, tkFs

try: basestring
except: basestring = str


REPOSITORIES = {
    "default":{}
}

default =  {
    "name":{"default"},
    "entities":{},
}
REPOSITORIES["default"] = default

class tkProject(tkProjectObj):
    def __init__(self, inEngine=dbEngine(), inDCC=None, inName=None, inType="Project", *args, **kwargs):
        super(tkProject, self).__init__(inEngine, inType=inType, inParent=None, *args, **kwargs)

        self.name=inName
        self.pipeline = tkpipe.tkPipeline()
        self._engine = inEngine
        self.dcc = inDCC
        self.isProjectValid = True

    def __getattr__(self, inName):
        if inName in tkProjectObj.PROTECTEDMEMBERS:
            return tkProjectObj.__getattr__(self, inName)
        if "pipeline" in self.__dict__:
            if inName in self.pipeline._constants:
                return self.pipeline._constants[inName].get(self.pipeline.context)
            if inName in self.pipeline._patterns:
                return self.pipeline.getPattern(inName, inDict=self.pipeline.context)
        
        return tkProjectObj.__getattr__(self, inName)
    
    def __setattr__(self, inName, value):
        if inName in tkProjectObj.PROTECTEDMEMBERS:
            return tkProjectObj.__setattr__(self, inName, value)
        if "pipeline" in self.__dict__:
            if inName in self.pipeline._constants:
                self.pipeline._constants[inName]._value = value
                return
            elif inName in self.pipeline._patterns:
                self.pipeline._patterns[inName]._value = value
                return
        else:
            tkProjectObj.__setattr__(self,inName, value)

    @staticmethod
    def _get(inName):
        mod = None

        if sys.version_info >= (2,7):
            import importlib
            try:
                mod = importlib.import_module("Toonkit_Core.tkProjects.projects.{0}".format(inName))
            except Exception as e:
                tkLogger.warning(str(e))
                pass

        else:
            try:
                mod = __import__("Toonkit_Core.tkProjects.projects.{0}".format(inName))
            except:
                tkLogger.warning(str(e))
                pass

        if mod is None:
            return None 

        reload(mod)
        toolClass = getattr(mod, inName)

        return toolClass

    @staticmethod
    @tkCore.verbosed
    def getClass(inName, inPaths = []):
        project = None
        
        folder = os.path.dirname(os.path.realpath(__file__))
        projectsFolder = os.path.join(folder, "projects")
        
        subFiles = os.listdir(projectsFolder)

        if inName + ".py" in subFiles:
            project = tkProject._get(inName)
            tkLogger.debug("Class instanced correctly : ", str(project))
        else:
            if not isinstance(inPaths, (list, tuple)):
                inPaths = [inPaths]
            for path in inPaths:
                if os.path.isdir(path):
                    subfiles = os.listdir(path)
                    if inName + ".py" in subfiles:#Warning if getModuleFromPath is None
                        module = tkFs.getModuleFromPath(os.path.join(path, inName))
                        if module:
                            project = getattr(module, inName)

        if project is None:
            tkLogger.warning("No project given or found, default used !")
            project = tkProject._get("default")

        if project is None and len(subFiles) > 0:
            for subFile in subFiles:
                if not subFile.endswith(".py"):
                    continue

                    project = tkProject._get(subFile[:-3])

                    if not project is None:
                        break

        return project

    def indentStr(self, inStr, inIndentLevel=1, inIndentStr = " ", inIndentAmout=4):
        return (inIndentStr * inIndentAmout * inIndentLevel) + str(inStr)
    
    def help(self, inContext=None):
        lines = []
        indentLevel = 0

        lines.append(self.indentStr("Project Name : {name}".format(name = self.name), indentLevel))
        lines.append(self.indentStr("Dcc Name : {dccName}".format(dccName = self.dcc.name), indentLevel))

        lines.append(self.indentStr("Projet Patterns : ", indentLevel))
        indentLevel +=1
        for patternName, patternData in sorted(list(self.pipeline._patterns.items()), key= lambda kvPair: kvPair[0]):
            patternValue = self.pipeline.getPattern(patternName, inContext)
            lines.append(self.indentStr("{patternName} : {patternValue}".format(patternName=patternName, patternValue=tkCore.reduceStr(patternValue)), indentLevel))
            if len(patternData._overrides) > 0 and inContext == None:
                indentLevel +=1
                lines.append(self.indentStr("Overrides :", indentLevel))
                for overrides in  patternData._overrides:
                    lines.append(self.indentStr("- {0} : {1}".format(*[tkCore.reduceStr(x) for x in overrides]), indentLevel))
                indentLevel -=1
        indentLevel -=1
        lines.append(self.indentStr("Project Constants : ", indentLevel))
        indentLevel +=1
        for constantName, constantData in sorted(list(self.pipeline._constants.items()), key= lambda kvPair: kvPair[0]):
            constantValue = constantData.get(inContext)
            lines.append(self.indentStr("{constantName} : {constantValue}".format(constantName=constantName, constantValue=tkCore.reduceStr(constantValue)), indentLevel))
            if len(constantData._overrides) > 0 and inContext == None:
                indentLevel += 1
                lines.append(self.indentStr("Overrides : ", indentLevel))
                for overrides in constantData._overrides:
                    lines.append(self.indentStr("- {0} : {1}".format(*[tkCore.reduceStr(x) for x in overrides]), indentLevel))
                indentLevel -=1
        indentLevel -=1
        
        message = os.linesep.join(lines)
        print(message)

    def getEntitiesPatterns(self, inRepo="default"):
        repo = self._repositories.get(inRepo)
        assert repo is not None, "Repository '{}' does not exists !".format(inRepo)

        entities = repo.get("entities")
        assert entities is not None, "Repository '{0}' does not implement entities key !".format(inRepo)

        return entities

    def getPattern(self, inAsset, inRepo="default"):
        pattern = self.getEntitiesPatterns(inRepo=inRepo).get(inAsset)
        assert pattern is not None, "Repository '{0}' does not implement asset '{1}' !".format(inRepo, inAsset)

        return pattern

    def getDefaultKeys(self, inEntityType, inTranslate=False):
        return self._engine.getDefaultKeys(inEntityType, inTranslate=inTranslate)
    
    def resolveProperties(self):
        newItems = []
        for key, projectProp in self.pipeline._constants.items():
            if isinstance(projectProp._value, basestring) and projectProp._value.lower().startswith("path="):
                path = os.path.join(projectProp._value[5:])
                newItems.append(self.resolvePathPropertie(key, path))
            for nb, (dictKey, override) in enumerate(projectProp._overrides):
                if isinstance(override, basestring) and override.lower().startswith("path="):
                    projectProp._overrides[nb] = (dictKey, self.resolvePathPropertie(key, os.path.join(override[5:]))[1])

        for key, value in newItems:
            self.pipeline._constants[key]._value = value
        
        return self._properties
    
    @tkCore.verbosed
    def resolvePathPropertie(self, name, path):
        path = os.path.expandvars(path)
        if os.path.isfile(path):
            if path.endswith(".py"):
                data = self._resolveVarInData(path)
                return name, data
        elif os.path.isdir(path):
            files = os.listdir(path)
            datas = {}
            for file in files:
                if file.endswith(".py"):
                    data = self._resolveVarInData(path)
                    datas[".".join(file.split(".")[:-1])] = data
            if not data == {}:
                return name, datas
        return name, None

    def _resolveVarInData(self, inPath):
        try:
            with open(inPath, "r") as f:
                data = f.read()
            try:
                foundVars = re.findall("self.[A-z0-9]+", data)
                for foundVar in foundVars:
                    trueVar = eval(foundVar)
                    tkLogger.debug("FoundVraible in properties: {} => {}".format(foundVar, trueVar))
                    if isinstance(trueVar, basestring) and trueVar.startswith("path="):
                        varName, varData = self.resolvePathPropertie(foundVar.replace("self.", ""), trueVar[5:])
                        self.pipeline._constants[varName]._value = varData
                        tkLogger.debug("ResolvedValue = {}".format(eval(foundVar)))
                data = eval(data)
            except Exception as e:
                tkLogger.warning("Unable to eval data {}, can't resolve variable inside file.".format(inPath.split("\\")[-1]))
                tkLogger.warning(e)
                data = "path=" + inPath
            return data
        except Exception as e:
            tkLogger.error("Unable to read file {0} at path :\n{1}".format(inPath.split("\\")[-1], inPath))
            tkLogger.error(e)
            return None

    def getProperty(self, inPropertie, inContext=None):
        if inPropertie in self.pipeline._patterns:
            return self.pipeline.getPattern(inPropertie, inContext)
        elif inPropertie in self.pipeline._constants:
            return self.pipeline._constants[inPropertie].get(inContext)
        elif inPropertie in self._properties:
            return self._properties[inPropertie].value
        else:
            return None

    def detectContext(self, path=None, pattern=None, inUpdateContext=False, inForceResolve=False):
        context = self.pipeline.baseContext.copy()
        patternName = None
        if path == None:
            path = self.dcc.getSceneName()
        if not path is None:
            detectedContext = self.pipeline.detectContext(path, pattern, variables=context)
            pattern = detectedContext[0]
            patternName = detectedContext[1]
        elif pattern is None:
            tkLogger.error("Could not find matching pattern of this asset in the current project !")
            return None
        elif path is None:
            unresolved = ctx.getVariables(pattern, True)
            dccBasedContext = self.dcc.detect_context(inVariable=unresolved, inPattern=pattern, inContext=context)
            if dccBasedContext == context:
                tkLogger.error("Could not find matching pattern of this asset in the current project !")
                return None
            context.update(dccBasedContext)
            ctx.expandVariables(pattern, context)
        else:
            tkLogger.error("Could not find matching pattern of this asset in the current project !")
            return None

        if (patternName and ctx.match(self.pipeline.getPattern(patternName, context), path)):
            unresolved = ctx.getVariables(pattern, True)
            if not unresolved == [] or inForceResolve:
                tkLogger.info("Pattern unresolved or inForceResolve option is True !")
                dccBasedContext = self.dcc.detect_context(unresolved, pattern, context)
                context.update(dccBasedContext)
        if inUpdateContext:
            self.pipeline.context.update(context)
        return context
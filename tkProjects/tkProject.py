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
from .. import tkLogger

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
    def __init__(self, inEngine=dbEngine(), inDCC=None, inType="Project", *args, **kwargs):
        super(tkProject, self).__init__(inEngine, inType=inType, inParent=None, *args, **kwargs)

        self.name="tkProject"
        self.pipeline = tkpipe.tkPipeline()
        self._engine = inEngine
        self.dcc = inDCC

    def __getattr__(self, inName):
        if inName in tkProjectObj.PROTECTEDMEMBERS:
            return tkProjectObj.__getattr__(self, inName)
        if "pipeline" in self.__dict__:
            if inName in self.pipeline._constants:
                return self.pipeline._constants[inName].get(self.pipeline.context)
            if inName in self.pipeline._patterns:
                return self.pipeline.getPattern(inName)
        
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
            mod = __import__("Toonkit_Core.tkProjects.projects.{0}".format(inName))

        if mod is None:
            return None 

        reload(mod)
        toolClass = getattr(mod, inName)

        return toolClass

    @staticmethod
    def getClass(inName):
        project = None

        folder = os.path.dirname(os.path.realpath(__file__))
        projectsFolder = os.path.join(folder, "projects")
        
        subFiles = os.listdir(projectsFolder)

        if inName + ".py" in subFiles:
            project = tkProject._get(inName)
            tkLogger.info(project)

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
    
    def resolveProperties(self, recurtionDeph=3):
        newItems = []
        while recurtionDeph != 0:
            for key, projectProp in self.pipeline._constants.items():
                if isinstance(projectProp._value, basestring) and projectProp._value.lower().startswith("path="):
                    path = os.path.join(projectProp._value[5:])
                    newItems.append(self.resolvePathPropertie(key, path))
                for nb, (dictKey, override) in enumerate(projectProp._overrides):
                    if isinstance(override, basestring) and override.lower().startswith("path="):
                        projectProp._overrides[nb] = (dictKey, self.resolvePathPropertie(key, os.path.join(override[5:]))[1])

            for key, value in newItems:
                self.pipeline._constants[key]._value = value
            recurtionDeph -= 1
        
        return self._properties
    
    def resolvePathPropertie(self, name, path):
        if os.path.isfile(path):
            if path.endswith(".py"):
                try:
                    data = self._resolveVarInData(path)
                    return name, data
                except:
                    tkLogger.warning("Error: Unable to read file {0} at path :\n{1}".format(path.split("\\")[-1], path))
                    return  name, None
        elif os.path.isdir(path):
            files = os.listdir(path)
            datas = {}
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(path +"\\" + file, "r") as f:
                            data = self._resolveVarInData(path)
                        datas[".".join(file.split(".")[:-1])] = data
                    except:
                        tkLogger.warning("Error: Unable to read file {0} at path :\n{1}".format(file, path))
                        datas[".".join(file.split(".")[:-1])] = None
            if not data == {}:
                return name, data
            else:
                return name, None
        else:
            return name, None

    def _resolveVarInData(self, inPath):
        try:
            with open(inPath, "r") as f:
                data = f.read()
            varInStr = re.findall("self.[A-z]+", data)
            isTranslated = False
            if varInStr != []:
                for matching in varInStr:
                    value = eval(matching)
                    if isinstance(value, basestring) and value.startswith("path="):
                        isTranslated = False
                        break
                    else: isTranslated = True
                if isTranslated == True:
                    data = eval(data)
                else:
                    data = "path=" + inPath
            else:
                data = eval(data)
            return data
        except Exception as e:
            tkLogger.error("Error: Unable to read file {0} at path :\n{1}".format(inPath.split("\\")[-1], inPath))
            tkLogger.error(e)
            return None

    def getPropertie(self, inPropertie, inContext=None):
        if inPropertie in self.pipeline._patterns:
            return self.pipeline.getPattern(inPropertie, inContext)
        elif inPropertie in self.pipeline._constants:
            return self.pipeline._constants[inPropertie].get(inContext)
        elif inPropertie in self._properties:
            return self._properties[inPropertie].value
        else:
            return None

    def detectContext(self, path, pattern=None, inForceResolve=False):
        context = self.pipeline.baseContext.copy()
        detectedContext = self.pipeline.detectContext(path, pattern, variables=context)

        if detectedContext and ctx.match(self.pipeline.getPattern(detectedContext[1], context), path):
            machedPattern = detectedContext[0]
            unresolved = ctx.getVariables(machedPattern, True)
            if not unresolved == [] or inForceResolve:
                tkLogger.info("Pattern unresolved or inForceResolve option is True !")
                dccBasedContext = self.dcc.detect_context(unresolved, machedPattern, context)
                context.update(dccBasedContext)
        else:
            tkLogger.error("Could not find matching pattern of this asset in the current project !")
            return None
        return context

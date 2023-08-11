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



import Toonkit_Core.tkProjects.tkPipeline as tkpipe
reload(tkpipe)

pipe = tkpipe.tkPipeline()

pipe.addPattern("ProjectPath", r"Q:\0088_Marmottes2020\PROJECT\PROJECT",
    [({"repo":"Tsunami"}, r"P:\__PROD__\Marmottes\WORK\lesmarmottes2020"),
    ])

pipe.addPattern("Sequence", r"Seq{SeqNumber:[0-9]{2}}")

pipe.addPattern("Shot", r"Cut{CutNumber:[0-9]{3}}")

pipe.addPattern("ShotLongName", r"{Episode}.{Sequence}-{Shot}")

pipe.addPattern("ShotFile", r"{ShotLongName}_{Task}_v{Version:[0-9]{4}}.ma")

pipe.addPattern("ShotPath", r"{ProjectPath}\FILM\{ShotLongName}\{ShotFile}")

#pipe.context = {"Episode":"swimming", "SeqNumber":1, "CutNumber":10, "Task":"blocking", "Version":1}

print pipe.getPattern("ShotPath")
"""
import os
from .. import tkLogger

from . import tkContext
from .tkProjectData import tkProjectData
from . import tkContext as ctx

__author__ = "Cyril GIBAUD - Toonkit"

class tkPipeline(object):
    def __init__(self):
        super(tkPipeline, self).__init__()

        self.context = {}
        self.baseContext = None

        self._constants = {}
        self._patterns = {}

    def addConstant(self, inName, inValue, inOverrides=None):
        self._constants[inName] = tkProjectData(inName, inValue, inOverrides=inOverrides)

    def addPattern(self, inName, inValue, inOverrides=None):
        self._patterns[inName] = tkProjectData(inName, inValue, inOverrides=inOverrides)

    def getPattern(self, inName, inDict=None, inResolve=True):
        assert inName in self._patterns,"Pattern '{0}' does not exists".format(inName)

        dic = inDict.copy() if inDict is not None else {}

        rawValue = self._patterns[inName].get(dic)
        rawVariables = tkContext.getVariables(rawValue, inNamesOnly=True)
        intersections = set(rawVariables).intersection(self._patterns.keys())

        recursions = 20
        while(len(intersections) > 0):
            tkLogger.debug("{0} intersections ({1})".format(len(intersections), intersections))

            thisDict = {key:self._patterns[key].get(dic) for key in intersections}

            rawValue = tkContext.expandVariables(rawValue, thisDict)
            rawVariables = tkContext.getVariables(rawValue, inNamesOnly=True)
            intersections = set(rawVariables).intersection(self._patterns.keys())

            recursions += -1
            assert recursions > 0,"Cannot resolve pattern '{0}', maximum recursions reached ({1}) !".format(inName, rawValue)

        if inResolve:
            return tkContext.expandVariables(rawValue, dic)

        return rawValue
    
    def detectContext(self, path, pattern = None, variables={}, inUpdateContext=False):
        if variables == {}:
            if self.baseContext != None:
                variables = self.baseContext.copy()
            else:
                variables = {}

        if pattern and ctx.match(pattern, path, variables):
            return pattern, None
        elif not pattern:
            for key, value in self.getLeavesPattern().items():
                if value._value:
                    if ctx.match(value._value, path, variables):
                        toResolved = ctx.getVariables(value._value, True)
                        for var in toResolved:
                            if not var in self._patterns:
                                continue
                            elif ctx.match(self._patterns[var]._value, path, variables):
                                continue
                            elif self._patterns[var]._overrides == []:
                                continue
                            else:
                                for overrideFilters, overridePattern in self._patterns[var]._overrides:
                                    if ctx.match(overridePattern, path, variables):
                                        variables.update(overrideFilters)
                        tkLogger.info("Matching Pattern : " + value._value)
                        if inUpdateContext:
                            self.context.update(variables)
                        return value._value, key
                if not value._overrides == []:
                    for overides in value._overrides:
                        if ctx.match(overides[1], path, variables):
                            tkLogger.info("Matching Override Pattern : " + overides[1])
                            variables.update(overides[0])
                            if inUpdateContext:
                                self.context.update(variables)
                            return value._value, key
        else:
            return None
    
    def getLeavesPattern(self):
        variables = []
        for value in self._patterns.values():
            variables.extend([x[1:-1] for x in ctx.getVariables(value._value)])
        leavesPattern = {}
        for key, value in self._patterns.items():
            if not key in variables:
                leavesPattern[key] = value
        return leavesPattern
    

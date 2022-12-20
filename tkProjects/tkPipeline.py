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

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

import tkContext
from tkProjectData import tkProjectData

__author__ = "Cyril GIBAUD - Toonkit"

class tkPipeline(object):
    def __init__(self):
        super(tkPipeline, self).__init__()

        self.context = {}

        self._constants = {}
        self._patterns = {}

    def addConstant(self, inName, inValue, inOverrides=None):
        self._constants[inName] = tkProjectData(inName, inValue, inOverrides=inOverrides)

    def addPattern(self, inName, inValue, inOverrides=None):
        self._patterns[inName] = tkProjectData(inName, inValue, inOverrides=inOverrides)

    def getPattern(self, inName, inDict=None, inResolve=True):
        assert inName in self._patterns,"Pattern '{0}' does not exists".format(inName)

        dic = self.context.copy()
        if not inDict is None:
            dic.update(inDict)

        rawValue = self._patterns[inName].get(dic)
        rawVariables = tkContext.getVariables(rawValue, inNamesOnly=True)
        intersections = set(rawVariables).intersection(self._patterns.keys())

        recursions = 20
        while(len(intersections) > 0):
            LOGGER.debug("{0} intersections ({1})".format(len(intersections), intersections))

            thisDict = {key:self._patterns[key].get(dic) for key in intersections}

            rawValue = tkContext.expandVariables(rawValue, thisDict)
            rawVariables = tkContext.getVariables(rawValue, inNamesOnly=True)
            intersections = set(rawVariables).intersection(self._patterns.keys())

            recursions += -1
            assert recursions > 0,"Cannot resolve pattern '{0}', maximum recursions reached ({1}) !".format(inName, rawValue)

        if inResolve:
            return tkContext.expandVariables(rawValue, dic)

        return rawValue
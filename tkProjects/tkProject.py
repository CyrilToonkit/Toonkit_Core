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
import sys

import tkContext

def _get(inName):
    mod = None
    if sys.version_info >= (2,7):
        import importlib
        print "importlib"
        #try:
        mod = importlib.import_module("Toonkit_Core.tkProjects.projects.{0}".format(inName))
        #except Exception,e:
        #    print str(e)
        #    pass

    else:
        mod = __import__("Toonkit_Core.tkProjects.projects.{0}".format(inName))

    if mod is None:
        return None 

    toolClass = getattr(mod, inName)

    return toolClass()

def get(inName):
    project = None

    folder = os.path.dirname(os.path.realpath(__file__))
    projectsFolder = os.path.join(folder, "projects")
    
    subFiles = os.listdir(projectsFolder)

    print "subFiles",subFiles

    if inName + ".py" in subFiles:
        project = _get(inName)

    if project is None:
        project = _get("default")

    if project is None and len(subFiles) > 0:
        for subFile in subFiles:
            if not subFile.endswith(".py"):
                continue

                project = _get(subFile[:-3])

                if not project is None:
                    break

    return project

class tkProject:
	def __init__(self):
		self.name=None
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

from tkOptions import Options
from tkTool import Tool

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0"

class ToonkitCore(Tool):
    def __init__(self, inContext=None, inDebug=False):
        print "Toonkit Core {0} initializing...".format(VERSIONINFO)

        super(ToonkitCore, self).__init__(inName="ToonkitMayaCore", inDescription="Toonkit's Maya base library",
            inUsage="", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())

        if self.options["debug"]:
            self.debug = self.options["debug"]

        # OPTIONS : inName, inValue, inDescription=DEFAULT_DESC, inNiceName=None, inOptional=False, inCategory=None
        #Configuration
        self.options.addOption("project", "demo", None, "Project name", False, "Configuration")
        self.options.addOption("debug", inDebug, "Log more verbose messages", "Debug", False, "Configuration")

        if not self.options.isSaved():
            self.saveOptions()
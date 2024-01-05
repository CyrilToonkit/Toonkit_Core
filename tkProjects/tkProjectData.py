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
import six
basestring = six.string_types
from . import tkContext as ctx

__author__ = "Cyril GIBAUD - Toonkit"

class tkProjectData(object):
    def __init__(self, inName, inValue, inOverrides=None):
        super(tkProjectData, self).__init__()

        self.name = inName

        self._value = inValue
        self._overrides = inOverrides or []

    def get(self, inDict=None):
        if not inDict is None and len(inDict) > 0:
            for overrideDict, overrideValue in reversed(self._overrides):
                matches = True
                for key, value in overrideDict.items():
                    if not key in inDict or inDict[key] != value:
                        matches = False
                        break
                if matches:
                    return ctx.expandAllVariables(overrideValue, inDict)

        return ctx.expandAllVariables(self._value, inDict or {})
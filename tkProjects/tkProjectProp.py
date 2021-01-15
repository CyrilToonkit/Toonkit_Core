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

from datetime import datetime, timedelta

class tkProjectProp(object):
    LIFETIME = 10000#in milliseconds

    def __init__(self, inName, inValue=(), inImmortal=False):
        self.name  =inName
        self._value=inValue
        self._obsolete = inValue is tuple
        self._date = datetime.now()
        self.immortal = inImmortal

        self._modified = False

    @property
    def obsolete(self):
        return not self.immortal and ( self._obsolete or (self._date + timedelta(milliseconds=tkProjectProp.LIFETIME)) < datetime.now())

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, inValue):
        self._value=inValue
        self._date = datetime.now()
        self._modified = True
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
import logging
from .. import tkLogger
from imp import reload
from functools import partial
from . import tkContext
from .dbEngines.dbEngine import dbEngine
from .tkProjectProp import tkProjectProp
from .. import tkCore as tc

try:basestring
except:basestring=str


class tkProjectObj(object):
    PROTECTEDMEMBERS = [
        "name",
        "type",
        "parent",
        "engine",
        "pipeline",
        ]

    def __init__(self, inEngine=dbEngine(), inType=None, inParent=None, *args, **kwargs):
        self._properties = {}
        self.engine = inEngine


        self.type = inType
        self.parent = inParent

        for key, value in kwargs.items():
            translatedKey = self.engine.untranslate(key, self.type)

            self._properties[translatedKey] = tkProjectProp(translatedKey, value, inImmortal=translatedKey.endswith("id"))

            if translatedKey == "name":
                self.name=value

    def __getitem__(self, value):
        if value in self._properties.keys():
            return self._properties[value].value
        else:
            raise KeyError (str(value))
            
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__["name"]

        tkLogger.debug("__getattr__ {0} ({1})".format(name, self))

        multi = name.endswith("s")


        #Pure functions
        if name.startswith("Get"):
            if multi:
                name = name[:-1]

            name = name[3:]
            if multi:
                return partial(self.get, name)

            return partial(self.getOne, name)

        #Existing properties
        elif name in self._properties:
            prop = self._properties[name]

            if prop.obsolete:
                tkLogger.debug("Property {0} was obsolete, retrieve from db...".format(prop.name))
                entity = self.engine.getOne(self.type, self, inKeys=[name])
                print ("entity",entity)

                if entity is None or not name in entity._properties:
                    prop.value = None
                else:
                    prop.value = getattr(entity, name)
                    prop._modified = False

            return prop.value

        #Custom property getter
        else:
            if multi:
                return self.get(name[:-1])

            return self.getOne(name)

    def __setattr__(self, name, value):
        if name in tkProjectObj.PROTECTEDMEMBERS or name.startswith("_") or name in self.__dict__:
            self.__dict__[name] = value
            return

        tkLogger.debug("__setattr__ {0}:{1} ({2})".format(name, value, self))

        if not name in self.__dict__["_properties"]:
            self.__dict__["_properties"][name] = tkProjectProp(name, value)
        else:
            self.__dict__["_properties"][name].value = value

    def __repr__(self):
        return "{0} ({1}) - {2}".format(
            self.name, self.type,
            {key:value._value for key, value in self._properties.items() if not key in self.PROTECTEDMEMBERS}
            )

    @property
    def project(self):
        ancestor = self.parent

        if ancestor is None:
            return None

        while not ancestor.parent is None:
            ancestor = ancestor.parent

        return ancestor

    @staticmethod
    def getClass(inName):
        mod = None

        try:
            if sys.version_info >= (2,7):
                import importlib
                mod = importlib.import_module("Toonkit_Core.tkProjects.tk{0}".format(inName))
            else:
                mod = __import__("Toonkit_Core.tkProjects.tk{0}".format(inName))
        except Exception as e:
            print (str(e))

        if mod is None:
            return tkProjectObj

        reload(mod)

        return getattr(mod, "tk" + inName)

    def get(self, inEntityType, *args, **kwargs):

        if isinstance(inEntityType, (list, tuple)):
            values = []
            for val in values:
                if inEntityType in self._properties.keys():
                    values.append(self._properties[val].value)
            return values
        if inEntityType in self._properties.keys():
            return self._properties[inEntityType].value

        limit = 0

        if "inLimit" in kwargs:
            limit = kwargs["inLimit"]
            del kwargs["inLimit"]

        internalFilters = []

        filters = []
        for criterion, value in kwargs.items():
            operator = "=="
            if isinstance(value, (list, tuple)):
                if len(value) == 2 and value[0] in tc.OPERATORS:
                    operator, value = value
                elif len(value) == 3  and value[1] in tc.OPERATORS:
                    internalFilter = [criterion] + list(value)

                    if isinstance(internalFilter[3], basestring):
                        internalFilter[3] = "\""+internalFilter[3]+"\""

                    internalFilters.append(internalFilter)
                    continue

            filters.append([criterion, operator, value])

        results = self.engine.get(inEntityType, self, inFilters=filters, inKeys=list(args),
                                    inLimit=0 if len(internalFilters) > 0 else limit)

        if len(internalFilters) > 0:
            newResults = []
            for result in results:

                matches = True
                for internalFilter in internalFilters:
                    code = "result.{0}{1} {2} {3}".format(*internalFilter)
                    print ("!!! matchesFilter ",eval(code), code)
                    print ("!!! val ",eval("result.{0}{1}".format(internalFilter[0], internalFilter[1])))
                    if not eval(code):
                        matches = False
                        break

                if matches:
                    newResults.append(result)

            if limit != 0:
                if len(newResults) > limit:
                    newResults = newResults[:limit]
            results = newResults

        return results

    def getOne(self, inEntityType, *args, **kwargs):
        kwargs.update({"inLimit":1})
        results = self.get(inEntityType, *args, **kwargs)
        return results[0] if len(results) > 0 else None

    @property
    def modifiedProperties(self):
        return {name:prop for name,prop in self._properties.items() if prop._modified}

    def _updateProperties(self, inProperties):
        self._properties = inProperties
        for member in PROTECTEDMEMBERS:
            if member in self._properties:
                self.__dict__[member] = self._properties[member].value

    def push(self, inForce=False):
        result = self.engine.set(self, inForce=inForce)
        if not result is None:
            self._properties = result._properties

    def pull(self):
        entity = self.engine.getOne(self.type, self, inKeys=self._properties.keys())
        self._properties = entity._properties

    def getPath(inResolve=True, **kwargs):
        if project is None:
            return None

        return project.pipeline.getPattern(self.type + "Path", inDict=kwargs, inResolve=inResolve)

    def getPaths(**kwargs):
        if project is None:
            return []

        pattern = project.pipeline.getPattern(self.type + "Path", inDict=kwargs, inResolve=True)

        return tkContext.collectPath(pattern)
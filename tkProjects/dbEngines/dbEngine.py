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

def getReversedDict(inDict):

    reversedDict = {}

    for key, value in inDict.iteritems():
        if not value in reversedDict:
            reversedDict[value] = key

    return reversedDict

class dbEngine(object):
    COMMONKEYS = ["name", "id", "type"]

    DEFAULTKEYS = {
        "Asset":    ["status", "assetType"],
        "Shot":     ["status", "duration", "Sequence"],
        "Sequence": ["status", "Episode"],
        "Episode":  ["status"],
        "Task":     ["status", "step", "startDate", "endDate", "duration"],
        "Note":     ["status", "description"]
        }

    DEFAULTTRANSLATORS = {}

    def __init__(self, inTranslators=None, *args, **kwargs):
        self.name="dbEngine"
        self.translators=inTranslators or dbEngine.DEFAULTTRANSLATORS

        self.retries = 3
        self.delay = 3000

    #Keys translations

    def translate(self, inWord, inType="Type"):
        translated = self.translators.get(inType, {}).get(inWord, inWord)

        return translated

    def untranslate(self, inWord, inType="Type"):
        translated = getReversedDict(self.translators.get(inType, {})).get(inWord, inWord)

        return translated

    def getDefaultKeys(self, inEntityType, inTranslate=True):
        baseKeys =  dbEngine.COMMONKEYS + dbEngine.DEFAULTKEYS.get(inEntityType, [])

        if inTranslate:
            return [self.translate(key, inType=inEntityType) for key in baseKeys]

        return baseKeys

    #Actual getter

    #Please override me
    def _get(self, inEntityType, inSender, inFilters=None, inKeys=None, inOrder=None, inLimit=0):
        pass

    def get(self, inEntityType, inSender, inFilters=None, inKeys=None, inOrder=None, inLimit=0):
        results = self._get(inEntityType, inSender=inSender, inFilters=inFilters, inKeys=inKeys, inOrder=inOrder, inLimit=inLimit)
        for result in results:
            result.parent = inSender

        return results

    def getOne(self, inEntityType, inSender, inFilters=None, inKeys=None, inOrder=None):
        results = self.get(inEntityType, inSender, inFilters=inFilters, inKeys=inKeys, inOrder=inOrder, inLimit=1)
        for result in results:
            result.parent = inSender

        return results[0] if len(results) > 0 else None

    #Actual setter

    #Please override me
    def _set(self, inObject, inForce=False):
        pass

    def set(self, inObject, inForce=False):
        return self._set(inObject, inForce=inForce)
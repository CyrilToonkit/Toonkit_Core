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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                                TK CONTEXT

    Static library to resolve or collect variables from patterns on paths or simple names 

    1) Example to check if a file name match pattern and collect variables:
        
    #Start of code
    characterFile = "wf_ch_jimhall_moh.5.ma"
    pattern = ur"{projectShortName:.{2}}_{categoryName:.{2}}_{assetName:.+?}_{stepName:.{3}}.{version:\d+}.ma"

    otherVariables = {}
    print tkContext.match(pattern, characterFile, otherVariables)
    print otherVariables
    #End of code

    Outputs :
    True
    {u'assetName': 'jimhall', u'projectShortName': 'wf', u'stepName': 'moh', u'categoryName': 'ch', u'version': '5'}

    2) Example to resolve a path giving some variables (ex : {projectName}) and collecting some values on the fly using regexp (ex {projectNumber:.+}):
    
    #Start of code
    variables ={
                "projectName"         :"whitefang",
                "projectShortName"    :"wf",
                "categoryName"        :"ch"
            }

    variables["assetName"]="jimhall"

    print tkContext.resolvePath(r"\\NHAMDS\ToonKit\{projectNumber:.+}_{projectName}\Scenes\Assets\{assetName}\{projectShortName}_{categoryName}_{assetName}{fileEnd:.*}.ma", variables, inAcceptUndefinedResults=True, inVerbose=False)
    #End of code

    Outputs (if such file exists of course) :
    \\NHAMDS\ToonKit\0025_whitefang\Scenes\Assets\jimhall\wf_ch_jimhall_moh.5.ma

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import re
from .. import tkLogger
from .. import tkCore as tc

try: basestring
except: 
    import six
    basestring = six.string_types

__author__ = "Cyril GIBAUD - Toonkit"

DRIVE_SEP = u":"

SEP_VARIABLE = u":"
SEP_VARIABLE_START = u"{"
SEP_VARIABLE_END = u"}"

SEP_ALTQUANTIFIER_START = u"[["
SEP_ALTQUANTIFIER_END = u"]]"

SEP_VARIABLE_START_LENGTH = None
SEP_VARIABLE_END_LENGTH = None

RE_VARIABLES = None
RE_INTFORMAT = re.compile("\[0-9\]\{(\d)\}")

def conformPath(inPath):
    path = re.sub(r"/", r"\\", inPath)
    path = re.sub(r"(.+?)\\\\", r"\1\\", path)

    return path

def setSynTax(inVariableSep=SEP_VARIABLE, inVariableStart=SEP_VARIABLE_START, inVariableEnd=SEP_VARIABLE_END):
    global SEP_VARIABLE
    global SEP_VARIABLE_START
    global SEP_VARIABLE_END
    global SEP_VARIABLE_START_LENGTH
    global SEP_VARIABLE_END_LENGTH
    global RE_VARIABLES

    SEP_VARIABLE = inVariableSep
    SEP_VARIABLE_START = inVariableStart
    SEP_VARIABLE_END = inVariableEnd

    SEP_VARIABLE_START_LENGTH = len(SEP_VARIABLE_START)
    SEP_VARIABLE_END_LENGTH = len(SEP_VARIABLE_END)

    RE_VARIABLES = re.compile(u'('+SEP_VARIABLE_START+r'.*?[^\d]'+SEP_VARIABLE_END+u')')

setSynTax()

def isVariable(inVariableCandidate):
    found = re.findall(RE_VARIABLES, inVariableCandidate)
    return inVariableCandidate == "".join(found)

def splitReVariable(inReVariable):
    varName = None
    rePattern = None

    if SEP_VARIABLE in inReVariable:
        varSplit = inReVariable.split(SEP_VARIABLE)
        varName = varSplit[0][SEP_VARIABLE_START_LENGTH:]
        rePattern = varSplit[1][:-SEP_VARIABLE_END_LENGTH].replace(SEP_ALTQUANTIFIER_START, "{").replace(SEP_ALTQUANTIFIER_START, "}")
    else:
        varName = freeVariable(inReVariable)

    return (varName, rePattern)

def joinReVariable(inSplitReVariable):
    return inSplitReVariable[0] + SEP_VARIABLE + inSplitReVariable[1]

def freeVariable(inEnclosedVariable):
    return inEnclosedVariable[SEP_VARIABLE_START_LENGTH:-SEP_VARIABLE_END_LENGTH]

def encloseVariable(inFreeVariable):
    return SEP_VARIABLE_START + inFreeVariable + SEP_VARIABLE_END

def getVariables(inPattern, inNamesOnly=False):
    variables = re.findall(RE_VARIABLES, inPattern)
    if inNamesOnly:
        return [splitReVariable(variable)[0] for variable in variables]

    return variables

def toReg(inPattern):
    reg = inPattern
    
    managedVariables = []

    variables = getVariables(inPattern)

    for variable in variables:
        variableName, variableReg = splitReVariable(variable)
        if variableName in managedVariables:
            continue
        managedVariables.append(variableName)
        
        reg = reg.replace(variable, variableReg)
        
    return reg

def replaceVariables(inPattern, inReplace="*"):
    variables = getVariables(inPattern)

    specialChars = ["[", "]", "{", "}"]

    escapedVariables = []
    for variable in variables:
        for specialChar in specialChars:
            variable = variable.replace(specialChar, "\\" + specialChar)

        escapedVariables.append(variable)

    return re.sub("|".join(escapedVariables), inReplace, inPattern)

def expandVariables(inPattern, inVariables=None):
    parseAblePath = inPattern

    if inVariables == None:
        inVariables = {}

    managedVariables = []

    variables = re.findall(RE_VARIABLES, inPattern)

    for variable in variables:
        variableName, variableReg = splitReVariable(variable)
        if variableName in managedVariables:
            continue
        managedVariables.append(variableName)

        if variableName in inVariables:#Resolvable
            if variableReg != None:
                matchObj = RE_INTFORMAT.match(variableReg)
                if matchObj:
                    #TODO : Here is a brute force handling of int formatting with n zeroes in front...
                    inVariables[variableName] = int(inVariables[variableName])
                    variableName = "{0}:0{1}d".format(variableName, matchObj.groups()[0])
                    
                parseAblePath = parseAblePath.replace(variable, encloseVariable(variableName))
        else:#Not Resolvable
            safeVariable = variableName
            if variableReg != None:
                safeVariable = joinReVariable([variableName, variableReg.replace("{", "{{").replace("}", "}}")])

            parseAblePath = parseAblePath.replace(variable, "{{{0}}}".format(encloseVariable(safeVariable)))

    return parseAblePath.format(**inVariables)

def expandIterablesVariables(inIterable, inVariables={}):
    if isinstance(inIterable, (tuple, list)):
        isTuple=False
        iterable = inIterable[:]
        if isinstance(iterable, tuple):
            iterable = list(iterable)
            isTuple = True
        for nb, item in enumerate(iterable):
            if isinstance(item, basestring):
                iterable[nb] = expandVariables(item, inVariables)
            if isinstance(item, (tuple, list)):
                iterable[nb] = expandIterablesVariables(item, inVariables)
            if isinstance(item, dict):
                iterable[nb] = expandDictionaryVariables(item, inVariables)
        if isTuple:
            iterable = tuple(iterable)
    return iterable

def expandDictionaryVariables(inDict, inVariables={}):
    if isinstance(inDict, dict):
        expandDict = inDict.copy()
        for key, value in expandDict.items():
            if isinstance(value, basestring):
                expandDict[key] = expandVariables(value, inVariables)
            if isinstance(value, (tuple, list)):
                expandDict[key] = expandIterablesVariables(value, inVariables)
            if isinstance(value, dict):
                expandDict[key] = expandDictionaryVariables(value, inVariables)
    return expandDict

def expandAllVariables(inVar, inVariables={}):
    if isinstance(inVar, basestring):
        inVar = expandVariables(inVar, inVariables)
    elif isinstance(inVar, (tuple, list)):
        inVar = expandIterablesVariables(inVar, inVariables)
    elif isinstance(inVar, dict):
        inVar = expandDictionaryVariables(inVar, inVariables)
    return inVar

def regroupKnownChunks(inSplit):
    splitPathRegrouped = []
    splitGroup = []

    for split in inSplit:
        if SEP_VARIABLE_START in split:
            curItem = os.path.sep.join(splitGroup)
            if len(curItem) > 0:
                splitPathRegrouped.append(os.path.sep.join(splitGroup))
            splitPathRegrouped.append(split)
            splitGroup = []
        else:
            splitGroup.append(split)

    if len(splitGroup) > 0:
        splitPathRegrouped.append(os.path.sep.join(splitGroup))

    return splitPathRegrouped

def match(inPattern, inString, inVariables=None):
    inPattern = expandVariables(inPattern, inVariables)
    variables = re.findall(RE_VARIABLES, inPattern)

    managedVariables = []

    if len(variables) > 0:
        if inVariables == None:
            inVariables = {}

        pattern = inPattern
        for variable in variables:
            variableName, variableReg = splitReVariable(variable)

            if variableName in managedVariables:
                pattern = pattern.replace(variable, "($REGESCAPE$"+ str(managedVariables.index(variableName) + 1)+"{1})", 1)
            else:

                if variableReg == None:
                    variableReg = ".+"
                else:
                    searchIndex = re.search("<(.+)>", variableReg)
                    #Search if we have a custom sorting directive (index)
                    if searchIndex:
                        index=searchIndex.groups()[0]
                        variableReg = variableReg.replace("<"+index+">", "")

                if "\\" in variableReg:
                    tkLogger.warning ("Please don't use escaped characters in variables regular expressions !")

                pattern = pattern.replace(variable, "("+variableReg+")", 1)
                managedVariables.append(variableName)

        curReg = re.compile(pattern.replace('\\', r'\\').replace('$REGESCAPE$', '\\'), re.IGNORECASE)
        tkLogger.debug("expression : {0}, path: {1}".format(pattern, inString))
        matchObj = re.search(curReg, inString)

        if not matchObj:
            return False

        groups = matchObj.groups()

        #fill Variables
        for i in range(len(variables)):
            variable = variables[i]
            variableName, variableReg = splitReVariable(variable)
            inVariables[variableName] = groups[i]

        return True
    else:
        tkLogger.warning("No variables found in pattern \"{0}\" !".format(inPattern))
        pattern = inPattern
    curReg = re.compile(pattern.replace('\\', r'\\'), re.IGNORECASE)

    return not re.search(curReg, inString) is None

def translate(inSourcePath, inSourcePattern, inDestinationPattern, inAcceptUndefinedResults=False, inAddVariables=None, inVariablesTranslator=None, inAllowDifferent=None, inUseDifferent=False):
    variables = {}
    matched = match(inSourcePattern, inSourcePath, variables)

    if matched:

        if not inAddVariables is None:
            inAddVariables.update(variables)
            variables.update(inAddVariables)

        if not inVariablesTranslator is None:
            addedVariables = {}
            for key, value in variables.items():
                if key in inVariablesTranslator:
                    for transKey, transFunc in inVariablesTranslator[key].items():
                        if transFunc is None:
                            addedVariables[transKey] = value
                        else:
                            addedVariables[transKey] = transFunc(value)

            addedVariables.update(variables)
            variables = addedVariables

        path = None
        if inAcceptUndefinedResults:
            path = expandVariables(inDestinationPattern, variables)
        else:
            path = resolvePath(inDestinationPattern, variables)

        if (path is None or inUseDifferent) and inAllowDifferent != None:
            variables2 = variables.copy()
            inDestinationPattern2 = inDestinationPattern

            for variableName, value in inAllowDifferent.items():
                newValue = value.get("value")
                newPattern = value.get("pattern")
                
                if variableName in variables2:
                    if not newValue is None:
                        variables2[variableName] = newValue
                    else:
                        del variables2[variableName]

                    if not newPattern is None:
                        variables = re.findall(RE_VARIABLES, inDestinationPattern2)

                        for variable in variables:
                            if variable != variableName:
                                continue
                            variableName2, variableReg2 = splitReVariable(variable)
                            oldPattern = variable
                            newPattern = joinReVariable(variable, newPattern)
                            inDestinationPattern2 = inDestinationPattern2.replace(oldPattern, newPattern)
                else:
                    variables2[variableName] = value

            result = None
            if inAcceptUndefinedResults:
                result = expandVariables(inDestinationPattern2, variables2)
            else:
                result = resolvePath(inDestinationPattern2, variables2)
            return result

        return path

    return None

def resolvePath(inPath, inVariables=None, inAcceptUndefinedResults=False, inVerbose=False, inRootExists=False):
    results = collectPath(inPath, inVariables, inMaxResults=1, inRootExists=inRootExists, inAcceptUndefinedResults=inAcceptUndefinedResults, inVerbose=inVerbose)
    if len(results) > 0:
        if not inVariables is None:
            inVariables.update(results[0][1])
        return results[0][0]

    return None

#Beware, only works with "{}" variables enclosures, because it relies on str.format()...
#todo "Create" mode ?
@tc.verbosed
def collectPath(inPath, inVariables=None, inMaxResults=0, inRootExists=False, inFiles=True, inFolders=True, inAcceptUndefinedResults=False, inVerbose=False):

    #Todo maybe we can be smart on the way we want to confirm existence of root... 
    inRootExists = False

    results = []

    parsings = 0
    checkings = 0

    if inVariables == None:
        inVariables = {}

    parseAblePath = expandVariables(inPath, inVariables)
    variables = re.findall(RE_VARIABLES, parseAblePath)

    tkLogger.debug(("parseAblePath",parseAblePath))
    tkLogger.debug(("variables", variables))

    #Need real parsing
    if len(variables) > 0:
        splitPath = parseAblePath.split(os.path.sep)
        if not len(splitPath) == 1 and len(splitPath[0]) + len(splitPath[1]) == 0:
            #Shoud be a windows network root
            del splitPath[:2]
            splitPath[0] = r"\\" + splitPath[0]

        #Manage case where os.path.sep == "\" and could be used as regexp escape characher...
        if os.path.sep == "\\":
            i = 0
            while i < len(splitPath):
                if splitPath[i].count(SEP_VARIABLE_START) > splitPath[i].count(SEP_VARIABLE_END):
                    splitPath[i] = splitPath[i] + os.path.sep + splitPath[i+1]
                    splitPath.remove(splitPath[i+1])
                i+=1

        splitPath = regroupKnownChunks(splitPath)
        pathLen = len(splitPath)

        confirmedPath = None
        if inRootExists or os.path.isdir(splitPath[0]):
            confirmedPath = splitPath[0]
            checkings+=1
        elif inVerbose:
            tkLogger.info("Path {0} does not exists !".format(splitPath[0]))

        if confirmedPath != None:
            item = splitPath[1]
            toResolvePath = os.path.join(confirmedPath, item)
            innerVariables = re.findall(RE_VARIABLES, item)
            
            if len(innerVariables) > 0:
                items = sorted(os.listdir(confirmedPath), key=lambda v: v.lower())
                parsings+=1
                pattern = item

                index = None
                indexVariable = None

                for innerVariable in innerVariables:
                    variableName, variableReg = splitReVariable(innerVariable)
                    if variableReg == None:
                        variableReg = ".+"
                    searchIndex = re.search("<(.+)>", variableReg)
                    #Search if we have a custom sorting directive (index)
                    if searchIndex:
                        index=searchIndex.groups()[0]
                        variableReg = variableReg.replace("<"+index+">", "")
                        indexVariable = variableName
                    pattern = pattern.replace(innerVariable, "("+variableReg+")")

                curReg = re.compile("^"+pattern+"$", re.IGNORECASE)
                for pathItem in items:
                    matchObj = re.search(curReg, pathItem)
                    if matchObj:
                        if not inFiles or pathLen > 2:
                            if os.path.isfile(os.path.join(confirmedPath,pathItem)):
                                continue
                        if not inFolders:
                            if os.path.isdir(os.path.join(confirmedPath,pathItem)):
                                continue

                        #Resolve Variables
                        groups = matchObj.groups()
                        for i in range(len(innerVariables)):
                            innerVariable = innerVariables[i]
                            variableName, variableReg = splitReVariable(innerVariable)
                            inVariables[variableName] = groups[i]

                        curResults = collectPath(parseAblePath, inVariables.copy(), inMaxResults, inRootExists=True, inVerbose=inVerbose)
                        lenResults = len(curResults)
                        if lenResults > 0:
                            results.extend(curResults)

                lenResults = len(results)

                if lenResults > 1 and indexVariable != None:
                    results = sorted(results, key=lambda rslt:float(rslt[1][indexVariable]))
                    return [results[int(index)]]

                if inMaxResults > 0 and lenResults >= inMaxResults:
                    filteredResults = []
                    filteredResults.extend(results[:min(inMaxResults, lenResults)])
                    return filteredResults

    else:#All variables are resolved
        if (inFiles and os.path.isfile(parseAblePath)) or (inFolders and os.path.isdir(parseAblePath)):
            checkings+=1
            results = [(parseAblePath,inVariables)]

    tkLogger.debug("! resolvePath performed {0} file checks and {1} directories parsing".format(checkings, parsings))

    return results

"""
import tkContext
import subprocess
import os


def openModFolders(inAssetName="jimhall", inProjectName="whitefang", iProjectShortName="wf"):
    process = "explorer"
    
    variables ={
                "projectName"         :inProjectName,
                "projectShortName"    :iProjectShortName,
                "assetName"           :inAssetName
            }

    paths = [
        r"\\NHAMDS\ToonKit\ToonKit\OSCAR\Projects\{projectName}\Assets\{assetName}HD\Data\mod_versions",
        r"\\NHAMDS\ToonKit\{projectNumber:.+}_{projectName}\DELIVERY\{projectShortName}\ch\{assetName}\moh",
        r"\\NHAMDS\ToonKit\{projectNumber:.+}_{projectName}\Scenes\Assets\{assetName}",
    ]
    
    for path in paths:
        resolved = tkContext.resolvePath(path, variables)
        if resolved != None and os.path.isdir(resolved):
            subprocess.Popen("{0} {1}".format(process, resolved))
        
openModFolders()



COLLECT test

#Start of code
variables ={
            "projectName"         :"whitefang",
            "projectShortName"    :"wf",
            "categoryName"        :"ch"
        }

variables["assetName"]="jimhall"

pattern = ur"\\NHAMDS\ToonKit\{projectNumber:.+}_{projectName}\Scenes\Assets\{assetName}\{projectShortName}_{categoryName}_{assetName}_{step:.{3}}.{version:[0-9]+}.ma"

import time

now = time.time()
results = tkContext.collect(pattern, variables, inVerbose=False)
print time.time() - now

print "\n".join([str(r) for r in results])

#End of code

"""
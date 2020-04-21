"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Authors : Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev
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

from subprocess import call
import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)
DEBUG = False



import os
import shutil
import tkCore as tc
import tkProjects.tkContext as tkcx

@tc.verbosed
def makedirs(inPath, inVerbose=DEBUG, inLogger=LOGGER):
    """Create directory structure is it does not exists already (can take a file path)"""

    #Manage case where a filename is given
    dirPath, filePath = os.path.split(inPath)
    if os.extsep in filePath:
        inPath = dirPath

    try:
        os.makedirs(inPath)
    except OSError:
        if not os.path.isdir(inPath):
            raise

@tc.verbosed
def copy(inInPath, inOutPath=None, inOutDir=None, inUseRobocopy=True, inVerbose=DEBUG, inLogger=LOGGER):
    """Copy file or directory"""

    assert not inOutPath is None or not inOutDir is None, "Output path and output directory cannot both be None !"

    if os.path.isfile(inInPath):
        if inOutPath is None:
            inOutPath = os.join(inOutDir, os.path.basename(filePath))
        
        #makedirs(inOutPath)
        if inUseRobocopy:
            inInFolderPath, inInFileName = os.path.split(inInPath)
            inOutFolderPath, inOutFileName = os.path.split(inOutPath)

            call(["robocopy", inInFolderPath, inOutFolderPath, inInFileName])

            if inInFileName != inOutFileName:
                notRenamedPath = os.path.join(inOutFolderPath, inInFileName)
                os.rename(notRenamedPath, inOutPath)
        else:
            shutil.copy2(inInPath, inOutPath)

        return inOutPath

    if os.path.isdir(inInPath):
        outDir = inOutPath or inOutDir
        shutil.copytree(inInPath, outDir)

        return outDir
    else:
        raise IOError("copy : File or directory '{0}' does not exists !".format(inInPath))

    return None

@tc.verbosed
def copyTranslated( inSourcePatterns, inDestinationPatterns, inFileList=None, inMove=False, inUseRobocopy=True,
                    inAddVariables=None, inVariablesTranslator=None, inAllowDifferent=None, inUseDifferent=False, inVerbose=DEBUG, inLogger=LOGGER):
    """Copy or move file(s) from a hierarchy pattern to another"""


    if not isinstance(inSourcePatterns, dict):
        inSourcePatterns = {"Unknown":inSourcePatterns}

    if not isinstance(inDestinationPatterns, dict):
        inDestinationPatterns = {"Unknown":inDestinationPatterns}

    results = []

    if inFileList is None:
        inFileList = [f[0] for f in tkcx.collectPath(inSourcePattern[0])]
    elif not isinstance(inFileList, (list, tuple)):
        inFileList = (inFileList,)

    for srcFile in inFileList:
        if not os.path.isfile(srcFile):
            LOGGER.debug("File '{}' does not exists, skip...".format(srcFile))
            continue

        matched = True

        for fileType, pattern in inSourcePatterns.iteritems():
            variables = {}

            if tkcx.match(pattern, srcFile, variables):
                matched = True

                destinations = inDestinationPatterns[fileType]

                if not isinstance(destinations, (list, tuple)):
                    destinations = (destinations, )

                for destination in destinations:

                    destPath = tkcx.translate(  srcFile, pattern, destination, inAcceptUndefinedResults=True,
                                        inAddVariables=inAddVariables, inVariablesTranslator=inVariablesTranslator, inAllowDifferent=inAllowDifferent, inUseDifferent=inUseDifferent)

                    if not destPath is None:
                        results.append(destPath)
                        if inMove and destination == destinations[-1]:

                            if inUseRobocopy and srcFile[:3] != destPath[:3]:
                                inInFolderPath, inInFileName = os.path.split(srcFile)
                                inOutFolderPath, inOutFileName = os.path.split(destPath)

                                call(["robocopy", inInFolderPath, inOutFolderPath, inInFileName])
                                os.remove(srcFile)
                            else:
                                shutil.move(srcFile, destPath)

                            LOGGER.info("copyTranslated : File '{0}' moved to '{1}'".format(srcFile, destPath))
                        else:
                            copy(srcFile, destPath, inUseRobocopy=inUseRobocopy, inVerbose=inVerbose)
                            LOGGER.info("copyTranslated : File '{0}' copied to '{1}'".format(srcFile, destPath))

                break

        if not matched:
            LOGGER.warning("File '{}' does not match any patterns !".format(srcFile))

    return results

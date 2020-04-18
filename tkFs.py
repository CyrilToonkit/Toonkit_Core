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

import logging
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
def copy(inInPath, inOutPath=None, inOutDir=None, inVerbose=DEBUG, inLogger=LOGGER):
    """Copy file or directory"""

    assert not inOutPath is None or not inOutDir is None, "Output path and output directory cannot both be None !"

    if os.path.isfile(inInPath):
        if inOutPath is None:
            inOutPath = os.join(inOutDir, os.path.basename(filePath))
        
        makedirs(inOutPath)
        shutil.copy2(inInPath, inOutPath)

    elif os.path.isdir(inInPath):
        outDir = inOutPath or inOutDir
        shutil.copytree(inInPath, outDir)
    else:
        raise IOError("copy : File or directory '{0}' does not exists !".format(inInPath))

@tc.verbosed
def copyTranslated( inSourcePattern, inDestinationPattern, inFileList=None, inMove=False,
                inAddVariables=None, inAllowDifferent=None, inUseDifferent=False, inVerbose=DEBUG, inLogger=LOGGER):
    """Copy ormove file(s) from a hierarchy pattern to another"""

    if inFileList is None:
        inFileList = [f[0] for f in tkcx.collectPath(inSourcePattern)]
    elif not isinstance(inFileList, (list, tuple)):
        inFileList = (inFileList,)

    for srcFile in inFileList:
        if not os.path.isfile(srcFile):
            LOGGER.debug("File '{}' does not exists, skip...".format(srcFile))
            continue

        destPath = tkcx.translate(  srcFile, inSourcePattern, inDestinationPattern, inAcceptUndefinedResults=True,
                                    inAddVariables=inAddVariables, inAllowDifferent=inAllowDifferent, inUseDifferent=inUseDifferent)

        if not destPath is None:
            if inMove:
                shutil.move(srcFile, destPath)
                LOGGER.info("copyTranslated : File '{0}' moved to '{1}'".format(srcFile, destPath))
            else:
                copy(srcFile, destPath, inVerbose=inVerbose)
                LOGGER.info("copyTranslated : File '{0}' copied to '{1}'".format(srcFile, destPath))



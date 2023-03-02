"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Authors : Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev, Mickael Garcia - Toonkit
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

import logging
import os

CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}

# Create the Tk logger or get if it allrady exist, then set level to NotSet
tkLogger = logging.getLogger("tkLogger")
if tkLogger.level == 0:
    tkLogger.setLevel("NOTSET")

def makedirs(inPath):
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

# Set logFile for the tkLogger. Create it if it doesn't exist, or return it.
def setLogsFiles(path):
    handlers = tkLogger.handlers
    if len(handlers) == 0:
        logForm = logging.Formatter(fmt='%(asctime)s, Level:%(levelname)s, Module:%(module)s, Func:%(funcName)s, Ligne:%(lineno)d,    %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        makedirs(path)
        fileHandler = logging.FileHandler(path)
        fileHandler.setLevel(tkLogger.level)
        fileHandler.setFormatter(logForm)
        tkLogger.addHandler(fileHandler)
    return handlers if len(handlers) !=0 else [fileHandler]

# Set log level for tkLogger and his relatade files handlers.
def setLevel(level):
    tkLogger.setLevel(level)
    if isinstance(level, int):
        tkLogger.info("Logger level set to {}".format(_levelToName[level]))
    else:
        tkLogger.info("Logger level set to {}".format(level))
    handlers = tkLogger.handlers
    if len(handlers) !=0:
        for handler in handlers:
            handler.setLevel(level)

# Remove all log file handlers of the tkLogger
def removeHandlers():
    for hdlr in tkLogger.handlers:
        tkLogger.removeHandler(hdlr)

def level():
    return _levelToName.get(tkLogger.level)


def debug(msg, *args, **kwargs):
    if tkLogger.isEnabledFor(DEBUG):
        tkLogger._log(DEBUG, msg, args, **kwargs)
def info(msg, *args, **kwargs):
    if tkLogger.isEnabledFor(INFO):
        tkLogger._log(INFO, msg, args, kwargs)
def warning(msg, *args, **kwargs):
    if tkLogger.isEnabledFor(WARNING):
        tkLogger._log(WARNING, msg, args, **kwargs)
def error(msg, *args, **kwargs):
    if tkLogger.isEnabledFor(ERROR):
        tkLogger._log(ERROR, msg, args, **kwargs)

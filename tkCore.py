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

import inspect
import logging
logging.basicConfig()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ____                _              _       
  / ___|___  _ __  ___| |_ __ _ _ __ | |_ ___ 
 | |   / _ \| '_ \/ __| __/ _` | '_ \| __/ __|
 | |__| (_) | | | \__ \ || (_| | | | | |_\__ \
  \____\___/|_| |_|___/\__\__,_|_| |_|\__|___/

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

VERBOSE_ARGNAME = "inVerbose"
LOGGER_ARGNAME = "inLogger"


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____                           _                 
 |  _ \  ___  ___ ___  _ __ __ _| |_ ___  _ __ ___ 
 | | | |/ _ \/ __/ _ \| '__/ _` | __/ _ \| '__/ __|
 | |_| |  __/ (_| (_) | | | (_| | || (_) | |  \__ \
 |____/ \___|\___\___/|_|  \__,_|\__\___/|_|  |___/
                                                   
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def verbosed(func):
    """logLevel/debug decorator"""

    def wrapper(*args, **kwargs):

        #inspect for arguments
        argspec = inspect.getargspec(func)
        defaultArguments = list(reversed(zip(reversed(argspec.args), reversed(argspec.defaults))))

        all_kwargs = kwargs.copy()
        for arg, value in defaultArguments:
            if arg not in kwargs:
                all_kwargs[arg] = value

        oldLevel = None
        if VERBOSE_ARGNAME in all_kwargs and LOGGER_ARGNAME in all_kwargs:
            #If verbosed, log function name and arguments
            oldLevel = all_kwargs[LOGGER_ARGNAME].getEffectiveLevel()
            if all_kwargs[VERBOSE_ARGNAME]:
                all_kwargs[LOGGER_ARGNAME].setLevel(logging.DEBUG)

                #Format arguments
                argsList = []
                for arg in args:
                    argsList.append("\"{}\"".format(arg) if isinstance(arg, basestring) else str(arg))
                
                for key, value in all_kwargs.iteritems():
                    if key in [VERBOSE_ARGNAME, LOGGER_ARGNAME]:
                        continue

                    argsList.append(("{0}=\"{1}\"" if isinstance(value, basestring) else "{0}={1}").format(key, value)) 

                all_kwargs[LOGGER_ARGNAME].debug("CALL {0}({1})\r\n".format(func.__name__, ",".join(argsList)))
            else:
                #Restore logLevel
                all_kwargs[LOGGER_ARGNAME].setLevel(logging.WARNING)

        #Actual function call
        rslt = func(*args, **kwargs)

        if not oldLevel is None:
            all_kwargs[LOGGER_ARGNAME].setLevel(oldLevel)

        return rslt

    return wrapper

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____  _      _   
 |  _ \(_) ___| |_ 
 | | | | |/ __| __|
 | |_| | | (__| |_ 
 |____/|_|\___|\__|
                   
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def getReversedDict(inDict):

    reversedDict = {}

    for value, key in inDict.iteritems():
        if not value in reversedDict:
            reversedDict[value] = key

    return reversedDict

def getFromDefaults(inDict, inKey, inLastDefault, *args):
    """
    Get a value from the first dictionary actually implementing the given key 

    :param inDict: The first dictionary to look into
    :type inDict: dict
    :param inKey: The key to look for
    :type inKey: object
    :param inLastDefault: The default value if key can't be found anywhere
    :type inLastDefault: object
    :param *args: a list of dictionaries to look for the key, in order
    :type *args: list(dict)
    :return: The value
    :rtype: object
    """

    if inKey in inDict:
        return inDict[inKey]

    for defaultDict in args:
        if inKey in defaultDict:
            return defaultDict[inKey]

    return inLastDefault
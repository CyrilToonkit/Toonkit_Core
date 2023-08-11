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
from qtpy.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QApplication, 
    QVBoxLayout, 
    QPlainTextEdit,
    )
from qtpy import QtGui
import tkSound
import logging
import sys
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
        tkLogger.debug("Logger level set to {}".format(_levelToName[level]))
    else:
        tkLogger.debug("Logger level set to {}".format(level))
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
        from .tkCore import reduceStr
        msg = reduceStr(msg)
        tkLogger._log(DEBUG, msg, args, **kwargs)

def info(msg, *args, **kwargs):
    if tkLogger.isEnabledFor(INFO):
        from .tkCore import reduceStr
        msg = reduceStr(msg)
        tkLogger._log(INFO, msg, args, kwargs)

def warning(msg, *args, **kwargs):
    if tkLogger.isEnabledFor(WARNING):
        from .tkCore import reduceStr
        msg = reduceStr(msg)
        tkLogger._log(WARNING, msg, args, **kwargs)

def error(msg, *args, **kwargs):
    if tkLogger.isEnabledFor(ERROR):
        from .tkCore import reduceStr
        msg = reduceStr(msg)
        tkSound.playError()
        tkLogger._log(ERROR, msg, args, **kwargs)


class CustomFormatter(logging.Formatter):
    FORMATS = {
        ERROR:   ("%(asctime)s - [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s", QtGui.QColor(220,0,0)),
        DEBUG:   ("%(asctime)s - [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s", QtGui.QColor(0,200,0)),
        INFO:    ("%(asctime)s - [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s", QtGui.QColor(0,175,175)),
        WARNING: ('%(asctime)s - [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s', QtGui.QColor(175,175,0))
    }

    def format( self, record ):
        isStyle = False
        try:
            last_fmt = self._style._fmt
            isStyle = True
        except:
            last_fmt = self._fmt
        
        opt = CustomFormatter.FORMATS.get(record.levelno)
        if opt:
            fmt, color = opt
            self._fmt  = "<font color=\"{}\">{}</font>".format(QtGui.QColor(color).name(),fmt)
            if isStyle:
                self._style._fmt = self._fmt
        res = logging.Formatter.format( self, record )
        self._fmt = last_fmt
        if isStyle:
            self._style._fmt = last_fmt
        return res


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent=None):
        super(QPlainTextEditLogger, self).__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)    

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendHtml(msg)
        scrollbar = self.widget.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class LoggerUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(LoggerUI, self).__init__(*args,**kwargs)
        self.buildUI()
        self.objectName = "LoggerUI"

    def windowIconText(self):
        return self.objectName

    def buildUI(self):
        self.setWindowTitle("Logger UI")
        self.resize(800, 480)
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)


        self.textField = QPlainTextEditLogger()
        tkLogger.addHandler(self.textField)
        self.textField.setFormatter(CustomFormatter(datefmt='%d.%m.%y %H:%M:%S'))
        layout.addWidget(self.textField.widget)
        self.menuBar().addAction("Clear logs", self.textField.widget.clear)

def loadLoggerUI():
    window = None
    if '__main__' == __name__:
        app = QApplication(sys.argv)
        window = LoggerUI()
        window.show()
        sys.exit(app.exec_())
    else:
        allWidgets = QApplication.allWidgets()
        QtWindow = None
        for widget in allWidgets:
            try:
                if widget.windowIconText() == "LoggerUI":
                    window = widget
                if widget.windowIconText() =="Maya":
                    QtWindow = widget
            except:pass
        if not QtWindow is None:
            if window is None:
                window = LoggerUI(QtWindow)
            window.close()
            window.show()
    return window
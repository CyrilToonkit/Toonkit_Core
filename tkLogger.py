import logging
import tkFs 

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

# Set logFile for the tkLogger. Create it if it doesn't exist, or return it.
def setLogsFiles(path):
    handlers = tkLogger.handlers
    if len(handlers) == 0:
        logForm = logging.Formatter(fmt='[%(asctime)s, Level:%(levelname)s, Module:%(module)s, Func:%(funcName)s, Ligne:%(lineno)d]:    %(message)s', datefmt='%H:%M:%S')
        tkFs.makedirs(path)
        fileHandler = logging.FileHandler(path)
        fileHandler.setLevel(tkLogger.level)
        fileHandler.setFormatter(logForm)
        tkLogger.addHandler(fileHandler)
    return handlers if len(handlers) !=0 else [fileHandler]

# Set log level for tkLogger and his relatade files handlers.
def setLevel(level):
    tkLogger.setLevel(level)
    handlers = tkLogger.handlers
    if len(handlers) !=0:
        for handler in handlers:
            handler.setLevel(level)

# Remove all log file handlers of the tkLogger
def removeHandlers():
    for hdlr in tkLogger.handlers:
        tkLogger.removeHandler(hdlr)

@property
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

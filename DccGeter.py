from . import tkLogger
class DccGeter():

    def detect_context(self, inVariable, inPattern, inContext = {}):
        tkLogger.error("Detect context must be overwrite, you must use specific dcc geter !")
        raise AttributeError
        
    def detect_template(self):
        tkLogger.error("Detect template must be overwrite, you must use specific dcc geter !")
        raise AttributeError

    def getSceneName(self):
        tkLogger.error("getSceneName must be overwrite, you must use specific dcc geter !")
        raise AttributeError

    def getNamespace(self):
        tkLogger.error("getNameSpace must be overwrite, you must use specific dcc geter !")
        raise AttributeError
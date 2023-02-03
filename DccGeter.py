from . import tkLogger
class DccGeter():

    def detect_context():
        tkLogger.error("Detect context must be overwrite, you must use specific dcc geter !")
        raise AttributeError
        
    def detect_template(inTemplatesSpecs, ns=""):
        tkLogger.error("Detect template must be overwrite, you must use specific dcc geter !")
        raise AttributeError

    def get_lod_var(lod_tags={}, inVariables = None):
        tkLogger.error("get_lod_var must be overwrite, you must use specific dcc geter !")
        raise AttributeError
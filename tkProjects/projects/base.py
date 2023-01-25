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
__author__ = "Mickael GARCIA - Toonkit"

from ... import tkLogger

from ..tkProject import tkProject
from ..tkPipeline import tkPipeline
from .. import tkContext as ctx
import tkMayaCore as tkc
import os

class base(tkProject):
    def __init__(self, *args, **kwargs):
        super(base, self).__init__(*args, **kwargs)
        tkLogger.info(args)

        self.modulePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
        self.name = self.getProject()
        
        self.pipeline.addPattern("IOProject", ctx.resolvePath(r"Q:\{projectNumber:[0-9]{4}}_{projectName}" , {"projectName":self.name}))

        self.pipeline.addPattern("releasePatern", r"{IOProject}\DELIVERY\{assetType}\{name:.+}\{name:.+}_{lodTag}_v{version:[0-9]{3}<-1>}.ma")
        self.pipeline.addPattern("deltaFolder", r"{IOProject}\Interne\DELTAS")
        self.pipeline.addPattern("modPath", r"{IOProject}\SOURCE\{name:.+}_v{version:[0-9]{4}<-1>}.abc") # must be overwrite        
        self.pipeline.addPattern("OSCARProject", r"Z:\ToonKit\OSCAR\Projects\{projectName}")
        self.pipeline.addPattern("assetPatern", r"{OSCARProject}\Assets\{name:.+}\AN\{name:.+}.ma")
        self.pipeline.addPattern("scriptFolder", r"{OSCARProject}\Scripts")
        self.pipeline.addPattern("template", self.modulePath + r"\templates")
        self.pipeline.addPattern("AngleListener", r'{template}\AngleListener\{templateName}.py')
        self.pipeline.addPattern("ShadowRig", r'{template}\ShadowRig\{templateName}.py')
        self.pipeline.addPattern("RotationOrder", r"{template}\RotationOrder\{templateName}.py")
        self.pipeline.addPattern("PickWalk", r"{template}\PickWalk\{templateName}.py")
        self.pipeline.addPattern("conform", r"{scriptFolder}\Conform{projectName}.py")
        self.setOverwrite([("Z:", "Q:")])
        self.pipeline.context = {"projectName": self.name, "repo":"local"}
        self.baseContextKeys = ["projectName"]
        self.pipeline.baseContext = {key:value for (key, value) in self.pipeline.context.items() if key in self.baseContextKeys}
        

        # RawPath
        self.localAssetPatern = self.pipeline.getPattern("assetPatern")
        self.scriptFolder = self.pipeline.getPattern("scriptFolder")
        self.conformPath = self.pipeline.getPattern("conform")
        self.mocapPath = r"Q:\Bank\Mocap\SkeletalModel_Biped_ToonkitHIK.ma"

        # PathProperties
        self.AngleListener = r"path={0}\templates\AngleListener\AngleListener.py".format(self.modulePath)
        self.ShadowRig = r"path={0}\templates\ShadowRig\ShadowRig.py".format(self.modulePath)
        self.RotationOrder = r"path={0}\templates\RotationOrder\RotationOrder.py".format(self.modulePath)
        self.PickWalk = r"path={0}\templates\PickWalk\PickWalk.py".format(self.modulePath)
        
        self.resolveProperies()

        # Contantes
        self.rigGrp = "rig_grp"
        self.ctrlSetName = "*_anim_set"
        self.geoSetName = "*_geo_selset"
        self.modNamespace = "MOD"
        self.hideSuffix = ["_PRO", "_PXY"]
        self.templatesSpecs = {"Biped":[("Left_Leg_ParamHolder*", 0.75), ("Right_Leg_ParamHolder*", 0.75), ("Left_Arm_ParamHolder*", 0.75), ("Right_Arm_ParamHolder*", 0.75)],
                               "Quadriped": [("Left_Foreleg_ParamHolder*", 0.75), ("Left_Foreleg_ParamHolder*", 0.75), ("Left_RearLeg_ParamHolder*", 0.75), ("Right_RearLeg_ParamHolder*", 0.75)],
                               "Bird": [("*Wing*", 1.5), ("*Feather*", 1)],# Feather is usless in my point of view
                               "Vehicule": [({"type":"tkWheel"}, 1), ("Undercarriage*", 1)],
                               "Props": [("Global_SRT", 1)]}

        self.excludeTags = [
            ".+_geocns.*",
            ".+_GeoCns.*",
            ".+_geoconst.*",
            ".+_prx.*",
            ".+_PRX.*",
            ".+_tri",
            ".+_patch",
            ".+_eyelid_target.*",
            ".+_eyelid_wrapper.*",
            ".+_geo_cns",
            ".+_ref",
            ".+_SW",
            ]
        self.dualQuatMeshs = []
        self.excludeShadowRig = [] # /!\ Must be in full lowercase /!\ #
        self.includeShadowRig = [] # /!\ Must be in full lowercase /!\ #
        self.forceInfShadowRig = []
        self.lodTags = {"LD":"lod2", "MD":"lod1", "HD":"lod0"}
        self.isShadowRig = False

    def getProject(self):
        return tkc.TOOL.options["project"]

    def setOverwrite(self, inRoots):
        for key, value in self.pipeline._patterns.items():
            for inRoot, outRoot in inRoots:
                if value._value.startswith(inRoot):
                    projData = self.pipeline._patterns[key]
                    projData._overrides.append(({"repo": "server"}, projData._value.replace(inRoot, outRoot)))
                    break
    
    def detectContext(self, path, pattern=None):
        context = self.pipeline.context.copy()
        machedPattern = self.pipeline.detectContext(path, pattern, variables=context)
        if machedPattern:
            context.update(self.getPropertie("dcc").detect_template(self.getPropertie("templatesSpecs")))
            self.lodData, self.variationData = self["dcc"].get_lod_var(self.getPropertie("lodTags"), context)
            if "AN" in machedPattern:
                self.getVersion(self.pipeline.getPattern("releasePatern"), context)
        return context

    def getVersion(self, pattern, variables):
        tmpVersion = []
        if "version" in variables.keys():
            del(variables["version"])
        if not (ctx.resolvePath(pattern, variables)is None):
            tmpVersion.append(int(variables["version"]))
            del(variables["version"])
        if len(tmpVersion) >0 :
            variables["version"] = (max(tmpVersion))
        else:
            variables["version"] = 0
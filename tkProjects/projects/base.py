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
from .. import tkContext as ctx
from ... import tkCore as tkc
import os

class base(tkProject):
    def __init__(self, *args, **kwargs):
        super(base, self).__init__(*args, **kwargs)
        tkLogger.info(args)

        self.pipeline.addConstant("modulePath", os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)))
        self.name = self.getProject()

        self.pipeline.addPattern("IOProject", ctx.resolvePath(r"Q:\{projectNumber:[0-9]{4}}_{projectName}" , {"projectName":self.name}))
        if not self.pipeline._patterns["IOProject"]._value:
            raise Exception("Unable to get valide In/Out project folder !")
        self.pipeline.addPattern("OSCARProject", r"Z:\ToonKit\OSCAR\Projects\{projectName}")

        self.pipeline.addPattern("releasePattern", r"{IOProject}\DELIVERY\{assetType}\{name:.+}\{name:.+}_{lodTag}_v{version:[0-9]{3}<-1>}.ma")
        self.pipeline.addPattern("deltaFolder", r"{IOProject}\Interne\DELTAS")
        self.pipeline.addPattern("assetAnPattern", r"{OSCARProject}\Assets\{name:.+}\AN\{name:.+}.ma")
        self.pipeline.addPattern("assetRawPattern", r"{OSCARProject}\Assets\{name:.+}\AN\{name:.+}_RAW.ma")
        self.pipeline.addPattern("assetMasterPattern", r"{OSCARProject}\Assets\{name:.+}_MASTER.ma")
        self.pipeline.addPattern("assetMasterRawPattern", r"{OSCARProject}\Assets\{name:.+}_MASTER_RAW.ma")
        self.pipeline.addPattern("assetRigPattern", r"{OSCARProject}\Assets\{name:.+}\{name:.+}.ma")
        self.pipeline.addPattern("scriptFolder", r"{OSCARProject}\Scripts")
        self.pipeline.addPattern("template", self.modulePath + r"\templates")
        self.setOverwrite([("Z:", "Q:")])
        self.pipeline.context = {"projectName": self.name, "repo":"local"}
        self.pipeline.addConstant("baseContextKeys", ["projectName"])
        self.pipeline.baseContext = {key:value for (key, value) in self.pipeline.context.items() if key in self.baseContextKeys}
        
        # RawPath
        self.pipeline.addConstant("scriptFolder", self.pipeline.getPattern("scriptFolder"))
        self.pipeline.addConstant("mocapPath", r"Q:\ToonKit\Bank\Mocap\SkeletalModel_Biped_ToonkitHIK.ma")

        # PathProperties
        self.pipeline.addConstant("AngleListener", r"path={0}\templates\AngleListener\AngleListener.py".format(self.modulePath))
        self.pipeline.addConstant("ShadowRig", r"path={0}\templates\ShadowRig\ShadowRig.py".format(self.modulePath))
        self.pipeline.addConstant("RotationOrder", r"path={0}\templates\RotationOrder\RotationOrder.py".format(self.modulePath))
        self.pipeline.addConstant("PickWalk", r"path={0}\templates\RigSpecs\PickWalk.py".format(self.modulePath))
        
        

        # Contantes
        self.pipeline.addConstant("rigGrp", "rig_grp")
        self.pipeline.addConstant("ctrlSetName", "::*anim_set")
        self.pipeline.addConstant("geoSetName", "::*geo_set")
        self.pipeline.addConstant("modNamespace", "MOD")
        self.pipeline.addConstant("hideSuffix", ["_PRO", "_PXY"])
        self.pipeline.addConstant("templatesSpecs", {"Biped":[("Left_Leg_ParamHolder*", 0.75), ("Right_Leg_ParamHolder*", 0.75), ("Left_Arm_ParamHolder*", 0.75), ("Right_Arm_ParamHolder*", 0.75)],
                               "Quadriped": [("Left_Foreleg_ParamHolder*", 0.75), ("Left_Foreleg_ParamHolder*", 0.75), ("Left_RearLeg_ParamHolder*", 0.75), ("Right_RearLeg_ParamHolder*", 0.75)],
                               "Bird": [("*Wing*", 1.5), ("*Feather*", 1)],# Feather is usless in my point of view
                               "Vehicule": [({"type":"tkWheel"}, 1), ("Undercarriage*", 1)],
                               "Props": [("Global_SRT", 1), ("GlobalSR*", 1)]})

        self.pipeline.addConstant("excludeTags", [
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
            ])
        self.pipeline.addConstant("dualQuatMeshs", ["*caruncle_layer1"])
        self.pipeline.addConstant("forceInfShadowRig", [])
        self.pipeline.addConstant("lodTags", {"LD":"lod2", "MD":"lod1", "HD":"lod0"})

        # RigingKickstarterTamplate, it's for testing purpose. 
        # To be delete befor commit !
        self.pipeline.addConstant("mocapPrefix","MayaHIK_")
        self.pipeline.addConstant("yup_zfront_preset", r"path={0}\templates\Mocap\yup_zfront_preset.py".format(self.modulePath))
        self.pipeline.addConstant("mocapDefinition", r"path={0}\templates\Mocap\mocapDefinition.py".format(self.modulePath))
        self.pipeline.addConstant("mocapBinding", r"path={0}\templates\Mocap\tamplate.py".format(self.modulePath))
        self.pipeline.addConstant("mocapOrient", r"path={0}\templates\Mocap\presets.py".format(self.modulePath))
        self.pipeline.addConstant("mocapSkeletonPath", r"Q:\Bank\Mocap\SkeletalModel_Biped_ToonkitHIK.ma".format(self.modulePath))

        self.pipeline.addConstant("shadowrigOrients", r"path={0}\templates\ShadowRig\shadowrig_orients.py".format(self.modulePath))
        self.pipeline.addConstant("shadowrigPreset", r"path={0}\templates\ShadowRig\shadowrig_preset.py".format(self.modulePath))
        self.pipeline.addConstant("shadowrigRenamings", r"path={0}\templates\ShadowRig\shadowrig_renamings.py".format(self.modulePath))
        self.pipeline.addConstant("shadowrigRotateorders", r"path={0}\templates\ShadowRig\shadowrig_rotateorders.py".format(self.modulePath))
        self.pipeline.addConstant("rigOrients", r"path={0}\templates\RigSpecs\rigOrients.py".format(self.modulePath))

        self.resolveProperties()
    def getProject(self):
        return tkc.TOOL.options["project"]

    def setOverwrite(self, inRoots):
        for key, value in self.pipeline._patterns.items():
            for inRoot, outRoot in inRoots:
                if value._value.startswith(inRoot):
                    projData = self.pipeline._patterns[key]
                    projData._overrides.append(({"repo": "server"}, projData._value.replace(inRoot, outRoot)))
                    break

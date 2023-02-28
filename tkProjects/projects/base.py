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
        self.name = kwargs["inName"] or self.getProject()
        os.environ["TK_MODULE_PATH"] = self.modulePath

        self.pipeline.addPattern("IOProject", ctx.resolvePath(r"Q:\{projectNumber:[0-9]{4}}_{projectName}" , {"projectName":self.name}))
        if not self.pipeline._patterns["IOProject"]._value:
            tkLogger.error("Unable to get valide In/Out project folder !")
            self.isProjectValid = False
            return None
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
        self.pipeline.addConstant("baseContextKeys", ["projectName", "repo"])
        self.pipeline.baseContext = {key:value for (key, value) in self.pipeline.context.items() if key in self.baseContextKeys}
        
        # RawPath
        self.pipeline.addConstant("scriptFolder", self.pipeline.getPattern("scriptFolder"))
        
        # PathProperties
        self.pipeline.addConstant("AngleListener", r"path=%tk_module_path%\templates\AngleListener\angle_listener.py")
        # self.pipeline.addConstant("ShadowRig", r"path={0}\templates\ShadowRig\shadowrig_hierarchy.py".format(self.modulePath))
        self.pipeline.addConstant("ShadowRig", None)
        self.pipeline.addConstant("RotationOrder", r"path=%tk_module_path%\templates\RigSpecs\rotation_order.py")
        self.pipeline.addConstant("PickWalk", r"path=%tk_module_path%\templates\RigSpecs\pick_walk.py")
        self.pipeline.addConstant("templatesSpecs", r"path=%tk_module_path%\templates\RigSpecs\assets_specs.py")
        self.pipeline.addConstant("assetTypeToSpec", r"path=%tk_module_path%\templates\RigSpecs\asset_type_to_spec.py")
        # self.pipeline.addConstant("rigOrients", r"path={0}\templates\RigSpecs\rig_orients.py".format(self.modulePath), [({"assetType":"props"}, None)])
        self.pipeline.addConstant("rigOrients",None)

        # Contantes
        self.pipeline.addConstant("rigGrp", "rig_grp")
        self.pipeline.addConstant("ctrlSetName", "::*anim_set")
        self.pipeline.addConstant("geoSetName", "::*geo_set")
        self.pipeline.addConstant("modNamespace", "MOD")
        self.pipeline.addConstant("hideSuffix", ["_PRO", "_PXY"])
        self.pipeline.addConstant("controlerWidth", 2.2)
        self.pipeline.addConstant("hilightController", ["Hips","Global_SRT","Local_SRT", "POS_ctrl", "TRAJ_ctrl", "Fly"])
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
        
        self.resolveProperties()

    def getProject(self):
        return tkc.getTool().options["project"]

    def setOverwrite(self, inRoots):
        for key, value in self.pipeline._patterns.items():
            for inRoot, outRoot in inRoots:
                if value._value.startswith(inRoot):
                    projData = self.pipeline._patterns[key]
                    projData._overrides.append(({"repo": "server"}, projData._value.replace(inRoot, outRoot)))
                    break

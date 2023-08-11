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

        self.pipeline.addConstant("modulePath", os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)))
        self.name = kwargs["inName"] or self.getProject()
        os.environ["TK_MODULE_PATH"] = self.modulePath

        ### __INIT__Patterns__ ###

        path = ctx.resolvePath(r"Q:\{projectNumber:[0-9]{4}}_{projectName}" , {"projectName":self.name})
        if not path is None:
            self.pipeline.addPattern("IOProject", path)
        else:
            self.pipeline.addPattern("IOProject", r"Q:\0000_{0}".format(self.name))
            tkLogger.debug("No valid Input Output folder found ('{}''), used '{}' !".format(r"Q:\{projectNumber:[0-9]{4}}_{projectName}", r"Q:\0000_{0}".format(self.name)))

        self.pipeline.addPattern("_template", self.modulePath + r"\templates")

        self.pipeline.addPattern("OSCARProject", r"Z:\ToonKit\OSCAR\Projects\{projectName}")
        self.pipeline.addPattern("releasePattern", r"{IOProject}\DELIVERY\{assetType}\{name:.+}\{name:.+}_{lodTag}_v{version:[0-9]{3}<-1>}.ma")
        self.pipeline.addPattern("deltaFolder", r"{IOProject}\Interne\DELTAS")
        self.pipeline.addPattern("assetRigPattern", r"{OSCARProject}\Assets\{name:.+}\{name:.+}.ma")
        self.pipeline.addPattern("assetMasterPattern", r"{OSCARProject}\Assets\{name:.+}\{name:.+}_MASTER.ma")
        self.pipeline.addPattern("assetMasterRawPattern", r"{OSCARProject}\Assets\{name:.+}\{name:.+}_MASTER_RAW.ma")
        self.pipeline.addPattern("assetAnPattern", r"{OSCARProject}\Assets\{name:.+}\AN\{name:.+}.ma")
        self.pipeline.addPattern("assetRawPattern", r"{OSCARProject}\Assets\{name:.+}\AN\{name:.+}_RAW.ma")
        self.pipeline.addPattern("modelingPattern", r"Q:\{projectNumber:[0-9]{4}_{projectName}\SOURCE\{name:.+}_v{modVersion:[0-9]{3}<-1>}.abc") # <= To be refered to the SOURCE dir 
        self.pipeline.addPattern("scriptFolder", r"{OSCARProject}\Scripts") # Unused for now
        self.setOverwrite([("Z:", "Q:")])
        self.pipeline.context = {"projectName": self.name, "repo":"local"}

        ### __INIT__Constants__ ###    
        self.pipeline.addConstant("baseContextKeys", ["projectName", "repo"])
        self.pipeline.baseContext = {key:value for (key, value) in self.pipeline.context.items() if key in self.baseContextKeys}

        # PathProperties
        #ShadowRig
        self.pipeline.addConstant("shadowrigActive", False, [({"assetType":"props"}, False)])
        self.pipeline.addConstant("shadowRig", r"path=%tk_module_path%\templates\ShadowRig\shadowrig_hierarchy.py")
        self.pipeline.addConstant("shadowrigOrients", r"path=%tk_module_path%\templates\ShadowRig\shadowrig_orients.py")
        self.pipeline.addConstant("shadowrigPreset", r"path=%tk_module_path%\templates\ShadowRig\shadowrig_preset.py")
        self.pipeline.addConstant("shadowrigRenamings", r"path=%tk_module_path%\templates\ShadowRig\shadowrig_renamings.py")
        self.pipeline.addConstant("shadowrigRotateorders", r"path=%tk_module_path\templates\ShadowRig\shadowrig_rotateorders.py")

        #Mocap
        self.pipeline.addConstant("mocapActive", False, [({"assetType":"props"}, False)])
        self.pipeline.addConstant("yup_zfront_preset", r"path=%tk_module_path%\templates\yup_zfront_preset.py")
        self.pipeline.addConstant("mocapPrefix", "MayaHIK_")
        self.pipeline.addConstant("mocapBinding", r"path=%tk_module_path%\templates\Mocap\mocap_binding.py")
        self.pipeline.addConstant("mocapOrient", r"path=%tk_module_path%\templates\Mocap\mocap_orients.py")
        self.pipeline.addConstant("mocapSkeletonPath", r"Q:\Bank\Mocap\SkeletalModel_Biped_ToonkitHIK.ma")

        #RigSpecks
        self.pipeline.addConstant("rotationOrder", {}) # r"path=%tk_module_path%\templates\RigSpecs\rotation_order.py"
        self.pipeline.addConstant("pickWalk", []) #r"path=%tk_module_path%\templates\RigSpecs\pick_walk.py"
        self.pipeline.addConstant("templatesSpecs", r"path=%tk_module_path%\templates\RigSpecs\assets_specs.py")
        self.pipeline.addConstant("assetTypeToSpec", r"path=%tk_module_path%\templates\RigSpecs\asset_type_to_spec.py")
        self.pipeline.addConstant("rigOrients", {}) # r"path=%tk_module_path%\templates\RigSpecs\rig_orients.py", [({"assetType":"props"}, {})]

        # Contantes
        self.pipeline.addConstant("preConformScripts", None)
        self.pipeline.addConstant("postConformScripts", None)
        self.pipeline.addConstant("preReleaseScripts", None)
        self.pipeline.addConstant("postReleaseScripts", None)
        
        self.pipeline.addConstant("mocapAdditionalMatchers", { #Used in menu items for mocap
            "Ct_Neck_MCP_0_JNT":"Neck_FK_1",
            "Ct_Spine_MCP_1_JNT":(("Spine_FK_2",0.5),("Spine_FK_3",0.5)),
            "Ct_Spine_MCP_2_JNT":(("Spine_FK_3",0.2),("Spine_FK_4",0.8)),
        },)
        self.pipeline.addConstant("bonesToFix", [ #Dirty quick fix, should be deprecated and deleted after OSCAR fix
            "::Left_Rear_LEG_IK_Bone_0",
            "::Left_Rear_IK3_DogLeg_Bone_0",
            "::Right_Rear_LEG_IK_Bone_0",
            "::Right_Rear_IK3_DogLeg_Bone_0",
            "::Left_Fore_IK3_DogLeg_Bone_0",
            "::Left_Fore_IK3_DogLeg_Bone_0",
            "::Left_Fore_LEG_IK_Bone_0",
            "::Right_Fore_IK3_DogLeg_Bone_0",
            "::Right_Fore_LEG_IK_Bone_0"
            ],)

        self.pipeline.addConstant("lodTags", {"LD":"proxy", "MD":"animation", "HD":"deformation"})
        self.pipeline.addConstant("geometryGrp", "Geometry_GRP")
        self.pipeline.addConstant("ctrlSetName", "anim_set")
        self.pipeline.addConstant("geoSetName", "geo_set")
        self.pipeline.addConstant("hiLockedTransformAttrs", [
            {"name":"tx", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"ty", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"tz", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"rx", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"ry", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"rz", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"sx", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"sy", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"sz", "type":"float", "value":None, "keyable":False, "lock":True},
            {"name":"visibility", "type":"bool", "value":None, "lock":True},])
        
        self.pipeline.addConstant("mocapDrivenChannels", []) #r"path=%tk_module_path%\templates\RigSpecs\baked_attrs.py"

        self.pipeline.addConstant("conformHierarchy", r"path=%tk_module_path%\templates\RigSpecs\rig_conform_hierarchy.py")

        self.pipeline.addConstant("refModActive", False)
        self.pipeline.addConstant("modNamespace", "MOD")

        self.pipeline.addConstant("hideSuffix", ["_PRO", "_PXY"]) # To be deprecated with benefit of standardisation of mod creation
        self.pipeline.addConstant("controlerWidth", 2.2)
        self.pipeline.addConstant("hilightController", ["Hips","Global_SRT","Local_SRT", "POS_ctrl", "TRAJ_ctrl", "Fly"])
        self.pipeline.addConstant("excludeTags", []) # To be deprecated with benefit of standardisation of mod creation
        self.pipeline.addConstant("dualQuatMeshs", ["*caruncle_layer1"])
        #OldVersion, To be deprecated:
        self.pipeline.addConstant("deletePatternList", [".+_OSCAR_Attributes",
                    ".+_TK_CtrlsChannelsDic",
                    ".+_TK_CtrlsDic",
                    ".+_TK_KeySets",
                    ".+_TK_KeySetsTree",
                    ".+_TK_ParamsDic",
                    ".+Neutral.+failed",
                    ".+FKREF",
                    ".+IKREF",
                    ".+Leg_Root_Sensor.+",
                    ".+_Frame",
                    ".*abcData",
                    ".+_HandProp_Main_Deform",
                    ".+_poleHelper"])
        
        self.pipeline.addConstant("optiAttrParentExcept", "|".join(["(.+_OSCAR_Attributes",
                                                                    ".+_TK_CtrlsChannelsDic",
                                                                    ".+_TK_CtrlsDic",
                                                                    ".+_TK_KeySets",
                                                                    ".+_TK_KeySetsTree",
                                                                    ".+_TK_ParamsDic",
                                                                    ".+Neutral.+failed)$"]))
        self.pipeline.addConstant("optiAttrNameExcept", "|".join(["(.+_Bone0_Init",
                                                                  ".+_Bone1_Init",
                                                                  ".+_Bone0_length",
                                                                  ".+_Bone1_length",
                                                                  ".+_Scale|timecode_.+",
                                                                  "mocap_clip_id)$"]))
        self.pipeline.addConstant("optiObjExcept", "|".join(["(.+_OSCAR_Attributes",
                                                             ".+_TK_CtrlsChannelsDic",
                                                             ".+_TK_CtrlsDic",
                                                             ".+_TK_KeySets",
                                                             ".+_TK_KeySetsTree",
                                                             ".+_TK_ParamsDic",
                                                             ".+Neutral.+failed",
                                                             ".+FKREF",".+IKREF",
                                                             ".+Leg_Root_Sensor.+",
                                                             ".+_Frame",
                                                             ".*abcData)$"]))
        
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

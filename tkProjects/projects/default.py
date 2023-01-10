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

class default(tkProject):
    def __init__(self, *args, **kwargs):
        super(default, self).__init__(*args, **kwargs)

        self.modulePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
        self.name = self.getProject()
        
        self.pipeline.addPattern("IOProject", ctx.resolvePath(r"Q:\{projectNumber:[0-9]{4}}_{projectName}", {"projectName":self.name}))
        self.pipeline.addPattern("OSCARProject", r"Z:\ToonKit\OSCAR\Projects\{projectName}")
        self.pipeline.addPattern("releasePatern", r"{IOProject}\DELIVERY\{assetType}\{name:.+}\{name:.+}_{lodTag}_v{version:[0-9]{3}<-1>}.ma")
        self.pipeline.addPattern("assetPatern", r"{OSCARProject}\Assets\{name:.+}\AN\{name:.+}.ma")
        self.pipeline.addPattern("deltaFolder", r"{IOProject}\Interne\DELTAS")
        self.pipeline.addPattern("scriptFolder", r"{OSCARProject}\Scripts")
        self.pipeline.addPattern("template", self.modulePath + r"\templates")
        self.pipeline.addPattern("AngleListener", r'{template}\AngleListener\{templateName}.py')
        self.pipeline.addPattern("ShadowRig", r'{template}\ShadowRig\{templateName}.py')
        self.pipeline.addPattern("RotationOrder", r"{template}\RotationOrder\{templateName}.py")
        self.pipeline.addPattern("PickWalk", r"{template}\PickWalk\{templateName}.py")
        self.pipeline.addPattern("conform", r"{scriptFolder}\Conform{projectName}.py")

        self.pipeline.context = {"projectName": self.name}

        # RawPath
        self.releasePatern = self.pipeline.getPattern("releasePatern")
        self.localAssetPatern = self.pipeline.getPattern("assetPatern")
        self.deltaFolder = self.pipeline.getPattern("deltaFolder")
        self.scriptFolder = self.pipeline.getPattern("scriptFolder")
        self.conformPath = self.pipeline.getPattern("conform")

        # PathProperties
        self.AngleListener = r"path={0}".format(self.pipeline.getPattern("AngleListener", {"templateName":"AngleListener"}))
        self.ShadowRig = r"path={0}".format(self.pipeline.getPattern("ShadowRig", {"templateName":"ShadowRig"}))
        self.RotationOrder = r"path={0}".format(self.pipeline.getPattern("RotationOrder", {"templateName":"RotationOrder"}))
        self.PickWalk = r"path={0}".format(self.pipeline.getPattern("PickWalk", {"templateName":"PickWalk"}))
        
        self.resolveProperies()

        # Contantes
        self.root= (["Z:", "Q:"])
        self.ctrlSetName = "*_anim_set"
        self.geoSetName = "*_geo_selset"
        self.hideSuffix = ["_PRO", "_PXY"]
        self.templatesSpecs = [
            ("Global_SRT", "props"),
            ("Left_Arm_ParamHolder", "char"),
            ("left_RearLeg_ParamHolder", "char")
        ]

        self.rigGrp = "rig_grp"

    def getProject(self):
        return tkc.TOOL.options["project"]

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
__author__ = "Cyril GIBAUD - Toonkit"

import logging
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
DEBUG = True

from ...tkProjects.tkProject import tkProject
from ...tkProjects.dbEngines.ShotgunEngine.ShotgunEngine import shotgunEngine

REPOSITORIES = {
    "default":{},"tkDeliverIN":{},"tkDeliverOUT":{},"tsuProd":{},"tsuDeliver":{}
}

#tkProd
default =  {
    "name":"tkProd",
    "entities":{
            "Anim":     r"Q:\0088_Marmottes2020\PROJECT\PROJECT\FILM\{Episode}.Seq{SeqNumber:[0-9]{2}}-Cut{CutNumber:[0-9]{3}}\{Episode}.Seq{SeqNumber:[0-9]{2}}-Cut{CutNumber:[0-9]{3}}_{Task}_v{Version:[0-9]{4}}.ma",
            "AnimCut":  r"Q:\0088_Marmottes2020\PROJECT\PROJECT\FILM\{Episode}.Seq{SeqNumber:[0-9]{2}}-Cut010_Cut\{Episode}.Seq{SeqNumber:[0-9]{2}}-Cut010_{Task}_v{Version:[0-9]{4}}_Cut{CutNumber:[0-9]{3}}.ma",
            "Character":r"Q:\0088_Marmottes2020\PROJECT\PROJECT\ASSETS\characters\{AssetName}\rig\{AssetName}_rig_v{Version:[0-9]{3}}.ma",
            "Props":    r"Q:\0088_Marmottes2020\PROJECT\PROJECT\ASSETS\props\{AssetFamily}\{AssetName}\rig\{AssetName}_rig_v{Version:[0-9]{3}}.ma",
            "Set":      r"Q:\0088_Marmottes2020\PROJECT\PROJECT\ASSETS\environments\{AssetName}\rig\{AssetName}_rig_v{Version:[0-9]{3}}.{Extension:ma|mb}",
        },
}
REPOSITORIES["default"] = default


tkDeliverIN =  {
    "name":"tkDeliverIN",
    "entities":{
            "ShotCache":        r"Q:\0088_Marmottes2020\PROJECT\PROJECT\FILM\{Episode}\Seq{SeqNumber:[0-9]{2}}\Cut{CutNumber:[0-9]{3}}\001_{EpisodeShortName}_{CutNumber4:[0-9]{4}}_{Asset}_{Task}_v{Version:[0-9]{3}}.abc",
            "SequencePlayblast":r"Q:\0088_Marmottes2020\PROJECT\PROJECT\FILM\{Episode}\Seq{SeqNumber:[0-9]{2}}\001_{EpisodeShortName}_playblast_{Task}_v{Version:[0-9]{3}}.mp4",
        },
}
REPOSITORIES["tkDeliverIN"] = tkDeliverIN


tkDeliverOUT =  {
    "name":"tkDeliverOUT",
    "entities":{
            "ShotCache":        r"Q:\0088_Marmottes2020\_DELIVERIES\{Today}\TOONKIT\shots\{Episode}\sh{CutNumberStripped:[0-9]{2}}\cache\001_{EpisodeShortName}_{CutNumber4:[0-9]{4}}_{Asset}_{Task}_v{Version:[0-9]{3}}.abc",
            "SequencePlayblast":r"Q:\0088_Marmottes2020\_DELIVERIES\{Today}\TOONKIT\shots\{Episode}\preview\001_{EpisodeShortName}_playblast_{Task}_v{Version:[0-9]{3}}.mp4",
        },
}
REPOSITORIES["tkDeliverOUT"] = tkDeliverOUT


tsuProd =  {
    "name":"tsuProd",
    "entities":{
            "Anim":     r"P:\__PROD__\Marmottes\WORK\lesmarmottes2020\00_UNKNOWN\{Episode}.Seq{SeqNumber:[0-9]{2}}-Cut{CutNumber:[0-9]{3}}_{Task}_v{Version:[0-9]{4}}.ma",#Escrime.Seq01-Cut010_Traj_v0001.ma
            "Character":r"P:\__PROD__\Marmottes\WORK\lesmarmottes2020\01_Workflow\Assets\Character\{AssetName}\Export\{AssetName}_rig\v{Version:[0-9]{4}}_rig_toonKit\centimeter\{AssetName}_rig_v{Version:[0-9]{3}}.ma",
            "Props":    r"P:\__PROD__\Marmottes\WORK\lesmarmottes2020\01_Workflow\Assets\Prop\{AssetName}\Export\{AssetName}_rig\v{Version:[0-9]{4}}_rig_toonKit\centimeter\{AssetName}_rig_v{Version:[0-9]{3}}.ma",
            "Set":      r"P:\__PROD__\Marmottes\WORK\lesmarmottes2020\01_Workflow\Assets\Environment\{AssetName}\Export\{AssetName}_rig\v{Version:[0-9]{4}}_rig_toonKit\centimeter\{AssetName}_rig_v{Version:[0-9]{3}}.{Extension:ma|mb}",
        },
}
REPOSITORIES["tsuProd"] = tsuProd

tsuDeliver =  {
    "name":{"tsuDeliver"},
    "entities":{
            "SequencePlayblast":r"Q:\0088_Marmottes2020\PROJECT\PROJECT\FILM\{Episode}.Seq{SeqNumber:[0-9]{2}-Cut010\{Episode}.Seq{SeqNumber:[0-9]{2}-Cut010_{Task}_v{Version:[0-9]{4}}.mp4",
        },
}
REPOSITORIES["tsuDeliver"] = tsuProd

class demo(tkProject):
    def __init__(self, inEngine=shotgunEngine(inScriptName="Tsunami", inScriptKey="jeillsltAziewnnddp$gndas5"), *args, **kwargs):
        super(demo, self).__init__(inEngine, *args, **kwargs)

        self.name="demo"
        self.id = 534
        self._repositories = REPOSITORIES
        
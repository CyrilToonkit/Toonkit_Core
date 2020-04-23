from Toonkit_Core.tkProjects.tkProject import tkProject

REPOSITORIES = {
    "default":{},"tkDeliverIN":{},"tkDeliverOUT":{},"tsuProd":{},"tsuDeliver":{}
}

#tkProd
default =  {
    "name":{"tkProd"},
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
    "name":{"tkDeliverIN"},
    "entities":{
            "ShotCache":        r"Q:\0088_Marmottes2020\PROJECT\PROJECT\FILM\{Episode}\Seq{SeqNumber:[0-9]{2}}\Cut{CutNumber:[0-9]{3}}\001_{EpisodeShortName}_{CutNumber4:[0-9]{4}}_{Asset}_{Task}_v{Version:[0-9]{3}}.abc",
            "SequencePlayblast":r"Q:\0088_Marmottes2020\PROJECT\PROJECT\FILM\{Episode}\Seq{SeqNumber:[0-9]{2}}\001_{EpisodeShortName}_playblast_{Task}_v{Version:[0-9]{3}}.mp4",
        },
}
REPOSITORIES["tkDeliverIN"] = tkDeliverIN


tkDeliverOUT =  {
    "name":{"tkDeliverOUT"},
    "entities":{
            "ShotCache":        r"Q:\0088_Marmottes2020\_DELIVERIES\{Today}\TOONKIT\shots\{Episode}\sh{CutNumberStripped:[0-9]{2}}\cache\001_{EpisodeShortName}_{CutNumber4:[0-9]{4}}_{Asset}_{Task}_v{Version:[0-9]{3}}.abc",
            "SequencePlayblast":r"Q:\0088_Marmottes2020\_DELIVERIES\{Today}\TOONKIT\shots\{Episode}\preview\001_{EpisodeShortName}_playblast_{Task}_v{Version:[0-9]{3}}.mp4",
        },
}
REPOSITORIES["tkDeliverOUT"] = tkDeliverOUT


tsuProd =  {
    "name":{"tsuProd"},
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
    def __init__(self):
        self.name="demo"
        self._defaultRepository="default"
        self._repositories = REPOSITORIES
        
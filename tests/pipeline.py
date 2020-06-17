import Toonkit_Core.tkProjects.tkPipeline as tkpipe
reload(tkpipe)

pipe = tkpipe.tkPipeline()

pipe.addPattern("ProjectPath", r"Q:\0088_Marmottes2020\PROJECT\PROJECT",
    [({"repo":"Tsunami"}, r"P:\__PROD__\Marmottes\WORK\lesmarmottes2020"),
    ])

pipe.addPattern("Sequence", r"Seq{SeqNumber:[0-9]{2}}")

pipe.addPattern("Shot", r"Cut{CutNumber:[0-9]{3}}")

pipe.addPattern("ShotLongName", r"{Episode}.{Sequence}-{Shot}")

pipe.addPattern("ShotFile", r"{ShotLongName}_{Task}_v{Version:[0-9]{4}}.ma")

pipe.addPattern("ShotPath", r"{ProjectPath}\FILM\{ShotLongName}\{ShotFile}")

#pipe.context = {"Episode":"swimming", "SeqNumber":1, "CutNumber":10, "Task":"blocking", "Version":1}

print pipe.getPattern("ShotPath")
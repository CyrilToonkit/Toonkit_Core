from imp import reload
from ..tkProjects import tkProjectProp as tpr
reload(tpr)
from ..tkProjects import tkProjectObj as to
reload(to)

from ..tkProjects import tkAsset as ta
reload(to)

from ..tkProjects import tkProject as tp
reload(tp)

from ..tkProjects.dbEngines import dbEngine as dbEngine
reload(dbEngine)

from ..tkProjects.dbEngines.ShotgunEngineimport import ShotgunEngine as shotgunEngine
reload(shotgunEngine)


from ..tkProjects.projects import demo as demo
reload(demo)

import Toonkit_Core.tkCore as tc
reload(tc)

#TODO : Field type conversions
#   dates string ==> datetime
#   durations string => timedelta
#TODO : Ordering ?
#TODO : Auto-omitting ?

#-----------------------------------------------------
#----    GET
#-----------------------------------------------------

#Go through Assets and print their corresponding Shots
#-----------------------------------------------------

for asset in tc.getProject().Assets:
    print (asset)
    for shot in asset.Shots:
        print (" - {0}".format(shot))

#Go through an asset Tasks and print their Notes
#-----------------------------------------------------
asset = tc.getProject().GetAsset(name="marmotte")
for task in asset.Tasks:
    print (task)
    for note in task.Notes:
        print (" - {0}".format(note))

#Go through all Shots that are not "omt"
#-----------------------------------------------------
for shot in tc.getProject().GetShots(status=("!=", "omt")):
    print (shot)




#2 TODO : Sum durations of all shots in a Sequence
#Tricky case, use a variable as criterion, not directly a property, see how to use patterns for that...

sequenceDuration = 0
for shot in tc.getProject().GetEpisode(name="swimming").GetSequence(SeqNumber=1).Shots:
    sequenceDuration += shot.duration
print ("sequenceDuration",sequenceDuration)

#Files/paths
#-------------------------------

#3 TODO : Get the "last" path of an asset, given its step
print (tc.getProject().GetAsset(name="marmotte").GetPath(step="rig"))#or .GetPath(Step="rig", Version=-1)

#3 TODO : Get all the existings paths of an asset, given its step
print (tc.getProject().GetAsset(name="marmotte").GetPaths(step="mod"))



#-----------------------------------------------------
#----    SET
#-----------------------------------------------------

#Update an Asset property (status)
#-----------------------------------------------------

marmotte = tc.getProject().GetAsset(name="marmotte")
print ("1 : Original", marmotte.status)
#Try to push without changing anything
marmotte.push()
#We get a warning indicating nothing has changed, if we want to force-push use
#marmotte.push(inForce=True)

#Actually change the value
marmotte.status = "apr"
print ("2 : Set to 'apr'", marmotte.status)
#The changed property is visible in "modifiedProperties" dict
print ("2 : modified properties", marmotte.modifiedProperties)

#If we pull here we lose the modifications
marmotte.pull()
print ("3 : pulled back to original", marmotte.status)

#Change the value again...
marmotte.status = "apr"

#... and push
marmotte.push()

#Value changed, even if pulled back again
marmotte.pull()
print ("4 : Set to 'apr' and pushed ", marmotte.status)

#4 TODO : Link an asset to a shot
#-----------------------------------------------------
#Tricky case, in shotgun a shot does not have an episode field (must be retrieved through Sequence...)
shot = tc.getProject().GetShot(Sequence=(".Episode.name", "==", "swimming"))
#tc.getProject().GetAsset(name="marmotte").SetShots(shot, CutNumber=10), add=True)


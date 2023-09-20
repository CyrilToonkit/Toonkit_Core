try:
    import winsound
except:
    winsound=None

SND_ASYNC = 1
SND_NODEFAULT = 2
SND_NOSTOP = 16
SND_NOWAIT = 8192
SND_ALIAS = 65536
SND_FILENAME = 131072
SND_MEMORY = 4
SND_PURGE = 64
SND_LOOP = 8
SND_APPLICATION = 128
MB_OK = 0
MB_ICONASTERISK = 64
MB_ICONEXCLAMATION = 48
MB_ICONHAND = 16
MB_ICONQUESTION = 32

def PlaySound(sound, flags=SND_ALIAS | SND_ASYNC):
    if not winsound is None:
        winsound.PlaySound(sound, flags)

def error():
    PlaySound("SystemHand")

def exit():
    PlaySound("SystemExit")

def question():
    PlaySound("SystemQuestion")
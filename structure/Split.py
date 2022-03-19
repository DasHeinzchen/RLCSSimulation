import os
import Globals
import json
import structure.Major as Major

class Split:
    def __init__(self, id="", current=False, currentEvent="", name=""):
        self._dict = {}
        self._id = id
        self._current = current
        self._currentEvent = currentEvent
        self._name = name

    def loadData(self):
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[1] + ".json")
        self._dict = json.load(file)

        self._id = self._dict["id"]
        self._current = self._dict["current"]
        self._currentEvent = self._dict["currentEvent"]
        self._name = self._dict["name"]

        file.close()

    def saveData(self):
        self._dict.update({
            "id": self._id,
            "current": self._current,
            "currentEvent": self._currentEvent,
            "name": self._name
        })
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[1] + ".json", "w")
        file.write(json.dumps(self._dict, indent=5))
        file.close()

    @property
    def current(self):
        return self._current

    @property
    def currentEvent(self):
        return self._currentEvent


def initializeSplit(id):
    id = id.split("_")
    os.mkdir(Globals.settings["path"] + "seasons\\" + id[0] + "\\" + id[1])
    file = open(Globals.settings["path"] + "seasons\\" + id[0] + "\\" + id[1] + "\\" + id[1] + ".json", "a")
    file.write("{}")
    file.close()
    id = id[0] + "_" + id[1]
    if id[-1:] == "1":
        Split(id=id, current=True, currentEvent=id + "_MJR").saveData()             #Put in id of first event of split
        Globals.current_split = id
    else:
        Split(id=id, currentEvent=id + "_MJR").saveData()                           #Put in id of first event of split

    Major.initializeMajor(id + "_MJR", current=True)        #Put first event of Split with 'current=True'

def getSplitById(id):
    split = Split(id=id)
    split.loadData()
    return split

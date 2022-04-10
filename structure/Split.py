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


def initializeSplit(splitId, path):
    with open(path, "w") as splitFile:
        dict = {
            "current": False,
            "currnetEvent": splitId + "_MJR",                   #TODO change to actual first event
            "name": "Split"
        }
        if splitId[-1] == "1":
            dict["current"] = True
            dict["name"] = "Fall Split"
        elif splitId[-1] == "2": dict["name"] = "Winter Split"
        elif splitId[-1] == "3": dict["name"] = "Spring Split"

        splitFile.write(json.dumps(dict, indent=5))

def getSplitById(id):
    split = Split(id=id)
    split.loadData()
    return split

def setupSplits(seasonId):
    path = Globals.settings["path"] + "seasons\\" + seasonId + "\\SPL"
    for i in range(3):
        try:
            os.mkdir(path + str(i + 1))
        except OSError:
            print("Creation of the Split directory failed")
        else:
            open(path + str(i + 1) + "\\split.json", "a").close()
            splitId = seasonId + "_SPL" + str(i + 1)
            Major.setupMajor(splitId)
            for region in Globals.regions:
                try:
                    os.mkdir(path + str(i + 1) + "\\" + region)
                except OSError:
                    print("Creation of the region directory failed")
                else:
                    open(path + str(i + 1) + "\\" + region + "\\rankings.json", "a").close()

            initializeSplit(splitId, path + str(i + 1) + "\\split.json")

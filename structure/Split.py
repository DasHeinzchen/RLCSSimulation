import os
import Globals
import json
import structure.Major as Major

class Split:
    def __init__(self, splitId):
        self._id = splitId
        self._current = False
        self._currentEvent = ""
        self._name = ""

        self.loadData()

    def loadData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\split.json", "r") as splitFile:
            dictionary = json.load(splitFile)
            self._current = dictionary["current"]
            self._currentEvent = dictionary["currentEvent"]
            self._name = dictionary["name"]

        return self

    def saveData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\split.json", "w") as splitFile:
            dictionary = {
                "current": self._current,
                "currentEvent": self._currentEvent,
                "name": self._name
            }

            splitFile.write(json.dumps(dictionary, indent=5))

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
            "currentEvent": splitId + "_MJR",                   #TODO change to actual first event
            "name": "Split"
        }
        if splitId[-1] == "1":
            dict["current"] = True
            dict["name"] = "Fall Split"
        elif splitId[-1] == "2": dict["name"] = "Winter Split"
        elif splitId[-1] == "3": dict["name"] = "Spring Split"

        splitFile.write(json.dumps(dict, indent=5))

def getSplitById(id):
    return Split(id)

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

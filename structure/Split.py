import os
import Globals
import json
import structure.Major as Major

class Split:
    def __init__(self, splitId):
        self._id = splitId
        self._current = False
        self._currentEvent = ""
        self._upcomingEvents = []
        self._name = ""

        self.loadData()

    def loadData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\split.json", "r") as splitFile:
            dictionary = json.load(splitFile)
            self._current = dictionary["current"]
            self._currentEvent = dictionary["currentEvent"]
            self._name = dictionary["name"]
            self._upcomingEvents = dictionary["upcomingEvents"]
            splitFile.close()

        return self

    def saveData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\split.json", "w") as splitFile:
            dictionary = {
                "current": self._current,
                "currentEvent": self._currentEvent,
                "upcomingEvents": self._upcomingEvents,
                "name": self._name
            }

            splitFile.write(json.dumps(dictionary, indent=5))
            splitFile.close()

    def startSplit(self):
        self._current = True
        self._currentEvent = self._upcomingEvents.pop(0)
        self.saveData()

        if self._currentEvent[-3:] == "MJR":
            Major.Major(self._currentEvent).start()

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current

    @property
    def currentEvent(self):
        return self._currentEvent


def initializeSplit(splitId, path):
    with open(path, "w") as splitFile:
        dict = {
            "current": False,
            "currentEvent": "",
            "upcomingEvents": [splitId + "_MJR"],
            "name": "Split"
        }
        if splitId[-1] == "1":
            dict["current"] = True
            dict["name"] = "Fall Split"
        elif splitId[-1] == "2": dict["name"] = "Winter Split"
        elif splitId[-1] == "3": dict["name"] = "Spring Split"

        splitFile.write(json.dumps(dict, indent=5))
        splitFile.close()

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

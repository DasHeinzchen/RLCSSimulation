import Globals
import json

import Team
import tournament.Formats as Formats

class Major:
    def __init__(self, id="", current=False, name="", formatType=""):
        self._id = id
        self._current = current
        self._name = name
        self._teams = [] #seeded
        self._formatType = formatType
        self._dict = {}

    def loadData(self):
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[2] + ".json")
        self._dict = json.load(file)

        self._id = self._dict["id"]
        self._current = self._dict["current"]
        self._name = self._dict["name"]
        self._formatType = self._dict["formatType"]

        file.close()
        return self

    def saveData(self, initialize=False):
        self._dict.update({
            "id": self._id,
            "current": self._current,
            "name": self._name,
            "formatType": self._formatType
        })
        if not initialize:
            self._dict.update({"format": Globals.format.dict})
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[2] + ".json", "w")
        file.write(json.dumps(self._dict, indent=5))
        file.close()

    def updateFormatDict(self, dict={}):
        self._dict.update({"format": dict})
        self.saveData()

    @property
    def dict(self):
        return self._dict

    @property
    def formatType(self):
        return self._formatType


def initializeMajor(majorId, path):
    with open(path, "w") as majorFile:
        dict = {
            "current": True,                    #TODO change to false when not first split event
            "formatType": "",
            "name": "Major",
            "format": {}
        }
        if majorId.split("_")[1][-1] == "1":
            dict["formatType"] = "Fall_Format"
            dict["name"] = "Fall Major"
        elif majorId.split("_")[1][-1] == "2":
            dict["formatType"] = "Winter_Format"
            dict["name"] = "Winter Major"
        elif majorId.split("_")[1][-1] == "3":
            dict["formatType"] = "Spring_Format"
            dict["name"] = "Spring Major"

        dict["format"] = Formats.initializeFormat(dict["formatType"], majorId, current=dict["current"])

        majorFile.write(json.dumps(dict, indent=5))

def getMajorById(id):
    return Major(id=id).loadData()

def setupMajor(splitId):
    majorId = splitId + "_MJR"
    ids = splitId.split("_")
    path = Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\MJR.json"
    open(path, "a").close()

    initializeMajor(majorId, path)

import Globals
import json

import Team
import tournament.Formats as Formats

class Major:
    def __init__(self, id):
        self._id = id
        self._current = False
        self._name = ""
        self._teams = [] #seeded
        self._formatType = ""
        self._formatDict = {}

        self.loadData()

    def loadData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\MJR.json", "r") as majorFile:
            dictionary = json.load(majorFile)
            self._current = dictionary["current"]
            self._name = dictionary["name"]
            self._formatType = dictionary["formatType"]
            for team in dictionary["teams"]:
                self._teams.append(Team.getTeamById(team))
            self._formatDict = dictionary["format"]

            majorFile.close()
        return self

    def saveData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\MJR.json", "w") as majorFile:
            teamStrings = []
            for team in self._teams:
                teamStrings.append(team.id)
            dictionary = {
                "current": self._current,
                "formatType": self._formatType,
                "name": self._name,
                "teams": teamStrings,
                "format": self._formatDict
            }

            majorFile.write(json.dumps(dictionary, indent=5))
            majorFile.close()

    def start(self):
        self._current = True
        self._formatDict = Formats.startFormat(self._formatDict)
        self.saveData()

    @property
    def formatType(self):
        return self._formatType

    @property
    def formatDict(self):
        return self._formatDict

    @formatDict.setter
    def formatDict(self, formatDict):
        self._formatDict = formatDict


def initializeMajor(majorId, path):
    with open(path, "w") as majorFile:
        dict = {
            "current": False,
            "formatType": "",
            "name": "Major",
            "teams": [],
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

        dict["format"] = Formats.initializeFormat(dict["formatType"], majorId)

        majorFile.write(json.dumps(dict, indent=5))
        majorFile.close()

def getMajorById(id):
    return Major(id=id).loadData()

def setupMajor(splitId):
    majorId = splitId + "_MJR"
    ids = splitId.split("_")
    path = Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\MJR.json"
    open(path, "a").close()

    initializeMajor(majorId, path)

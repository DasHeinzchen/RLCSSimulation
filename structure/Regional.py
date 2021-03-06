import json

import Globals
import Team
from tournament import Formats
from structure import Qualification
from ranking import Ranking


class Regional:
    def __init__(self, regionalId):
        self._id = regionalId
        self._current = False
        self._name = ""
        self._teams = []
        self._formatType = ""
        self._formatDict = {}

        self.loadData()

    def loadData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" + \
                   ids[3][-1] + "\\Regional.json", "r") as regionalFile:
            dictionary = json.load(regionalFile)

            self._current = dictionary["current"]
            self._name = dictionary["name"]
            for team in dictionary["teams"]:
                self._teams.append(Team.getTeamById(team))
            self._formatType = dictionary["formatType"]
            self._formatDict = dictionary["format"]

            regionalFile.close()
        return self

    def saveData(self):
        ids = self._id.split("_")
        with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" + \
                  ids[3][-1] + "\\Regional.json", "w") as regionalFile:
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

            regionalFile.write(json.dumps(dictionary, indent=5))
            regionalFile.close()

    def start(self):
        self._current = True
        self._formatDict = Formats.startFormat(self._formatDict)
        teamStrings = []
        for team in self._teams:
            teamStrings.append(team.id)
        self._formatDict = Formats.addTeams(self._formatDict, teamStrings)
        self.saveData()

    def seeding(self):
        #TODO implement seeding
        teamStrings = []
        for team in self._teams:
            teamStrings.append(team.id)
        self._formatDict = Formats.addTeams(self._formatDict, teamStrings)
        self.saveData()

    def finish(self):
        self._current = False
        self.saveData()

        Ranking.addPoints(self._formatDict["placements"], self._id)

    @property
    def id(self):
        return self._id

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current

    @property
    def formatType(self):
        return self._formatType

    @property
    def formatDict(self):
        return self._formatDict

    @formatDict.setter
    def formatDict(self, formatDict):
        self._formatDict = formatDict

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, teams):
        self._teams = teams

    def addTeams(self, teams):
        for team in self._teams:
            if team.id == "_tbd":
                self._teams.remove(team)
        self._teams = self._teams + teams

        for i in range(16 - len(self._teams)):
            self._teams.append(Team.placeholder)


def initializeRegionals(regionalId, path, dictionaryQual):
    with open(path, "w") as regionalFile:
        dictionary = {
            "current": False,
            "formatType": "",
            "name": "Regional",
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "format": {}
        }
        if regionalId.split("_")[1][-1] == "1":
            dictionary["formatType"] = "Fall_Format"
            dictionary["name"] = Globals.regional[regionalId.split("_")[2]] + " Fall Regional " + str(regionalId[-1])
        elif regionalId.split("_")[1][-1] == "2":
            dictionary["formatType"] = "Winter_Format"
            dictionary["name"] = Globals.regional[regionalId.split("_")[2]] + " Winter Regional " + str(regionalId[-1])
        elif regionalId.split("_")[1][-1] == "3":
            dictionary["formatType"] = "Spring_Format"
            dictionary["name"] = Globals.regional[regionalId.split("_")[2]] + " Spring Regional " + str(regionalId[-1])

        dictionary["format"] = Formats.initializeFormat(dictionary["formatType"], regionalId)

        regionalFile.write(json.dumps(dictionary, indent=5))
        regionalFile.close()
    if regionalId[-1] == "1":
        Qualification.initializeQualification(regionalId, dictionaryQual=dictionaryQual)
    else:
        Qualification.initializeQualification(regionalId)


def setupRegionals(splitId, dictionaryQual={}):
    for region in Globals.regions:
        for i in range(3):
            regionalId = splitId + "_" + region + "_REG" + str(i + 1)
            ids = splitId.split("_")
            path = Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + region + "\\Regional" + \
                   str(i + 1) + "\\Regional.json"
            open(path, "a").close()
            initializeRegionals(regionalId, path, dictionaryQual)

            if not dictionaryQual == {}:
                if i == 0 and dictionaryQual["invit"][region]:
                    path = Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + region + \
                            "\\Regional" + str(i + 1) + "\\Invitational Qualifier.json"
                    open(path, "a").close()

            path = Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + region + "\\Regional" + \
                   str(i + 1) + "\\Qualifier Day 1.json"
            open(path, "a").close()

            path = Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + region + "\\Regional" + \
                   str(i + 1) + "\\Qualifier Day 2.json"
            open(path, "a").close()

            path = Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + region + "\\Regional" + \
                   str(i + 1) + "\\Qualifier Day 3.json"
            open(path, "a").close()

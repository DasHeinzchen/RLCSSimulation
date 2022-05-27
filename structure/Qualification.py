import json

import Globals, Team
from tournament import Formats


class QualDay:
    def __init__(self, qualifierId):
        self._id = qualifierId
        self._current = False
        self._canceled = False
        self._teams = []
        self._qualifiedTeams = []
        self._formatType = ""
        self._formatDict = {}

        self.loadData()

    def loadData(self):
        ids = self._id.split("_")
        dictionary = {}
        if ids[-1] == "INVIT":
            with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" +
                    ids[3][-1] + "\\Invitational Qualifier.json", "r") as qualifierFile:
                dictionary = json.load(qualifierFile)
                qualifierFile.close()
        else:
            with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" +
                    ids[3][-1] + "\\Qualifier Day " + ids[4][-1] + ".json", "r") as qualifierFile:
                dictionary = json.load(qualifierFile)
                qualifierFile.close()
        self._current = dictionary["current"]
        self._canceled = dictionary["canceled"]
        self._formatType = dictionary["formatType"]
        for team in dictionary["teams"]:
            self._teams.append(Team.getTeamById(team))
        for team in dictionary["qualifiedTeams"]:
            self._qualifiedTeams.append(Team.getTeamById(team))
        self._formatDict = dictionary["format"]

    def saveData(self):
        ids = self._id.split("_")
        teamStrings = [[], []]
        for team in self._teams:
            teamStrings[0].append(team.id)
        for team in self._qualifiedTeams:
            teamStrings[1].append(team.id)
        dictionary = {
            "current": self._current,
            "canceled": self._canceled,
            "formatType": self._formatType,
            "teams": teamStrings[0],
            "qualifiedTeams": teamStrings[1],
            "format": self._formatDict
        }
        if ids[-1] == "INVIT":
            with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" +
                      ids[3][-1] + "\\Invitational Qualifier.json", "w") as qualifierFile:
                qualifierFile.write(json.dumps(dictionary, indent=5))
                qualifierFile.close()
        else:
            with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" +
                    ids[3][-1] + "\\Qualifier Day " + ids[4][-1] + ".json", "w") as qualifierFile:
                qualifierFile.write(json.dumps(dictionary, indent=5))
                qualifierFile.close()

    def start(self):
        self._current = True

        self._formatDict = Formats.startFormat(self._formatDict)
        teamStrings = []
        for team in self._teams:
            teamStrings.append(team.id)
        self._formatDict = Formats.addTeams(self._formatDict, teamStrings)

        self.saveData()

    def cancel(self):
        self._canceled = True

    def finish(self):
        self._current = False
        for team in self._formatDict["placements"]["qualified"]:
            self._qualifiedTeams.append(Team.getTeamById(team))

        self.saveData()

    @property
    def id(self):
        return self._id

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, teams):
        self._teams = teams

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
    def qualifiedTeams(self):
        return self._qualifiedTeams

    @staticmethod
    def initialize(qualifierId, format="default"):
        dictionary = {
            "current": False,
            "canceled": False,
            "formatType": "QualDay",
            "teams": [],
            "qualifiedTeams": [],
            "format": {}
        }
        if qualifierId[-5:] == "INVIT":
            dictionary["formatType"] = "Invitational"
        elif format == "default":
            dictionary["formatType"] += qualifierId[-1]
        elif format == "open":
            dictionary["formatType"] = "OpenQualDay" + qualifierId[-1]

        dictionary["format"] = Formats.initializeFormat(dictionary["formatType"], qualifierId)

        ids = qualifierId.split("_")
        if ids[-1] == "INVIT":
            with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" +
                   ids[3][-1] + "\\Invitational Qualifier.json", "w") as qualifierFile:
                qualifierFile.write(json.dumps(dictionary, indent=5))
                qualifierFile.close()
        else:
            with open(Globals.settings["path"] + "seasons\\" + ids[0] + "\\" + ids[1] + "\\" + ids[2] + "\\Regional" +
                   ids[3][-1] + "\\Qualifier Day " + ids[4][-1] + ".json", "w") as qualifierFile:
                qualifierFile.write(json.dumps(dictionary, indent=5))
                qualifierFile.close()


def initializeQualification(regionalId, dictionaryQual={}):
    regionalId += "_QUAL"
    if dictionaryQual == {}:
        QualDay.initialize(regionalId + "1")
        QualDay.initialize(regionalId + "2")
        QualDay.initialize(regionalId + "3")
    else:
        if dictionaryQual["invit"][regionalId.split("_")[2]]:
            QualDay.initialize(regionalId[:-5] + "_INVIT")
            QualDay.initialize(regionalId + "1")
            QualDay.initialize(regionalId + "2")
            QualDay.initialize(regionalId + "3")
        else:
            QualDay.initialize(regionalId + "1")
            QualDay.initialize(regionalId + "2", format="open")
            QualDay.initialize(regionalId + "3", format="open")


def setupQualification(splitId, regional, seasonStart=False):
    #TODO add closed Qualification Teams
    unusedEvents = []
    for region in Globals.regions:
        teams = registerTeams(region)
        if len(teams) <= 48:
            unusedEvents.append(splitId + "_" + region + "_REG" + str(regional) + "_QUAL1")
            if seasonStart:
                qual = QualDay(splitId + "_" + region + "_REG1_QUAL2")
                if qual.formatType[:4] == "Open":
                    if len(teams) <= 32:
                        unusedEvents.append(splitId + "_" + region + "_REG1_QUAL2")
                        qual = QualDay(splitId + "_" + region + "_REG1_QUAL3")
                        qual.teams = teams
                        qual.saveData()
                    else:
                        qual.teams = teams
                        qual.saveData()
                else:
                    if len(teams) <= 8:
                        unusedEvents.append(splitId + "_" + region + "_REG1_QUAL2")
                        qual = QualDay(splitId + "_" + region + "_REG1_QUAL3")
                        qual.teams = teams
                        qual.saveData()
                    else:
                        qual.teams = teams
                        qual.saveData()
            else:
                if len(teams) <= 8:
                    unusedEvents.append(splitId + "_" + region + "_REG" + str(regional) + "_QUAL2")
                    qual = QualDay(splitId + "_" + region + "_REG" + str(regional) + "_QUAL3")
                    qual.teams = teams
                    qual.saveData()
                else:
                    qual = QualDay(splitId + "_" + region + "_REG" + str(regional) + "_QUAL2")
                    qual.teams = teams
                    qual.saveData()

        else:
            qual = QualDay(splitId + "_" + region + "_REG" + str(regional) + "_QUAL1")
            qual.teams = teams
            qual.saveData()

    for event in unusedEvents:
        qualDay = QualDay(event)
        qualDay.cancel()
        qualDay.saveData()

    return unusedEvents


def registerTeams(region, qualifiedTeams=[]):
    teams = Team.teamsByRegion(region)
    return teams

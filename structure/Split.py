import os
import Globals
import json

import Team
from structure import Major, Regional, Qualification
from ranking import Ranking


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
        if self._currentEvent == "":
            for event in Qualification.setupQualification(self._id, 1, seasonStart=True):
                self._upcomingEvents.remove(event)
        self._currentEvent = self._upcomingEvents.pop(0)
        self.saveData()

        if self._currentEvent[-3:] == "MJR":
            Major.Major(self._currentEvent).start()
        elif self.currentEvent[-4:-1] == "REG":
            Regional.Regional(self._currentEvent).start()
        elif self._currentEvent[-5:-1] == "QUAL":
            Qualification.QualDay(self._currentEvent).start()
        elif self._currentEvent[-5:] == "INVIT":
            Qualification.QualDay(self._currentEvent).start()

    def nextEvent(self):
        if len(self._upcomingEvents) > 0:
            self.startSplit()
            return False
        else:
            return True

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current

    @property
    def currentEvent(self):
        return self._currentEvent


def initializeSplit(splitId, path, dictionaryQual={}):
    with open(path, "w") as splitFile:
        dict = {
            "current": False,
            "currentEvent": "",
            "upcomingEvents": [],
            "name": "Split"
        }
        if splitId[-1] == "1":
            dict["current"] = True
            dict["name"] = "Fall Split"
        elif splitId[-1] == "2": dict["name"] = "Winter Split"
        elif splitId[-1] == "3": dict["name"] = "Spring Split"

        for i in range(3):
            for region in Globals.regions:
                if not dictionaryQual == {}:
                    if dictionaryQual["invit"][region] and i == 0:
                        dict["upcomingEvents"].append(splitId + "_" + region + "_REG" + str(i + 1) + "_INVIT")
                dict["upcomingEvents"].append(splitId + "_" + region + "_REG" + str(i + 1) + "_QUAL1")
            for region in Globals.regions:
                dict["upcomingEvents"].append(splitId + "_" + region + "_REG" + str(i + 1) + "_QUAL2")
            for region in Globals.regions:
                dict["upcomingEvents"].append(splitId + "_" + region + "_REG" + str(i + 1) + "_QUAL3")
            for region in Globals.regions:
                dict["upcomingEvents"].append(splitId + "_" + region + "_REG" + str(i + 1))
        dict["upcomingEvents"].append(splitId + "_MJR")

        splitFile.write(json.dumps(dict, indent=5))
        splitFile.close()

    if splitId[-1] == "1":      #Setting up teams for 1st qualifier of season
        '''for region in Globals.regions:
            qual = Qualification.QualDay(splitId + "_" + region + "_REG1_QUAL1")
            qual.teams = Team.teamsByRegion(region)
            qual.saveData()'''


def getSplitById(id):
    return Split(id)


def setupSplits(seasonId, dictionaryQual):
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
                    for j in range(3):
                        try:
                            os.mkdir(path + str(i + 1) + "\\" + region + "\\" + "Regional" + str(j + 1))
                        except OSError:
                            print("Creation of the Regional directory failed")
                except OSError:
                    print("Creation of the region directory failed")
                else:
                    ranking = open(path + str(i + 1) + "\\" + region + "\\rankings.json", "a")
                    ranking.write(json.dumps(Ranking.emptyRankingTable(), indent=5))
                    ranking.close()
            if splitId[-1] == "1":
                Regional.setupRegionals(splitId, dictionaryQual)
                initializeSplit(splitId, path + str(i + 1) + "\\split.json", dictionaryQual=dictionaryQual)
            else:
                Regional.setupRegionals(splitId)
                initializeSplit(splitId, path + str(i + 1) + "\\split.json")

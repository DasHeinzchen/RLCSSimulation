import Globals
import json
import os
import structure.Split as Split
from ranking import Ranking


class Season:
    def __init__(self, seasonId):
        self._id = seasonId
        self._current = False
        self._currentSplit = ""
        self._upcomingSplits = []

        self.loadData()

    def loadData(self):
        with open(Globals.settings["path"] + "seasons\\" + self._id + "\\season.json", "r") as seasonFile:
            dictionary = json.load(seasonFile)

            self._current = dictionary["current"]
            self._currentSplit = dictionary["currentSplit"]
            self._upcomingSplits = dictionary["upcomingSplits"]

            seasonFile.close()

        return self

    def saveData(self):
        with open(Globals.settings["path"] + "seasons\\" + self._id + "\\season.json", "w") as seasonFile:
            dictionary = {
                "current": self._current,
                "currentSplit": self._currentSplit,
                "upcomingSplits": self._upcomingSplits
            }

            seasonFile.write(json.dumps(dictionary, indent=5))
            seasonFile.close()

    def start(self):
        Split.Split(self._currentSplit).startSplit()

    @property
    def id(self):
        return self._id

    @property
    def current(self):
        return self._current

    @property
    def currentSplit(self):
        return self._currentSplit


def readSeasonsJson():
    with open(Globals.settings["path"] + "seasons\\seasons.json") as seasonsFile:
        seasonsJson = json.load(seasonsFile)

        for season in seasonsJson["seasons"]:
            if season["current"]:
                Globals.current_season = season["id"]

        seasonsFile.close()


def getSeasonById(id):
    return Season(id)


def initializeSeason(seasonId):
    with open(Globals.settings["path"] + "seasons\\" + seasonId + "\\season.json", "w") as seasonFile:
        dict = {
            "current": True,
            "currentSplit": seasonId + "_SPL1",
            "upcomingSplits": [seasonId + "_SPL2", seasonId + "_SPL3"]
        }
        seasonFile.write(json.dumps(dict, indent=5))

    Globals.current_season = seasonId


def setupSeason(dictionaryQual):
    seasonId = "S"
    with open(Globals.settings["path"] + "seasons\\seasons.json") as seasonsFile:
        seasonsJson = json.load(seasonsFile)
        for season in seasonsJson["seasons"]:
            season["current"] = False

        seasonId += str(len(seasonsJson["seasons"]) + 1)
        seasonsJson["seasons"].append({"id": seasonId, "current": True})
        seasonsFile.close()

        with open(Globals.settings["path"] + "seasons\\seasons.json", "w") as seasonsFile:
            seasonsFile.write(json.dumps(seasonsJson, indent=5))
            seasonsFile.close()

    try:
        os.mkdir(Globals.settings["path"] + "seasons\\" + seasonId)
    except OSError:
        print("Creation of the Season directory failed")
    else:
        try:
            os.mkdir(Globals.settings["path"] + "seasons\\" + seasonId + "\\rankings")
        except OSError:
            print("Creation of the Season Rankings directory failed")
        else:
            for region in Globals.regions:
                ranking = open(Globals.settings["path"] + "seasons\\" + seasonId + "\\rankings\\" + region + ".json",
                               "a")
                ranking.write(json.dumps(Ranking.emptyRankingTable(), indent=5))
                ranking.close()
            ranking = open(Globals.settings["path"] + "seasons\\" + seasonId + "\\rankings\\" + "worlds_spots.json",
                           "a")
            ranking.write(json.dumps(Ranking.emptyRankingTable(), indent=5))
            ranking.close()
        open(Globals.settings["path"] + "seasons\\" + seasonId + "\\season.json", "a").close()
        Split.setupSplits(seasonId, dictionaryQual)

    initializeSeason(seasonId)

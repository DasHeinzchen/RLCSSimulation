import Globals
import json
import os
import structure.Split as Split

class Season:
    def __init__(self, seasonId):
        self._id = seasonId
        self._current = False
        self._currentSplit = ""

        self.loadData()

    def loadData(self):
        with open(Globals.settings["path"] + "seasons\\" + self._id + "\\season.json", "r") as seasonFile:
            dictionary = json.load(seasonFile)

            self._current = dictionary["current"]
            self._currentSplit = dictionary["currentSplit"]

        return self

    def saveData(self):
        with open(Globals.settings["path"] + "seasons\\" + self._id + "\\season.json", "w") as seasonFile:
            dictionary = {
                "current": self._current,
                "currentSplit": self._currentSplit
            }

            seasonFile.write(json.dumps(dictionary, indent=5))

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
            "currentSplit": seasonId + "_SPL1"
        }
        seasonFile.write(json.dumps(dict, indent=5))

    Globals.current_season = seasonId


def setupSeason():
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
        open(Globals.settings["path"] + "seasons\\" + seasonId + "\\season.json", "a").close()
        Split.setupSplits(seasonId)

    initializeSeason(seasonId)

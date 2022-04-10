import Globals
import json
import os
import structure.Split as Split

class Season:
    def __init__(self, id="", current=False):
        self._dict = {}
        self._id = id
        self._current = current
        self._splits = ["", "", ""]

    def loadData(self):
        if not os.path.isfile(Globals.settings["path"] + "seasons\\" + self._id + "\\" + self._id + ".json"):
            file = open(Globals.settings["path"] + "seasons\\" + self._id + "\\" + self._id + ".json", "a")
            file.write("{}")
            file.close()
        else:
            file = open(Globals.settings["path"] + "seasons\\" + self._id + "\\" + self._id + ".json")
            self._dict = json.load(file)

            for i in range(len(self._dict["splits"])):
                self._splits[i] = self._dict["splits"][i]["id"]
            file.close()

    def saveData(self):
        # Loading Values to dict
        list=[]
        for i in range(len(self._splits)):
            list.append({"id": self._splits[i]})
        self._dict.update({
            "splits": list
        })

        file = open(Globals.settings["path"] + "seasons\\" + self._id + "\\" + self._id + ".json", "w")
        file.write(json.dumps(self._dict, indent=5))
        file.close()

    def addSplitId(self, i, splitId):
        self._splits[i] = splitId

    @property
    def id(self):
        return self._id

    @property
    def current(self):
        return self._current

    @property
    def splits(self):
        return self._splits


def readSeasonsJson():
    with open(Globals.settings["path"] + "seasons\\seasons.json") as seasonsFile:
        seasonsJson = json.load(seasonsFile)
        for season in seasonsJson["seasons"]:
            try:
                os.mkdir(Globals.settings["path"] + "seasons\\" + season["id"])
            except:
                print("season directory vorhanden")

            if season["current"]:
                Globals.current_season = season["id"]

                break

        seasonsFile.close()

def getSeasonById(id):
    season = Season(id=id)
    season.loadData()
    return season

def initializeSeason(seasonId):
    with open(Globals.settings["path"] + "seasons\\" + seasonId + "\\season.json", "w") as seasonFile:
        dict = {
            "current": True,
            "currentSplit": seasonId + "_SPL1"
        }
        seasonFile.write(json.dumps(dict, indent=5))

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

import Globals
import json

import Team


class RTable:
    def __init__(self, tableId):
        self._id = tableId
        self._ranking = []
        self._items = {}
        self._currentEvent = 0

        self.loadData()

    def loadData(self):
        ids = self._id.split("_")
        if len(ids) == 3 and ids[-1] == "SPOTS":
            rankingFile = open(Globals.settings["path"] + "seasons\\" + ids[1] + "\\rankings\\worlds_spots.json", "r")
        elif len(ids) == 3:
            rankingFile = open(Globals.settings["path"] + "seasons\\" + ids[1] + "\\rankings\\" + ids[2] + ".json", "r")
        else:
            rankingFile = open(Globals.settings["path"] + "seasons\\" + ids[1] + "\\" + ids[2] + "\\" + ids[3] +
                               "rankings.json", "r")
        rankingDict = json.load(rankingFile)
        rankingFile.close()

        self._ranking = rankingDict["ranking"]
        self._currentEvent = rankingDict["currentEvent"]
        for key in rankingDict["items"]:
            self._items.update({key: RTItem(key).load(rankingDict["items"][key])})

    def saveData(self):
        ids = self._id.split("_")
        if len(ids) == 3 and ids[-1] == "SPOTS":
            rankingFile = open(Globals.settings["path"] + "seasons\\" + ids[1] + "\\rankings\\worlds_spots.json", "w")
        elif len(ids) == 3:
            rankingFile = open(Globals.settings["path"] + "seasons\\" + ids[1] + "\\rankings\\" + ids[2] + ".json", "w")
        else:
            rankingFile = open(Globals.settings["path"] + "seasons\\" + ids[1] + "\\" + ids[2] + "\\" + ids[3] +
                               "rankings.json", "w")

        items = {}
        for key in self._items:
            items.update({key: self._items[key].toDict()})
        rankingDict = {
            "currentEvent": self._currentEvent,
            "ranking": self._ranking,
            "items": items
        }

        rankingFile.write(json.dumps(rankingDict, indent=5))
        rankingFile.close()

    def addPoints(self, team, points):
        if team in self._ranking:
            item = self._items[team]
        else:
            self._ranking.append(team)
            item = RTItem(team)
        item.addPoints(points, self._currentEvent)
        self._items.update({team: item})

    def nextEvent(self):
        self._currentEvent += 1

    def rank(self):
        for i in range(len(self._ranking) - 1):
            for j in range(0, len(self._ranking) - i - 1):
                if self._items[self._ranking[j]].points < self._items[self._ranking[j+1]].points:
                    self._ranking[j], self._ranking[j+1] = self._ranking[j+1], self._ranking[j]

    def topTeams(self, top=1, bot=1):
        teams = []
        if top >= bot:
            for i in range(bot-1, top):
                teams.append(Team.getTeamById(self._ranking[i]))
        else:
            ids = self._ranking[(bot-1):]
            for id in ids:
                teams.append(Team.getTeamById(id))
        return teams


class RTItem:
    def __init__(self, team):
        self._team = team
        self._points = 0
        self._eventPoints = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def addPoints(self, points, event):
        self._points += points
        self._eventPoints[event] = points

    def toDict(self):
        return {
            "points": self._points,
            "eventPoints": self._eventPoints
        }

    def load(self, dict):
        self._points = dict["points"]
        self._eventPoints = dict["eventPoints"]
        return self

    @property
    def points(self):
        return self._points


def emptyRankingTable():
    return {
        "currentEvent": 0,
        "ranking": [],
        "items": {}
    }


def addPoints(placements, id, factor=1):
    ids = id.split("_")
    if int(ids[1][-1]) == 1:
        table = RTable("RANK_" + ids[0] + "_" + ids[2])
        table.addPoints(placements["1"], (300 * factor) + 1)
        table.addPoints(placements["2"], 250 * factor)
        for i in range(2):
            table.addPoints(placements["3-4"][i], 200 * factor)
            table.addPoints(placements["15-16"][i], 40 * factor)
        for i in range(3):
            table.addPoints(placements["9-11"][i], 110 * factor)
            table.addPoints(placements["12-14"][i], 70 * factor)
        for i in range(4):
            table.addPoints(placements["5-8"][i], 150 * factor)

    table.rank()
    table.nextEvent()
    table.saveData()


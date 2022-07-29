import EventHandler
import Team
import Log


class MatchFinishedEvent:
    def __init__(self):
        self.__eventhandler = []

    def __iadd__(self, Eventhandler):
        Log.new("i", "Adding Listener to MatchFinished")
        self.__eventhandler.append(Eventhandler)
        return self

    def __isub__(self, Eventhandler):
        Log.new("i", "Removing Listener from MatchFinished")
        self.__eventhandler.remove(Eventhandler)
        return self

    def __call__(self, matchObj):
        Log.new("i", "Calling MatchFinished")
        for handler in self.__eventhandler:
            handler(matchObj)


class Match:
    def __init__(self, matchDict):
        Log.new("i", "Generating new Match Object")
        self.id = matchDict["id"]
        self.current = matchDict["current"]
        self.team1 = matchDict["team1"]
        self.score1 = matchDict["score1"]
        self.team2 = matchDict["team2"]
        self.score2 = matchDict["score2"]
        self.winner = matchDict["winner"]

    def asDict(self):
        Log.new("i", "Converting Match object to dict")
        return {
            "id": self.id,
            "current": self.current,
            "team1": self.team1,
            "score1": self.score1,
            "team2": self.team2,
            "score2": self.score2,
            "winner": self.winner
        }

    @staticmethod
    def newMatch(matchId):
        Log.new("i", "Creating new Match '" + matchId + "'")
        matchDict = {
            "id": matchId,
            "current": False,
            "team1": "_tbd",
            "score1": 0,
            "team2": "_tbd",
            "score2": 0,
            "winner": 0
        }

        return Match(matchDict)


class OldMatch:
    @staticmethod
    def initialize(matchId):
        return {
            "id": matchId,
            "current": False,
            "score1": 0,
            "score2": 0,
            "winner": 0
        }

    @staticmethod
    def submitScore(score1, score2, matchDict):
        matchDict["score1"] = score1
        matchDict["score2"] = score2
        matchDict["current"] = False
        if score1 > score2: matchDict["winner"] = 1
        elif score1 < score2: matchDict["winner"] = 2

        return matchDict

    @staticmethod
    def start(matchDict):
        matchDict["current"] = True
        return matchDict


class SeriesFinishedEvent:
    def __init__(self):
        self.__eventhandler = []

    def __iadd__(self, Eventhandler):
        Log.new("i", "Adding Listener to SeriesFinished")
        self.__eventhandler.append(Eventhandler)
        return self

    def __isub__(self, Eventhandler):
        Log.new("i", "Removing Listener from SeriesFinished")
        self.__eventhandler.remove(Eventhandler)
        return self

    def __call__(self, seriesObj):
        Log.new("i", "Calling SeriesFinished")
        for handler in self.__eventhandler:
            handler(seriesObj)


class Series:
    def __init__(self, seriesDict):
        Log.new("i", "Generating new Series Object")
        Log.new("e", "Matches not implemented")
        self.id = seriesDict["id"]
        self.current = seriesDict["current"]
        self.currentMatch = seriesDict["currentMatch"]
        self.upcomingMatches = seriesDict["upcomingMatches"]
        self.bestOf = seriesDict["bestOf"]
        self.teams = seriesDict["teams"]
        self.placements = seriesDict["placements"]
        # TODO matches
        self.setFinishedEvent = SetFinishedEvent()

    def asDict(self):
        Log.new("i", "Converting Series object to dict")
        Log.new("e", "Matches not implemented")
        return {
            "id": self.id,
            "current": self.current,
            "currentMatch": self.currentMatch,
            "upcomingMatches": self.upcomingMatches,
            "bestOf": self.bestOf,
            "teams": self.teams,
            "placements": self.placements
            # TODO matches
        }

    @staticmethod
    def newSet(seriesId,  seriesBo):
        Log.new("i", "Creating new Series '" + seriesId + "' with bo '" + seriesBo + "'")
        Log.new("e", "Matches not implemented")
        seriesDict = {
            "id": seriesId,
            "current": False,
            "currentMatch": "",
            "upcomingMatches": [],
            "bestOf": seriesBo,
            "teams": ["_tbd", "_tbd"],
            "placements": {
                "winner": "_tbd",
                "loser": "_tbd"
            }
            # TODO matches
        }
        for i in range(int((seriesBo + 1) / 2)):
            seriesDict["upcomingMatches"].append("s" + str(i + 1))

        return Series(seriesDict)


class OldSeries:
    @staticmethod
    def initialize(seriesId, bo):
        matches = []
        for i in range(int((bo + 1) / 2)):
            if i == 0: matches.append(OldMatch.initialize(seriesId + "_M1"))
            else: matches.append(OldMatch.initialize(seriesId + "_M" + str(i + 1)))

        return {
            "id": seriesId,
            "current": False,
            "currentMatch": -1,
            "bestOf": bo,
            "team1": Team.placeholder.id,
            "score1": 0,
            "team2": Team.placeholder.id,
            "score2": 0,
            "winner": 0,
            "matches": matches
        }

    @staticmethod
    def submitScore(seriesDict, matchDict):
        seriesDict["matches"][seriesDict["currentMatch"]] = matchDict
        if matchDict["winner"] == 1: seriesDict["score1"] += 1
        elif matchDict["winner"] == 2: seriesDict["score2"] += 1

        if (seriesDict["score1"] >= seriesDict["score2"]
            and not len(seriesDict["matches"]) - (seriesDict["currentMatch"] + 1)
                    == ((seriesDict["bestOf"] + 1) / 2) - seriesDict["score1"])\
                or (seriesDict["score1"] <= seriesDict["score2"]
                    and not len(seriesDict["matches"]) - (seriesDict["currentMatch"] + 1)
                            == ((seriesDict["bestOf"] + 1) / 2) - seriesDict["score2"]):
            seriesDict["matches"].append(OldMatch.initialize(seriesDict["id"] + "_M" +
                                                             str(len(seriesDict["matches"]) + 1)))

        if seriesDict["score1"] == int((seriesDict["bestOf"] + 1) / 2): seriesDict["winner"] = 1
        elif seriesDict["score2"] == int((seriesDict["bestOf"] + 1) / 2): seriesDict["winner"] = 2

        if seriesDict["winner"] == 0:
            seriesDict["currentMatch"] += 1
            seriesDict["matches"][seriesDict["currentMatch"]]["current"] = True
            return seriesDict, False
        else:
            return seriesDict, True

    @staticmethod
    def start(seriesDict):
        seriesDict["current"] = True
        seriesDict["currentMatch"] = 0
        seriesDict["matches"][0] = OldMatch.start(seriesDict["matches"][0])
        return seriesDict

    @staticmethod
    def skip(seriesDict):
        if seriesDict["team1"] == "_bye":
            seriesDict["winner"] = 2
        elif seriesDict["team2"] == "_bye":
            seriesDict["winner"] = 1

        seriesDict["current"] = False
        seriesDict["matches"] = []
        return seriesDict


class SetFinishedEvent:
    def __init__(self):
        self.__eventhandler = []

    def __iadd__(self, Eventhandler):
        Log.new("i", "Adding Listener to SetFinished")
        self.__eventhandler.append(Eventhandler)
        return self

    def __isub__(self, Eventhandler):
        Log.new("i", "Removing Listener from SetFinished")
        self.__eventhandler.remove(Eventhandler)
        return self

    def __call__(self, setObj):
        Log.new("i", "Calling SetFinished")
        for handler in self.__eventhandler:
            handler(setObj)


class Set:
    def __init__(self, setDict):
        Log.new("i", "Generating new Set Object")
        Log.new("e", "Series not implemented")
        self.id = setDict["id"]
        self.current = setDict["current"]
        self.currentSeries = setDict["currentSeries"]
        self.upcomingSeries = setDict["upcomingSeries"]
        self.bestOf = setDict["bestOf"]
        self.teams = setDict["teams"]
        self.placements = setDict["placements"]
        # TODO series
        self.setFinishedEvent = SetFinishedEvent()

    def asDict(self):
        Log.new("i", "Converting Set object to dict")
        Log.new("e", "Series not implemented")
        return {
            "id": self.id,
            "current": self.current,
            "currentSeries": self.currentSeries,
            "upcomingSeries": self.upcomingSeries,
            "bestOf": self.bestOf,
            "teams": self.teams,
            "placements": self.placements
        }

    @staticmethod
    def newSet(setId, setBo, seriesBo):
        Log.new("i", "Creating new Set '" + setId + "' with bo '" + setBo + "'")
        Log.new("e", "Series not implemented")
        setDict = {
            "id": setId,
            "current": False,
            "currentSeries": "",
            "upcomingSeries": [],
            "bestOf": setBo,
            "teams": ["_tbd", "_tbd"],
            "placements": {
                "winner": "_tbd",
                "loser": "_tbd"
            }
            # TODO series
        }
        for i in range(int((setBo + 1) / 2)):
            setDict["upcomingSeries"].append("s" + str(i + 1))

        return Set(setDict)

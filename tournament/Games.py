import EventHandler
import Team


class Match:
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


class Series:
    @staticmethod
    def initialize(seriesId, bo):
        matches = []
        for i in range(int((bo + 1) / 2)):
            if i == 0: matches.append(Match.initialize(seriesId + "_M1"))
            else: matches.append(Match.initialize(seriesId + "_M" + str(i + 1)))

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
            seriesDict["matches"].append(Match.initialize(seriesDict["id"] + "_M" +
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
        seriesDict["matches"][0] = Match.start(seriesDict["matches"][0])
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

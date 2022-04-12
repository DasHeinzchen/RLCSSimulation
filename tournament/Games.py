import Team


class Match:
    @staticmethod
    def initialize(matchId, current):
        return {
            "id": matchId,
            "current": current,
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


class Series:
    @staticmethod
    def initialize(seriesId, current, bo):
        matches = []
        for i in range(int((bo + 1) / 2)):
            if i == 0: matches.append(Match.initialize(seriesId + "_M1", current))
            else: matches.append(Match.initialize(seriesId + "_M" + str(i + 1), False))

        return {
            "id": seriesId,
            "current": current,
            "currentMatch": 0,
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
                                                          str(len(seriesDict["matches"]) + 1), False))

        if seriesDict["score1"] == 4: seriesDict["winner"] = 1
        elif seriesDict["score2"] == 4: seriesDict["winner"] = 2

        if seriesDict["winner"] == 0:
            seriesDict["currentMatch"] += 1
            seriesDict["matches"][seriesDict["currentMatch"]]["current"] = True
            return seriesDict, False
        else:
            return seriesDict, True

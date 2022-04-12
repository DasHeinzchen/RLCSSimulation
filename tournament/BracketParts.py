from tournament import Games

def submitScore(partDict, seriesDict, condition):
    partDict[partDict["currentSeries"]] = seriesDict
    if condition:
        partDict[partDict["currentSeries"]]["current"] = False
        if partDict["type"] == "FIN":
            partDict = submitSetScore(partDict, seriesDict)
        if len(partDict["upcomingSeries"]) > 0:
            partDict = startPart(partDict)
            return partDict, False
        else:
            return partDict, True
    else:
        return partDict, False


def startPart(partDict):
    partDict["current"] = True
    partDict["currentSeries"] = partDict["upcomingSeries"].pop(0)
    partDict[partDict["currentSeries"]] = Games.Series.start(partDict[partDict["currentSeries"]])
    return partDict


def submitSetScore(partDict, seriesDict):
    if seriesDict["winner"] == 1: partDict["setScore1"] += 1
    elif seriesDict["winner"] == 2: partDict["setScore2"] += 1
    series = str(int(partDict["currentSeries"][-1]) + 1)

    if (partDict["setScore1"] >= partDict["setScore2"]
            and not len(partDict["upcomingSeries"]) == ((partDict["setBestOf"] + 1) / 2) - partDict["setScore1"])\
        or (partDict["setScore1"] <= partDict["setScore2"]
            and not len(partDict["upcomingSeries"]) == ((partDict["setBestOf"] + 1) / 2) - partDict["setScore2"]):
        partDict["upcomingSeries"].append("fin" + series)
        partDict.update({"fin" + series:
                             Games.Series.initialize(partDict["id"] + "_" + series, partDict["bestOf"])})

    if partDict["setScore1"] == int((partDict["setBestOf"] + 1) / 2): partDict["setWinner"] = 1
    elif partDict["setScore2"] == int((partDict["setBestOf"] + 1) / 2): partDict["setWinner"] = 2

    return partDict


class QuarterFinals:
    @staticmethod
    def initialize(partId, bo):
        return {
            "id": partId,
            "type": "QF",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["qf1", "qf2", "qf3", "qf4"],
            "bestOf": bo,
            "teams": [],
            "qf1": Games.Series.initialize(partId + "_1", bo),
            "qf2": Games.Series.initialize(partId + "_2", bo),
            "qf3": Games.Series.initialize(partId + "_3", bo),
            "qf4": Games.Series.initialize(partId + "_4", bo)
        }


class SemiFinals:
    @staticmethod
    def initialize(partId, bo):
        return {
            "id": partId,
            "type": "SF",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["sf1", "sf2"],
            "bestOf": bo,
            "teams": [],
            "sf1": Games.Series.initialize(partId + "_1", bo),
            "sf2": Games.Series.initialize(partId + "_2", bo)
        }


class Finals:
    @staticmethod
    def initialize(partId, bo, setBo):
        dictionary = {
            "id": partId,
            "type": "FIN",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": [],
            "bestOf": bo,
            "setBestOf": setBo,
            "setScore1": 0,
            "setScore2": 0,
            "setWinner": 0,
            "teams": []
        }
        for i in range(int((setBo + 1) / 2)):
            dictionary.update({
                "fin" + str(i+1): Games.Series.initialize(partId + "_" + str(i+1), bo)
            })
            dictionary["upcomingSeries"].append("fin" + str(i+1))

        return dictionary

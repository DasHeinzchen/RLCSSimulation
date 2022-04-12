from tournament import Games

def submitScore(partDict, seriesDict, condition):
    partDict[partDict["currentSeries"]] = seriesDict
    if condition:
        if len(partDict["upcomingSeries"]) > 0:
            partDict["currentSeries"] = partDict["upcomingSeries"].pop(0)
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


class QuarterFinals:
    @staticmethod
    def initialize(partId, bo):
        return {
            "id": partId,
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
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["sf1", "sf2"],
            "bestOf": bo,
            "teams": [],
            "sf1": Games.Series.initialize(partId + "_1", bo),
            "sf2": Games.Series.initialize(partId + "_2", bo)
        }

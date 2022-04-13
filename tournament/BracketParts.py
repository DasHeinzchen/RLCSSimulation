from tournament import Games

def submitScore(partDict, seriesDict, condition):
    partDict[partDict["currentSeries"]] = seriesDict
    if condition:
        if partDict["type"] == "FIN":
            partDict = submitSetScore(partDict, seriesDict)
        partDict = checkResults(partDict)
        partDict[partDict["currentSeries"]]["current"] = False
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
        partDict["fin" + series]["team1"] = partDict["teams"][0]
        partDict["fin" + series]["team2"] = partDict["teams"][1]

    if partDict["setScore1"] == int((partDict["setBestOf"] + 1) / 2): partDict["setWinner"] = 1
    elif partDict["setScore2"] == int((partDict["setBestOf"] + 1) / 2): partDict["setWinner"] = 2

    return partDict

def checkResults(partDict):
    if partDict["type"] == "QF":
        return QuarterFinals.checkResults(partDict)
    elif partDict["type"] == "SF":
        return SemiFinals.checkResults(partDict)
    elif partDict["type"] == "FIN":
        return Finals.checkResults(partDict)


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
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "winningTeams": ["_tbd", "_tbd", "_tbd", "_tbd"],
            "losingTeams": ["_tbd", "_tbd", "_tbd", "_tbd"],
            "qf1": Games.Series.initialize(partId + "_1", bo),
            "qf2": Games.Series.initialize(partId + "_2", bo),
            "qf3": Games.Series.initialize(partId + "_3", bo),
            "qf4": Games.Series.initialize(partId + "_4", bo)
        }

    @staticmethod
    def addTeams(partDict):
        partDict["qf1"]["team1"] = partDict["teams"][0]
        partDict["qf1"]["team2"] = partDict["teams"][7]
        partDict["qf2"]["team1"] = partDict["teams"][1]
        partDict["qf2"]["team2"] = partDict["teams"][6]
        partDict["qf3"]["team1"] = partDict["teams"][2]
        partDict["qf3"]["team2"] = partDict["teams"][5]
        partDict["qf4"]["team1"] = partDict["teams"][3]
        partDict["qf4"]["team2"] = partDict["teams"][4]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict[partDict["currentSeries"]]["winner"] == 1:
            partDict["winningTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team1"]
            partDict["losingTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team2"]
        elif partDict[partDict["currentSeries"]]["winner"] == 2:
            partDict["winningTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team2"]
            partDict["losingTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team1"]
        return partDict


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
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
            "winningTeams": ["_tbd", "_tbd"],
            "losingTeams": ["_tbd", "_tbd"],
            "sf1": Games.Series.initialize(partId + "_1", bo),
            "sf2": Games.Series.initialize(partId + "_2", bo)
        }

    @staticmethod
    def addTeams(partDict):
        partDict["sf1"]["team1"] = partDict["teams"][0]
        partDict["sf1"]["team2"] = partDict["teams"][3]
        partDict["sf2"]["team1"] = partDict["teams"][1]
        partDict["sf2"]["team2"] = partDict["teams"][2]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict[partDict["currentSeries"]]["winner"] == 1:
            partDict["winningTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team1"]
            partDict["losingTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team2"]
        elif partDict[partDict["currentSeries"]]["winner"] == 2:
            partDict["winningTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team2"]
            partDict["losingTeams"][int(partDict["currentSeries"][-1]) - 1]\
                = partDict[partDict["currentSeries"]]["team1"]
        return partDict


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
            "teams": ["_tbd", "_tbd"],
            "winningTeams": "_tbd",
            "losingTeams": "_tbd"
        }
        for i in range(int((setBo + 1) / 2)):
            dictionary.update({
                "fin" + str(i+1): Games.Series.initialize(partId + "_" + str(i+1), bo)
            })
            dictionary["upcomingSeries"].append("fin" + str(i+1))

        return dictionary

    @staticmethod
    def addTeams(partDict):
        if not partDict["currentSeries"] == "":
            partDict[partDict["currentSeries"]]["team1"] = partDict["teams"][0]
            partDict[partDict["currentSeries"]]["team2"] = partDict["teams"][1]
        for series in partDict["upcomingSeries"]:
            partDict[series]["team1"] = partDict["teams"][0]
            partDict[series]["team2"] = partDict["teams"][1]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict["setWinner"] == 1:
            partDict["winningTeams"] \
                = partDict[partDict["currentSeries"]]["team1"]
            partDict["losingTeams"] \
                = partDict[partDict["currentSeries"]]["team2"]
        elif partDict[partDict["currentSeries"]]["winner"] == 2:
            partDict["winningTeams"] \
                = partDict[partDict["currentSeries"]]["team2"]
            partDict["losingTeams"] \
                = partDict[partDict["currentSeries"]]["team1"]
        return partDict

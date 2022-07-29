from tournament import Games
import Log


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
    partDict[partDict["currentSeries"]] = Games.OldSeries.start(partDict[partDict["currentSeries"]])
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
                             Games.OldSeries.initialize(partDict["id"] + "_" + series, partDict["bestOf"])})
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
    elif partDict["type"] == "SWR1":
        return SwissRound1.checkResults(partDict)
    elif partDict["type"] == "SWR2":
        return SwissRound2.checkResults(partDict)
    elif partDict["type"] == "SWR3":
        return SwissRound3.checkResults(partDict)
    elif partDict["type"] == "SWR4":
        return SwissRound4.checkResults(partDict)
    elif partDict["type"] == "SWR5":
        return SwissRound5.checkResults(partDict)
    elif partDict["type"] == "RO16":
        return RoundOf16.checkResults(partDict)
    elif partDict["type"] == "RO32":
        return RoundOf32.checkResults(partDict)


def seeding(bracketDict, partDict):
    if partDict["type"] == "SWR1":
        return SwissRound1.seeding(bracketDict, partDict)
    elif partDict["type"] == "SWR2":
        return SwissRound2.seeding(bracketDict, partDict)
    elif partDict["type"] == "SWR3":
        return SwissRound3.seeding(bracketDict, partDict)
    elif partDict["type"] == "SWR4":
        return SwissRound4.seeding(bracketDict, partDict)
    elif partDict["type"] == "SWR5":
        return SwissRound5.seeding(bracketDict, partDict)
    else:
        return bracketDict


class BracketPartFinishedEvent:
    def __init__(self):
        self.__eventhandler = []

    def __iadd__(self, Eventhandler):
        Log.new("i", "Adding Listener to BracketPartFinished")
        self.__eventhandler.append(Eventhandler)
        return self

    def __isub__(self, Eventhandler):
        Log.new("i", "Removing Listener from BracketPartFinished")
        self.__eventhandler.remove(Eventhandler)
        return self

    def __call__(self, bracketPartObj):
        Log.new("i", "Calling BracketPartFinished")
        for handler in self.__eventhandler:
            handler(bracketPartObj)


class BracketPart:
    def __init__(self, partDict):
        Log.new("i", "Generating new Bracket Part Object")
        Log.new("e", "Sets not implemented")

        self.id = partDict["id"]
        self.type = partDict["type"]
        self.current = partDict["current"]
        self.currentSet = partDict["currentSet"]
        self.upcomingSets = partDict["upcomingSets"]
        self.teams = partDict["teams"]
        self.placements = partDict["placements"]
        # TODO series
        self.bracketPartFinishedEvent = BracketPartFinishedEvent()

    def asDict(self):
        Log.new("i", "Converting Bracket Part object to dict")
        Log.new("e", "Sets not implemented")
        return {
            "id": self.id,
            "type": self.type,
            "current": self.current,
            "currentSet": self.currentSet,
            "upcomingSets": self.upcomingSets,
            "teams": self.teams,
            "placements": self.placements
            # TODO series
        }

    @staticmethod
    def newBracketPart(partId, type, setBo, seriesBo):
        Log.new("i", "Creating new Bracket Part '" + partId + "' with type '" + type + "'")
        partDict = {
            "id": partId,
            "type": type,
            "current": False,
            "currentSet": "",
            "upcomingSets": [],
            "teams": [],
            "placements": {},
            "series": {}
        }

        if type == "RO2":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["set"],
                "teams": ["_tbd", "_tbd"],
                "placements": {
                    "winner": "_tbd",
                    "loser": "_tbd"
                }
                # TODO series
            })
        elif type == "RO4":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["set1, set2"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "winningTeams": ["_tbd", "_tbd"],
                    "losingTeams": ["_tbd", "_tbd"]
                }
                # TODO series
            })
        elif type == "RO8":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["set1", "set2", "set3", "set4"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "winningTeams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                    "losingTeams": ["_tbd", "_tbd", "_tbd", "_tbd"]
                }
                # TODO series
            })
        elif type == "RO16":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["set1", "set2", "set3", "set4", "set5", "set6", "set7", "set8"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "winningTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                    "losingTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
                }
                # TODO series
            })
        elif type == "RO32":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["set1", "set2", "set3", "set4", "set5", "set6", "set7", "set8",
                                 "set9", "set10", "set11", "set12", "set13", "set14", "set15", "set16"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "winningTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                                     "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                    "losingTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                                    "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
                }
                # TODO series
            })
        elif type == "SWR1":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["set1", "set2", "set3", "set4", "set5", "set6", "set7", "set8"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "winningTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                        "3-0":  [],
                        "3-1": [],
                        "3-2": []
                    },
                    "losingTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    }
                }
                # TODO series
            })
        elif type == "SWR2":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["h1", "l1", "h2", "l2", "h3", "l3", "h4", "l4"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "winningTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": []
                    },
                    "midTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": [],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    },
                    "losingTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    }
                }
                # TODO series
            })
        elif type == "SWR3":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["m1", "m2", "m3", "m4", "l1", "h1", "l2", "h2"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "qualTeams": {
                        "teams": ["_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": []
                    },
                    "elimTeams": {
                        "teams": ["_tbd", "_tbd"],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    },
                    "highTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": [],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    },
                    "lowTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": [],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    }
                }
                # TODO series
            })
        elif type == "SWR4":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["h1", "l1", "h2", "l2", "h3", "l3"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                          "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "qualTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": []
                    },
                    "elimTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd"],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    },
                    "midTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": [],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    }
                }
                # TODO series
            })
        elif type == "SWR5":
            Log.new("e", "sets not implemented")
            partDict.update({
                "upcomingSets": ["set1", "set2", "set3"],
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "placements": {
                    "qualTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd"],
                        "3-0": [],
                        "3-1": [],
                        "3-2": []
                    },
                    "elimTeams": {
                        "teams": ["_tbd", "_tbd", "_tbd"],
                        "0-3": [],
                        "1-3": [],
                        "2-3": []
                    }
                }
                # TODO series
            })

        return BracketPart(partDict)


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
            "qf1": Games.OldSeries.initialize(partId + "_1", bo),
            "qf2": Games.OldSeries.initialize(partId + "_2", bo),
            "qf3": Games.OldSeries.initialize(partId + "_3", bo),
            "qf4": Games.OldSeries.initialize(partId + "_4", bo)
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
            "sf1": Games.OldSeries.initialize(partId + "_1", bo),
            "sf2": Games.OldSeries.initialize(partId + "_2", bo)
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
                "fin" + str(i+1): Games.OldSeries.initialize(partId + "_" + str(i + 1), bo)
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


class SwissRound1:
    @staticmethod
    def initialize(partId, bo):
        dictionary = {
            "id": partId,
            "type": "SWR1",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"],
            "bestOf": bo,
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "winningTeams": {
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "3-0":  [],
                "3-1": [],
                "3-2": []
            },
            "losingTeams": {
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "0-3": [],
                "1-3": [],
                "2-3": []
            }
        }
        for i in range(8):
            dictionary.update({"s" + str(i+1): Games.OldSeries.initialize(partId + "_SER" + str(i + 1), bo)})

        return dictionary

    @staticmethod
    def addTeams(partDict):
        for i in range(8):
            partDict["s" + str(i+1)]["team1"] = partDict["teams"][i]
            partDict["s" + str(i+1)]["team2"] = partDict["teams"][15-i]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict["bestOf"] == 5:
            if partDict[partDict["currentSeries"]]["winner"] == 1:
                if partDict[partDict["currentSeries"]]["score2"] == 0:
                    partDict["winningTeams"]["3-0"].append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["losingTeams"]["0-3"].append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["score2"] == 1:
                    partDict["winningTeams"]["3-1"].append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["losingTeams"]["1-3"].append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["score2"] == 2:
                    partDict["winningTeams"]["3-2"].append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["losingTeams"]["2-3"].append(partDict[partDict["currentSeries"]]["team2"])
            elif partDict[partDict["currentSeries"]]["winner"] == 2:
                if partDict[partDict["currentSeries"]]["score1"] == 0:
                    partDict["winningTeams"]["3-0"].append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["losingTeams"]["0-3"].append(partDict[partDict["currentSeries"]]["team1"])
                elif partDict[partDict["currentSeries"]]["score1"] == 1:
                    partDict["winningTeams"]["3-1"].append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["losingTeams"]["1-3"].append(partDict[partDict["currentSeries"]]["team1"])
                elif partDict[partDict["currentSeries"]]["score1"] == 2:
                    partDict["winningTeams"]["3-2"].append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["losingTeams"]["2-3"].append(partDict[partDict["currentSeries"]]["team1"])
        else:
            print("unsupported best Of for Swiss at BracketPart SwissRound1")

        partDict["winningTeams"]["teams"] = partDict["winningTeams"]["3-0"]\
                                            + partDict["winningTeams"]["3-1"]\
                                            + partDict["winningTeams"]["3-2"]
        for i in range(8 - len(partDict["winningTeams"]["teams"])):
            partDict["winningTeams"]["teams"].append("_tbd")

        partDict["losingTeams"]["teams"] = partDict["losingTeams"]["2-3"] \
                                            + partDict["losingTeams"]["1-3"] \
                                            + partDict["losingTeams"]["0-3"]
        for i in range(8 - len(partDict["losingTeams"]["teams"])):
            partDict["losingTeams"]["teams"].append("_tbd")
        return partDict

    @staticmethod
    def seeding(bracketDict, partDict):
        teams = []
        for initialSeed in bracketDict["teams"]:
            for team in partDict["winningTeams"]["3-0"]:
                if initialSeed == team:
                    teams.append(team)
                    bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
                    break
        for initialSeed in bracketDict["teams"]:
            for team in partDict["winningTeams"]["3-1"]:
                if initialSeed == team:
                    teams.append(team)
                    bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
                    break
        for initialSeed in bracketDict["teams"]:
            for team in partDict["winningTeams"]["3-2"]:
                if initialSeed == team:
                    teams.append(team)
                    bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
                    break

        bracketDict["r1"]["winningTeams"]["teams"] = teams
        teams = []

        for initialSeed in bracketDict["teams"]:
            for team in partDict["losingTeams"]["2-3"]:
                if initialSeed == team:
                    teams.append(team)
                    bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1
                    break
        for initialSeed in bracketDict["teams"]:
            for team in partDict["losingTeams"]["1-3"]:
                if initialSeed == team:
                    teams.append(team)
                    bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
                    break
        for initialSeed in bracketDict["teams"]:
            for team in partDict["losingTeams"]["0-3"]:
                if initialSeed == team:
                    teams.append(team)
                    bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
                    break

        bracketDict["r1"]["losingTeams"]["teams"] = teams
        return bracketDict


class SwissRound2:
    @staticmethod
    def initialize(partId, bo):
        dictionary = {
            "id": partId,
            "type": "SWR2",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["h1", "l1", "h2", "l2", "h3", "l3", "h4", "l4"],
            "bestOf": bo,
            "teams": {
                "1-0": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "0-1": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
            },
            "winningTeams": {
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                "3-0": [],
                "3-1": [],
                "3-2": []
            },
            "midTeams": {
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "3-0": [],
                "3-1": [],
                "3-2": [],
                "0-3": [],
                "1-3": [],
                "2-3": []
            },
            "losingTeams": {
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                "0-3": [],
                "1-3": [],
                "2-3": []
            }
        }
        for i in range(4):
            dictionary.update({"h" + str(i+1): Games.OldSeries.initialize(partId + "_HI" + str(i + 1), bo)})
        for i in range(4):
            dictionary.update({"l" + str(i+1): Games.OldSeries.initialize(partId + "_LO" + str(i + 1), bo)})
        return dictionary

    @staticmethod
    def addTeams(partDict):
        for i in range(4):
            partDict["h" + str(i+1)]["team1"] = partDict["teams"]["1-0"][i]
            partDict["h" + str(i+1)]["team2"] = partDict["teams"]["1-0"][7-i]
            partDict["l" + str(i+1)]["team1"] = partDict["teams"]["0-1"][i]
            partDict["l" + str(i+1)]["team2"] = partDict["teams"]["0-1"][7-i]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict["bestOf"] == 5:
            if partDict["currentSeries"][0] == "h":
                if partDict[partDict["currentSeries"]]["winner"] == 1:
                    if partDict[partDict["currentSeries"]]["score2"] == 0:
                        partDict["winningTeams"]["3-0"].append(partDict[partDict["currentSeries"]]["team1"])
                        partDict["midTeams"]["0-3"].append(partDict[partDict["currentSeries"]]["team2"])
                    elif partDict[partDict["currentSeries"]]["score2"] == 1:
                        partDict["winningTeams"]["3-1"].append(partDict[partDict["currentSeries"]]["team1"])
                        partDict["midTeams"]["1-3"].append(partDict[partDict["currentSeries"]]["team2"])
                    elif partDict[partDict["currentSeries"]]["score2"] == 2:
                        partDict["winningTeams"]["3-2"].append(partDict[partDict["currentSeries"]]["team1"])
                        partDict["midTeams"]["2-3"].append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["winner"] == 2:
                    if partDict[partDict["currentSeries"]]["score1"] == 0:
                        partDict["winningTeams"]["3-0"].append(partDict[partDict["currentSeries"]]["team2"])
                        partDict["midTeams"]["0-3"].append(partDict[partDict["currentSeries"]]["team1"])
                    elif partDict[partDict["currentSeries"]]["score1"] == 1:
                        partDict["winningTeams"]["3-1"].append(partDict[partDict["currentSeries"]]["team2"])
                        partDict["midTeams"]["1-3"].append(partDict[partDict["currentSeries"]]["team1"])
                    elif partDict[partDict["currentSeries"]]["score1"] == 2:
                        partDict["winningTeams"]["3-2"].append(partDict[partDict["currentSeries"]]["team2"])
                        partDict["midTeams"]["2-3"].append(partDict[partDict["currentSeries"]]["team1"])
            if partDict["currentSeries"][0] == "l":
                if partDict[partDict["currentSeries"]]["winner"] == 1:
                    if partDict[partDict["currentSeries"]]["score2"] == 0:
                        partDict["midTeams"]["3-0"].append(partDict[partDict["currentSeries"]]["team1"])
                        partDict["losingTeams"]["0-3"].append(partDict[partDict["currentSeries"]]["team2"])
                    elif partDict[partDict["currentSeries"]]["score2"] == 1:
                        partDict["midTeams"]["3-1"].append(partDict[partDict["currentSeries"]]["team1"])
                        partDict["losingTeams"]["1-3"].append(partDict[partDict["currentSeries"]]["team2"])
                    elif partDict[partDict["currentSeries"]]["score2"] == 2:
                        partDict["midTeams"]["3-2"].append(partDict[partDict["currentSeries"]]["team1"])
                        partDict["losingTeams"]["2-3"].append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["winner"] == 2:
                    if partDict[partDict["currentSeries"]]["score1"] == 0:
                        partDict["midTeams"]["3-0"].append(partDict[partDict["currentSeries"]]["team2"])
                        partDict["losingTeams"]["0-3"].append(partDict[partDict["currentSeries"]]["team1"])
                    elif partDict[partDict["currentSeries"]]["score1"] == 1:
                        partDict["midTeams"]["3-1"].append(partDict[partDict["currentSeries"]]["team2"])
                        partDict["losingTeams"]["1-3"].append(partDict[partDict["currentSeries"]]["team1"])
                    elif partDict[partDict["currentSeries"]]["score1"] == 2:
                        partDict["midTeams"]["3-2"].append(partDict[partDict["currentSeries"]]["team2"])
                        partDict["losingTeams"]["2-3"].append(partDict[partDict["currentSeries"]]["team1"])
        else:
            print("unsupported best Of for Swiss at BracketPart SwissRound2")

        partDict["winningTeams"]["teams"] = partDict["winningTeams"]["3-0"] \
                                            + partDict["winningTeams"]["3-1"] \
                                            + partDict["winningTeams"]["3-2"]
        for i in range(4 - len(partDict["winningTeams"]["teams"])):
            partDict["winningTeams"]["teams"].append("_tbd")

        partDict["midTeams"]["teams"] = partDict["midTeams"]["3-0"] \
                                        + partDict["midTeams"]["3-1"] \
                                        + partDict["midTeams"]["3-2"] \
                                        + partDict["midTeams"]["2-3"] \
                                        + partDict["midTeams"]["1-3"] \
                                        + partDict["midTeams"]["0-3"]
        for i in range(8 - len(partDict["midTeams"]["teams"])):
            partDict["midTeams"]["teams"].append("_tbd")

        partDict["losingTeams"]["teams"] = partDict["losingTeams"]["2-3"] \
                                            + partDict["losingTeams"]["1-3"] \
                                            + partDict["losingTeams"]["0-3"]
        for i in range(4 - len(partDict["losingTeams"]["teams"])):
            partDict["losingTeams"]["teams"].append("_tbd")
        return partDict

    @staticmethod
    def seeding(bracketDict, partDict):
        for team in partDict["winningTeams"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["winningTeams"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["winningTeams"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["midTeams"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["midTeams"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["midTeams"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["midTeams"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["midTeams"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["midTeams"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1
        for team in partDict["losingTeams"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["losingTeams"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["losingTeams"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1

        #Bubble sort for winning Teams
        for i in range(3):
            for j in range(4 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j+1])]:
                    partDict["winningTeams"]["teams"][j], partDict["winningTeams"]["teams"][j+1] = \
                        partDict["winningTeams"]["teams"][j+1], partDict["winningTeams"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j+1])]:
                    if bracketDict["teams"].index(partDict["winningTeams"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["winningTeams"]["teams"][j+1]):
                        partDict["winningTeams"]["teams"][j], partDict["winningTeams"]["teams"][j + 1] = \
                            partDict["winningTeams"]["teams"][j + 1], partDict["winningTeams"]["teams"][j]

        #Bubble sort for mid Teams
        teams = partDict["midTeams"]["3-0"] + partDict["midTeams"]["3-1"] + partDict["midTeams"]["3-2"]
        for i in range(3):
            for j in range(4 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(teams[j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"].index(teams[j + 1])]:
                    teams[j], teams[j + 1] = teams[j + 1], teams[j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(teams[j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"].index(teams[j + 1])]:
                    if bracketDict["teams"].index(teams[j]) > \
                            bracketDict["teams"].index(teams[j + 1]):
                        teams[j], teams[j + 1] = teams[j + 1], teams[j]
        partDict["midTeams"]["teams"] = teams

        teams = partDict["midTeams"]["2-3"] + partDict["midTeams"]["1-3"] + partDict["midTeams"]["0-3"]
        for i in range(3):
            for j in range(4 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(teams[j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"].index(teams[j + 1])]:
                    teams[j], teams[j + 1] = teams[j + 1], teams[j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(teams[j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"].index(teams[j + 1])]:
                    if bracketDict["teams"].index(teams[j]) > \
                            bracketDict["teams"].index(teams[j + 1]):
                        teams[j], teams[j + 1] = teams[j + 1], teams[j]
        partDict["midTeams"]["teams"] += teams

        #Bubble sort for losing Teams
        for i in range(3):
            for j in range(4 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j + 1])]:
                    partDict["losingTeams"]["teams"][j], partDict["losingTeams"]["teams"][j + 1] = \
                        partDict["losingTeams"]["teams"][j + 1], partDict["losingTeams"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j + 1])]:
                    if bracketDict["teams"].index(partDict["losingTeams"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["losingTeams"]["teams"][j + 1]):
                        partDict["losingTeams"]["teams"][j], partDict["losingTeams"]["teams"][j + 1] = \
                            partDict["losingTeams"]["teams"][j + 1], partDict["losingTeams"]["teams"][j]

        bracketDict["r2"] = partDict
        return bracketDict


class SwissRound3:
    @staticmethod
    def initialize(partId, bo):
        dictionary = {
            "id": partId,
            "type": "SWR3",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["m1", "m2", "m3", "m4", "l1", "h1", "l2", "h2"],
            "bestOf": bo,
            "teams": {
                "2-0": ["_tbd", "_tbd", "_tbd", "_tbd"],
                "1-1": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "0-2": ["_tbd", "_tbd", "_tbd", "_tbd"]
            },
            "highTeams": {
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "winningTeams": {
                    "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                    "3-0": [],
                    "3-1": [],
                    "3-2": []
                },
                "losingTeams": {
                    "teams": ["_tbd", "_tbd"],
                    "0-3": [],
                    "1-3": [],
                    "2-3": []
                }
            },
            "lowTeams": {
                "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "winningTeams": {
                    "teams": ["_tbd", "_tbd"],
                    "3-0": [],
                    "3-1": [],
                    "3-2": []
                },
                "losingTeams": {
                    "teams": ["_tbd", "_tbd", "_tbd", "_tbd"],
                    "0-3": [],
                    "1-3": [],
                    "2-3": []
                }
            },
            "placements": {
                "1-2": {
                    "teams": ["_tbd", "_tbd"],
                    "3-0": [],
                    "3-1": [],
                    "3-2": []
                },
                "15-16": {
                    "teams": ["_tbd", "_tbd"],
                    "0-3": [],
                    "1-3": [],
                    "2-3": []
                }
            }
        }
        for i in range(2):
            dictionary.update({"h" + str(i+1): Games.OldSeries.initialize(partId + "_HI" + str(i + 1), bo)})
        for i in range(4):
            dictionary.update({"m" + str(i+1): Games.OldSeries.initialize(partId + "_MID" + str(i + 1), bo)})
        for i in range(2):
            dictionary.update({"l" + str(i+1): Games.OldSeries.initialize(partId + "_LO" + str(i + 1), bo)})
        return dictionary

    @staticmethod
    def addTeams(partDict):
        for i in range(2):
            partDict["h" + str(i+1)]["team1"] = partDict["teams"]["2-0"][i]
            partDict["h" + str(i+1)]["team2"] = partDict["teams"]["2-0"][3-i]
            partDict["l" + str(i+1)]["team1"] = partDict["teams"]["0-2"][i]
            partDict["l" + str(i+1)]["team2"] = partDict["teams"]["0-2"][3 - i]
        for i in range(4):
            partDict["m" + str(i+1)]["team1"] = partDict["teams"]["1-1"][i]
            partDict["m" + str(i+1)]["team2"] = partDict["teams"]["1-1"][7-i]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict["bestOf"] == 5:
            if partDict["currentSeries"][0] == "h":
                if partDict[partDict["currentSeries"]]["winner"] == 1:
                    partDict["placements"]["1-2"]["3-" + str(partDict[partDict["currentSeries"]]["score2"])]\
                        .append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["highTeams"]["losingTeams"][str(partDict[partDict["currentSeries"]]["score2"]) + "-3"]\
                        .append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["winner"] == 2:
                    partDict["placements"]["1-2"]["3-" + str(partDict[partDict["currentSeries"]]["score1"])]\
                        .append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["highTeams"]["losingTeams"][str(partDict[partDict["currentSeries"]]["score1"]) + "-3"]\
                        .append(partDict[partDict["currentSeries"]]["team1"])
            elif partDict["currentSeries"][0] == "m":
                if partDict[partDict["currentSeries"]]["winner"] == 1:
                    partDict["highTeams"]["winningTeams"]["3-" + str(partDict[partDict["currentSeries"]]["score2"])] \
                        .append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["lowTeams"]["losingTeams"][str(partDict[partDict["currentSeries"]]["score2"]) + "-3"]\
                        .append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["winner"] == 2:
                    partDict["highTeams"]["winningTeams"]["3-" + str(partDict[partDict["currentSeries"]]["score1"])] \
                        .append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["lowTeams"]["losingTeams"][str(partDict[partDict["currentSeries"]]["score1"]) + "-3"]\
                        .append(partDict[partDict["currentSeries"]]["team1"])
            elif partDict["currentSeries"][0] == "l":
                if partDict[partDict["currentSeries"]]["winner"] == 1:
                    partDict["lowTeams"]["winningTeams"]["3-" + str(partDict[partDict["currentSeries"]]["score2"])] \
                        .append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["placements"]["15-16"][str(partDict[partDict["currentSeries"]]["score2"]) + "-3"]\
                        .append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["winner"] == 2:
                    partDict["lowTeams"]["winningTeams"]["3-" + str(partDict[partDict["currentSeries"]]["score1"])] \
                        .append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["placements"]["15-16"][str(partDict[partDict["currentSeries"]]["score1"]) + "-3"]\
                        .append(partDict[partDict["currentSeries"]]["team1"])

        partDict["placements"]["1-2"]["teams"] = partDict["placements"]["1-2"]["3-0"] + \
                                                 partDict["placements"]["1-2"]["3-1"] + \
                                                 partDict["placements"]["1-2"]["3-2"]
        for i in range(2 - len(partDict["placements"]["1-2"]["teams"])):
            partDict["placements"]["1-2"]["teams"].append("_tbd")

        partDict["highTeams"]["winningTeams"]["teams"] = partDict["highTeams"]["winningTeams"]["3-0"] + \
                                                         partDict["highTeams"]["winningTeams"]["3-1"] + \
                                                         partDict["highTeams"]["winningTeams"]["3-2"]
        for i in range(4 - len(partDict["highTeams"]["winningTeams"]["teams"])):
            partDict["highTeams"]["winningTeams"]["teams"].append("_tbd")

        partDict["highTeams"]["losingTeams"]["teams"] = partDict["highTeams"]["losingTeams"]["2-3"] + \
                                                         partDict["highTeams"]["losingTeams"]["1-3"] + \
                                                         partDict["highTeams"]["losingTeams"]["0-3"]
        for i in range(2 - len(partDict["highTeams"]["losingTeams"]["teams"])):
            partDict["highTeams"]["losingTeams"]["teams"].append("_tbd")
        partDict["highTeams"]["teams"] = partDict["highTeams"]["losingTeams"]["teams"] + \
                                         partDict["highTeams"]["winningTeams"]["teams"]

        partDict["lowTeams"]["winningTeams"]["teams"] = partDict["lowTeams"]["winningTeams"]["3-0"] + \
                                                         partDict["lowTeams"]["winningTeams"]["3-1"] + \
                                                         partDict["lowTeams"]["winningTeams"]["3-2"]
        for i in range(2 - len(partDict["lowTeams"]["winningTeams"]["teams"])):
            partDict["lowTeams"]["winningTeams"]["teams"].append("_tbd")

        partDict["lowTeams"]["losingTeams"]["teams"] = partDict["lowTeams"]["losingTeams"]["2-3"] + \
                                                         partDict["lowTeams"]["losingTeams"]["1-3"] + \
                                                         partDict["lowTeams"]["losingTeams"]["0-3"]
        for i in range(4 - len(partDict["lowTeams"]["losingTeams"]["teams"])):
            partDict["lowTeams"]["losingTeams"]["teams"].append("_tbd")
        partDict["lowTeams"]["teams"] = partDict["lowTeams"]["losingTeams"]["teams"] + \
                                        partDict["lowTeams"]["winningTeams"]["teams"]

        partDict["placements"]["15-16"]["teams"] = partDict["placements"]["15-16"]["2-3"] + \
                                                 partDict["placements"]["15-16"]["1-3"] + \
                                                 partDict["placements"]["15-16"]["0-3"]
        for i in range(2 - len(partDict["placements"]["15-16"]["teams"])):
            partDict["placements"]["15-16"]["teams"].append("_tbd")

        return partDict

    @staticmethod
    def seeding(bracketDict, partDict):
        for team in partDict["placements"]["1-2"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["placements"]["1-2"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["placements"]["1-2"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["highTeams"]["winningTeams"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["highTeams"]["winningTeams"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["highTeams"]["winningTeams"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["highTeams"]["losingTeams"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["highTeams"]["losingTeams"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["highTeams"]["losingTeams"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1
        for team in partDict["lowTeams"]["winningTeams"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["lowTeams"]["winningTeams"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["lowTeams"]["winningTeams"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["lowTeams"]["losingTeams"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["lowTeams"]["losingTeams"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["lowTeams"]["losingTeams"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1
        for team in partDict["placements"]["15-16"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["placements"]["15-16"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["placements"]["15-16"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1

        #sort for place 1-2
        if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["1-2"]["teams"][0])] < \
                bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["1-2"]["teams"][1])]:
            partDict["placements"]["1-2"]["teams"][0], partDict["placements"]["1-2"]["teams"][1] = \
                partDict["placements"]["1-2"]["teams"][1], partDict["placements"]["1-2"]["teams"][0]
        elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["1-2"]["teams"][0])] == \
                bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["1-2"]["teams"][1])]:
            if bracketDict["teams"].index(partDict["placements"]["1-2"]["teams"][0]) > \
                    bracketDict["teams"].index(partDict["placements"]["1-2"]["teams"][1]):
                partDict["placements"]["1-2"]["teams"][0], partDict["placements"]["1-2"]["teams"][1] = \
                    partDict["placements"]["1-2"]["teams"][1], partDict["placements"]["1-2"]["teams"][0]

        #sort for high losing Teams
        if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["highTeams"]["losingTeams"]["teams"][0])] < \
                bracketDict["gameDiff"][bracketDict["teams"].index(partDict["highTeams"]["losingTeams"]["teams"][1])]:
            partDict["highTeams"]["losingTeams"]["teams"][0], partDict["highTeams"]["losingTeams"]["teams"][1] = \
                partDict["highTeams"]["losingTeams"]["teams"][1], partDict["highTeams"]["losingTeams"]["teams"][0]
        elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["highTeams"]["losingTeams"]["teams"][0])] == \
                bracketDict["gameDiff"][bracketDict["teams"].index(partDict["highTeams"]["losingTeams"]["teams"][1])]:
            if bracketDict["teams"].index(partDict["highTeams"]["losingTeams"]["teams"][0]) > \
                    bracketDict["teams"].index(partDict["highTeams"]["losingTeams"]["teams"][1]):
                partDict["highTeams"]["losingTeams"]["teams"][0], partDict["highTeams"]["losingTeams"]["teams"][1] = \
                    partDict["highTeams"]["losingTeams"]["teams"][1], partDict["highTeams"]["losingTeams"]["teams"][0]

        #Bubble sort for high winning Teams
        for i in range(3):
            for j in range(4 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"]
                        .index(partDict["highTeams"]["winningTeams"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["highTeams"]["winningTeams"]["teams"][j+1])]:
                    partDict["highTeams"]["winningTeams"]["teams"][j], \
                    partDict["highTeams"]["winningTeams"]["teams"][j+1] = \
                        partDict["highTeams"]["winningTeams"]["teams"][j+1], \
                        partDict["highTeams"]["winningTeams"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"]
                        .index(partDict["highTeams"]["winningTeams"]["teams"][j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["highTeams"]["winningTeams"]["teams"][j + 1])]:
                    if bracketDict["teams"].index(partDict["highTeams"]["winningTeams"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["highTeams"]["winningTeams"]["teams"][j+1]):
                        partDict["highTeams"]["winningTeams"]["teams"][j], \
                        partDict["highTeams"]["winningTeams"]["teams"][j + 1] = \
                            partDict["highTeams"]["winningTeams"]["teams"][j + 1], \
                            partDict["highTeams"]["winningTeams"]["teams"][j]
        partDict["highTeams"]["teams"] = partDict["highTeams"]["losingTeams"]["teams"] + \
                                         partDict["highTeams"]["winningTeams"]["teams"]

        #Bubble sort for low losing Teams
        for i in range(3):
            for j in range(4 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"]
                        .index(partDict["lowTeams"]["losingTeams"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["lowTeams"]["losingTeams"]["teams"][j+1])]:
                    partDict["lowTeams"]["losingTeams"]["teams"][j], \
                    partDict["lowTeams"]["losingTeams"]["teams"][j + 1] = \
                        partDict["lowTeams"]["losingTeams"]["teams"][j + 1], \
                        partDict["lowTeams"]["losingTeams"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"]
                        .index(partDict["lowTeams"]["losingTeams"]["teams"][j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["lowTeams"]["losingTeams"]["teams"][j + 1])]:
                    if bracketDict["teams"].index(partDict["lowTeams"]["losingTeams"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["lowTeams"]["losingTeams"]["teams"][j+1]):
                        partDict["lowTeams"]["losingTeams"]["teams"][j], \
                        partDict["lowTeams"]["losingTeams"]["teams"][j+1] = \
                            partDict["lowTeams"]["losingTeams"]["teams"][j+1], \
                            partDict["lowTeams"]["losingTeams"]["teams"][j]

        #sort for low winning Teams
        if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["lowTeams"]["winningTeams"]["teams"][0])] < \
                bracketDict["gameDiff"][bracketDict["teams"].index(partDict["lowTeams"]["winningTeams"]["teams"][1])]:
            partDict["lowTeams"]["winningTeams"]["teams"][0], partDict["lowTeams"]["winningTeams"]["teams"][1] = \
                partDict["lowTeams"]["winningTeams"]["teams"][1], partDict["lowTeams"]["winningTeams"]["teams"][0]
        elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["lowTeams"]["winningTeams"]["teams"][0])] == \
                bracketDict["gameDiff"][bracketDict["teams"].index(partDict["lowTeams"]["winningTeams"]["teams"][1])]:
            if bracketDict["teams"].index(partDict["lowTeams"]["winningTeams"]["teams"][0]) > \
                    bracketDict["teams"].index(partDict["lowTeams"]["winningTeams"]["teams"][1]):
                partDict["lowTeams"]["winningTeams"]["teams"][0], partDict["lowTeams"]["winningTeams"]["teams"][1] = \
                    partDict["lowTeams"]["winningTeams"]["teams"][1], partDict["lowTeams"]["winningTeams"]["teams"][0]
        partDict["lowTeams"]["teams"] = partDict["lowTeams"]["losingTeams"]["teams"] + \
                                         partDict["lowTeams"]["winningTeams"]["teams"]

        bracketDict["r3"] = partDict
        return bracketDict


class SwissRound4:
    @staticmethod
    def initialize(partId, bo):
        dictionary = {
            "id": partId,
            "type": "SWR4",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["h1", "l1", "h2", "l2", "h3", "l3"],
            "bestOf": bo,
            "teams": {
                "2-1": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "1-2": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
            },
            "winningTeams": {
                "teams": ["_tbd", "_tbd", "_tbd"],
                "3-0": [],
                "3-1": [],
                "3-2": []
            },
            "losingTeams": {
                "teams": ["_tbd", "_tbd", "_tbd"],
                "0-3": [],
                "1-3": [],
                "2-3": []
            },
            "placements": {
                "3-5": {
                    "teams": ["_tbd", "_tbd", "_tbd"],
                    "3-0": [],
                    "3-1": [],
                    "3-2": []
                },
                "12-14": {
                    "teams": ["_tbd", "_tbd", "_tbd"],
                    "0-3": [],
                    "1-3": [],
                    "2-3": []
                }
            }
        }

        for i in range(3):
            dictionary.update({"h" + str(i+1): Games.OldSeries.initialize(partId + "_HI" + str(i + 1), bo)})
            dictionary.update({"l" + str(i+1): Games.OldSeries.initialize(partId + "_LO" + str(i + 1), bo)})
        return dictionary

    @staticmethod
    def addTeams(partDict):
        for i in range(3):
            partDict["h" + str(i+1)]["team1"] = partDict["teams"]["2-1"][i]
            partDict["h" + str(i+1)]["team2"] = partDict["teams"]["2-1"][5-i]
            partDict["l" + str(i+1)]["team1"] = partDict["teams"]["1-2"][i]
            partDict["l" + str(i+1)]["team2"] = partDict["teams"]["1-2"][5-i]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict["bestOf"] == 5:
            if partDict["currentSeries"][0] == "h":
                if partDict[partDict["currentSeries"]]["winner"] == 1:
                    partDict["placements"]["3-5"]["3-" + str(partDict[partDict["currentSeries"]]["score2"])] \
                        .append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["losingTeams"][str(partDict[partDict["currentSeries"]]["score2"]) + "-3"] \
                        .append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["winner"] == 2:
                    partDict["placements"]["3-5"]["3-" + str(partDict[partDict["currentSeries"]]["score1"])] \
                        .append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["losingTeams"][str(partDict[partDict["currentSeries"]]["score1"]) + "-3"] \
                        .append(partDict[partDict["currentSeries"]]["team1"])
            elif partDict["currentSeries"][0] == "l":
                if partDict[partDict["currentSeries"]]["winner"] == 1:
                    partDict["winningTeams"]["3-" + str(partDict[partDict["currentSeries"]]["score2"])] \
                        .append(partDict[partDict["currentSeries"]]["team1"])
                    partDict["placements"]["12-14"][str(partDict[partDict["currentSeries"]]["score2"]) + "-3"] \
                        .append(partDict[partDict["currentSeries"]]["team2"])
                elif partDict[partDict["currentSeries"]]["winner"] == 2:
                    partDict["winningTeams"]["3-" + str(partDict[partDict["currentSeries"]]["score1"])] \
                        .append(partDict[partDict["currentSeries"]]["team2"])
                    partDict["placements"]["12-14"][str(partDict[partDict["currentSeries"]]["score1"]) + "-3"] \
                        .append(partDict[partDict["currentSeries"]]["team1"])

        partDict["placements"]["3-5"]["teams"] = partDict["placements"]["3-5"]["3-0"] + \
                                                 partDict["placements"]["3-5"]["3-1"] + \
                                                 partDict["placements"]["3-5"]["3-2"]
        for i in range(3 - len(partDict["placements"]["3-5"]["teams"])):
            partDict["placements"]["3-5"]["teams"].append("_tbd")

        partDict["winningTeams"]["teams"] = partDict["winningTeams"]["3-0"] + \
                                            partDict["winningTeams"]["3-1"] + \
                                            partDict["winningTeams"]["3-2"]
        for i in range(3 - len(partDict["winningTeams"]["teams"])):
            partDict["winningTeams"]["teams"].append("_tbd")

        partDict["losingTeams"]["teams"] = partDict["losingTeams"]["2-3"] + \
                                           partDict["losingTeams"]["1-3"] + \
                                           partDict["losingTeams"]["0-3"]
        for i in range(3 - len(partDict["losingTeams"]["teams"])):
            partDict["losingTeams"]["teams"].append("_tbd")

        partDict["placements"]["12-14"]["teams"] = partDict["placements"]["12-14"]["2-3"] + \
                                                   partDict["placements"]["12-14"]["1-3"] + \
                                                   partDict["placements"]["12-14"]["0-3"]
        for i in range(3 - len(partDict["placements"]["12-14"]["teams"])):
            partDict["placements"]["12-14"]["teams"].append("_tbd")

        return partDict

    @staticmethod
    def seeding(bracketDict, partDict):
        for team in partDict["placements"]["3-5"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["placements"]["3-5"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["placements"]["3-5"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["winningTeams"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["winningTeams"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["winningTeams"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["losingTeams"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["losingTeams"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["losingTeams"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1
        for team in partDict["placements"]["12-14"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["placements"]["12-14"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["placements"]["12-14"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1

        #Bubble sort for place 3-5
        for i in range(2):
            for j in range(3 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["3-5"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["placements"]["3-5"]["teams"][j+1])]:
                    partDict["placements"]["3-5"]["teams"][j], partDict["placements"]["3-5"]["teams"][j+1] = \
                        partDict["placements"]["3-5"]["teams"][j+1], partDict["placements"]["3-5"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["3-5"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["placements"]["3-5"]["teams"][j + 1])]:
                    if bracketDict["teams"].index(partDict["placements"]["3-5"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["placements"]["3-5"]["teams"][j+1]):
                        partDict["placements"]["3-5"]["teams"][j], partDict["placements"]["3-5"]["teams"][j+1] = \
                            partDict["placements"]["3-5"]["teams"][j+1], partDict["placements"]["3-5"]["teams"][j]

        #Bubble sort for winning Teams
        for i in range(2):
            for j in range(3 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j+1])]:
                    partDict["winningTeams"]["teams"][j], partDict["winningTeams"]["teams"][j+1] = \
                        partDict["winningTeams"]["teams"][j+1], partDict["winningTeams"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["winningTeams"]["teams"][j + 1])]:
                    if bracketDict["teams"].index(partDict["winningTeams"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["winningTeams"]["teams"][j+1]):
                        partDict["winningTeams"]["teams"][j], partDict["winningTeams"]["teams"][j+1] = \
                            partDict["winningTeams"]["teams"][j+1], partDict["winningTeams"]["teams"][j]

        # Bubble sort for losing Teams
        for i in range(2):
            for j in range(3 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j+1])]:
                    partDict["losingTeams"]["teams"][j], partDict["losingTeams"]["teams"][j+1] = \
                        partDict["losingTeams"]["teams"][j+1], partDict["losingTeams"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j])] == \
                        bracketDict["gameDiff"][bracketDict["teams"].index(partDict["losingTeams"]["teams"][j+1])]:
                    if bracketDict["teams"].index(partDict["losingTeams"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["losingTeams"]["teams"][j+1]):
                        partDict["losingTeams"]["teams"][j], partDict["losingTeams"]["teams"][j+1] = \
                            partDict["losingTeams"]["teams"][j+1], partDict["losingTeams"]["teams"][j]

        bracketDict["r4"] = partDict
        return bracketDict


class SwissRound5:
    @staticmethod
    def initialize(partId, bo):
        dictionary = {
            "id": partId,
            "type": "SWR5",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["s1", "s2", "s3"],
            "bestOf": bo,
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "placements": {
                "6-8": {
                    "teams": ["_tbd", "_tbd", "_tbd"],
                    "3-0": [],
                    "3-1": [],
                    "3-2": []
                },
                "9-11": {
                    "teams": ["_tbd", "_tbd", "_tbd"],
                    "0-3": [],
                    "1-3": [],
                    "2-3": []
                }
            }
        }
        for i in range(3):
            dictionary.update({"s" + str(i+1): Games.OldSeries.initialize(partId + "_SER" + str(i + 1), bo)})
        return dictionary

    @staticmethod
    def addTeams(partDict):
        for i in range(3):
            partDict["s" + str(i+1)]["team1"] = partDict["teams"][i]
            partDict["s" + str(i+1)]["team2"] = partDict["teams"][5-i]
        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict["bestOf"] == 5:
            if partDict[partDict["currentSeries"]]["winner"] == 1:
                partDict["placements"]["6-8"]["3-" + str(partDict[partDict["currentSeries"]]["score2"])] \
                    .append(partDict[partDict["currentSeries"]]["team1"])
                partDict["placements"]["9-11"][str(partDict[partDict["currentSeries"]]["score2"]) + "-3"] \
                    .append(partDict[partDict["currentSeries"]]["team2"])
            elif partDict[partDict["currentSeries"]]["winner"] == 2:
                partDict["placements"]["6-8"]["3-" + str(partDict[partDict["currentSeries"]]["score1"])] \
                    .append(partDict[partDict["currentSeries"]]["team2"])
                partDict["placements"]["9-11"][str(partDict[partDict["currentSeries"]]["score1"]) + "-3"] \
                    .append(partDict[partDict["currentSeries"]]["team1"])

        partDict["placements"]["6-8"]["teams"] = partDict["placements"]["6-8"]["3-0"] + \
                                                 partDict["placements"]["6-8"]["3-1"] + \
                                                 partDict["placements"]["6-8"]["3-2"]
        for i in range(3 - len(partDict["placements"]["6-8"]["teams"])):
            partDict["placements"]["6-8"]["teams"].append("_tbd")

        partDict["placements"]["9-11"]["teams"] = partDict["placements"]["9-11"]["2-3"] + \
                                                  partDict["placements"]["9-11"]["1-3"] + \
                                                  partDict["placements"]["9-11"]["0-3"]
        for i in range(3 - len(partDict["placements"]["9-11"]["teams"])):
            partDict["placements"]["9-11"]["teams"].append("_tbd")

        return partDict

    @staticmethod
    def seeding(bracketDict, partDict):
        for team in partDict["placements"]["6-8"]["3-0"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 3
        for team in partDict["placements"]["6-8"]["3-1"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 2
        for team in partDict["placements"]["6-8"]["3-2"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] += 1
        for team in partDict["placements"]["9-11"]["0-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 3
        for team in partDict["placements"]["9-11"]["1-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 2
        for team in partDict["placements"]["9-11"]["2-3"]:
            bracketDict["gameDiff"][bracketDict["teams"].index(team)] -= 1

        # Bubble sort for place 6-8
        for i in range(2):
            for j in range(3 - i - 1):
                if bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["6-8"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["placements"]["6-8"]["teams"][j+1])]:
                    partDict["placements"]["6-8"]["teams"][j], partDict["placements"]["6-8"]["teams"][j+1] = \
                        partDict["placements"]["6-8"]["teams"][j+1], partDict["placements"]["6-8"]["teams"][j]
                elif bracketDict["gameDiff"][bracketDict["teams"].index(partDict["placements"]["6-8"]["teams"][j])] < \
                        bracketDict["gameDiff"][bracketDict["teams"]
                                .index(partDict["placements"]["6-8"]["teams"][j+1])]:
                    if bracketDict["teams"].index(partDict["placements"]["6-8"]["teams"][j]) > \
                            bracketDict["teams"].index(partDict["placements"]["6-8"]["teams"][j+1]):
                        partDict["placements"]["6-8"]["teams"][j], partDict["placements"]["6-8"]["teams"][j+1] = \
                            partDict["placements"]["6-8"]["teams"][j+1], partDict["placements"]["6-8"]["teams"][j]

        bracketDict["r5"] = partDict
        return bracketDict


class RoundOf16:
    @staticmethod
    def initialize(partId, bo):
        dictionary = {
            "id": partId,
            "type": "RO16",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"],
            "bestOf": bo,
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "winningTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "losingTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
        }
        for i in range(8):
            dictionary.update({"s" + str(i + 1): Games.OldSeries.initialize(partId + "_SER" + str(i + 1), bo)})
        return dictionary

    @staticmethod
    def addTeams(partDict):
        for i in range(8):
            partDict["s" + str(i+1)]["team1"] = partDict["teams"][i]
            partDict["s" + str(i+1)]["team2"] = partDict["teams"][15-i]

        return partDict

    @staticmethod
    def checkResults(partDict):
        if partDict[partDict["currentSeries"]]["winner"] == 1:
            partDict["winningTeams"][int(partDict["currentSeries"][-1]) - 1] \
                = partDict[partDict["currentSeries"]]["team1"]
            partDict["losingTeams"][int(partDict["currentSeries"][-1]) - 1] \
                = partDict[partDict["currentSeries"]]["team2"]
        elif partDict[partDict["currentSeries"]]["winner"] == 2:
            partDict["winningTeams"][int(partDict["currentSeries"][-1]) - 1] \
                = partDict[partDict["currentSeries"]]["team2"]
            partDict["losingTeams"][int(partDict["currentSeries"][-1]) - 1] \
                = partDict[partDict["currentSeries"]]["team1"]
        return partDict


class RoundOf32:
    @staticmethod
    def initialize(partId, bo):
        dictionary = {
            "id": partId,
            "type": "RO32",
            "current": False,
            "currentSeries": "",
            "upcomingSeries": [],
            "bestOf": bo,
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "winningTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                             "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "losingTeams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                            "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
        }
        for i in range(16):
            dictionary["upcomingSeries"].append("s" + str(i + 1))
            dictionary.update({"s" + str(i + 1): Games.OldSeries.initialize(partId + "_SER" + str(i + 1), bo)})
        return dictionary

    @staticmethod
    def addTeams(partDict):
        for i in range(16):
            partDict["s" + str(i+1)]["team1"] = partDict["teams"][i]
            partDict["s" + str(i+1)]["team2"] = partDict["teams"][31-i]

        return partDict

    @staticmethod
    def checkResults(partDict):
        #print("1" + str(partDict))
        if partDict[partDict["currentSeries"]]["winner"] == 1:
            partDict["winningTeams"][int(partDict["currentSeries"][1:]) - 1] \
                = partDict[partDict["currentSeries"]]["team1"]
            partDict["losingTeams"][int(partDict["currentSeries"][1:]) - 1] \
                = partDict[partDict["currentSeries"]]["team2"]
        elif partDict[partDict["currentSeries"]]["winner"] == 2:
            partDict["winningTeams"][int(partDict["currentSeries"][1:]) - 1] \
                = partDict[partDict["currentSeries"]]["team2"]
            partDict["losingTeams"][int(partDict["currentSeries"][1:]) - 1] \
                = partDict[partDict["currentSeries"]]["team1"]
        #print("2" + str(partDict))
        return partDict

import tournament.BracketParts as Parts


def submitScore(bracketDict, partDict, condition):
    bracketDict[bracketDict["currentPart"]] = partDict
    if condition:
        bracketDict[bracketDict["currentPart"]]["current"] = False
        bracketDict = checkResults(bracketDict)
        if len(bracketDict["upcomingParts"]) > 0:
            bracketDict = startBracket(bracketDict)
            return bracketDict, False
        else:
            return bracketDict, True
    else:
        return bracketDict, False


def startBracket(bracketDict):
    bracketDict["current"] = True
    bracketDict["currentPart"] = bracketDict["upcomingParts"].pop(0)
    bracketDict[bracketDict["currentPart"]] = Parts.startPart(bracketDict[bracketDict["currentPart"]])
    return bracketDict


def checkResults(bracketDict):
    if bracketDict["type"] == "SE8":
        return SE8.checkResults(bracketDict)
    elif bracketDict["type"] == "SWISS":
        return Swiss.checkResults(bracketDict)
    elif bracketDict["type"] == "16-8Q-U-16L8D-8Q":
        return B16_8Q_U_16L8D_8Q.checkResults(bracketDict)
    elif bracketDict["type"] == "16-4Q-U-32L8DSL4D-4Q":
        return B16_4Q_U_32L8DSL4D_4Q.checkResults(bracketDict)


class SE8:
    @staticmethod
    def initialize(bracketId, variation):
        variations = {
            1: {
                "qfbo": 7,
                "sfbo": 7,
                "fset": 3,
                "fbo": 7
            },
            2: {
                "qfbo": 1,
                "sfbo": 1,
                "fset": 1,
                "fbo": 1
            }
        }
        return {
            "id": bracketId,
            "type": "SE8",
            "current": False,
            "currentPart": "",
            "upcomingParts": ["quarterFinals", "semiFinals", "finals"],
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "placements": {
                "1": "_tbd",
                "2": "_tbd",
                "3-4": ["_tbd", "_tbd"],
                "5-8": ["_tbd", "_tbd", "_tbd", "_tbd"]
            },
            "quarterFinals": Parts.QuarterFinals.initialize(bracketId + "_QF", variations[variation]["qfbo"]),
            "semiFinals": Parts.SemiFinals.initialize(bracketId + "_SF", variations[variation]["sfbo"]),
            "finals":
                Parts.Finals.initialize(bracketId + "_FIN", variations[variation]["fbo"], variations[variation]["fset"])
        }

    @staticmethod
    def addTeams(bracketDict):
        bracketDict["quarterFinals"]["teams"] = bracketDict["teams"]
        bracketDict["quarterFinals"] = Parts.QuarterFinals.addTeams(bracketDict["quarterFinals"])
        bracketDict["semiFinals"] = Parts.SemiFinals.addTeams(bracketDict["semiFinals"])
        bracketDict["finals"] = Parts.Finals.addTeams(bracketDict["finals"])
        return bracketDict

    @staticmethod
    def checkResults(bracketDict):
        bracketDict["placements"]["5-8"] = bracketDict["quarterFinals"]["losingTeams"]
        bracketDict["placements"]["3-4"] = bracketDict["semiFinals"]["losingTeams"]
        bracketDict["placements"]["2"] = bracketDict["finals"]["losingTeams"]
        bracketDict["placements"]["1"] = bracketDict["finals"]["winningTeams"]

        bracketDict["semiFinals"]["teams"] = bracketDict["quarterFinals"]["winningTeams"]
        bracketDict["finals"]["teams"] = bracketDict["semiFinals"]["winningTeams"]

        bracketDict = SE8.addTeams(bracketDict)

        return bracketDict


class Swiss:
    @staticmethod
    def initialize(bracketId, variation):
        variations = {
            1: {
                "r1bo": 5,
                "r2bo": 5,
                "r3bo": 5,
                "r4bo": 5,
                "r5bo": 5
            }
        }
        return {
            "id": bracketId,
            "type": "SWISS",
            "current": False,
            "currentPart": "",
            "upcomingParts": ["r1", "r2", "r3", "r4", "r5"],
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "gameDiff": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "placements": {
                "1-2": ["_tbd", "_tbd"],
                "3-5": ["_tbd", "_tbd", "_tbd"],
                "6-8": ["_tbd", "_tbd", "_tbd"],
                "9-11": ["_tbd", "_tbd", "_tbd"],
                "12-14": ["_tbd", "_tbd", "_tbd"],
                "15-16": ["_tbd", "_tbd"]
            },
            "r1": Parts.SwissRound1.initialize(bracketId + "_R1", variations[variation]["r1bo"]),
            "r2": Parts.SwissRound2.initialize(bracketId + "_R2", variations[variation]["r2bo"]),
            "r3": Parts.SwissRound3.initialize(bracketId + "_R3", variations[variation]["r3bo"]),
            "r4": Parts.SwissRound4.initialize(bracketId + "_R4", variations[variation]["r4bo"]),
            "r5": Parts.SwissRound5.initialize(bracketId + "_R5", variations[variation]["r5bo"])
        }

    @staticmethod
    def addTeams(bracketDict):
        #Round1
        bracketDict["r1"]["teams"] = bracketDict["teams"]
        bracketDict["r1"] = Parts.SwissRound1.addTeams(bracketDict["r1"])
        #Round2
        bracketDict["r2"]["teams"]["1-0"] = bracketDict["r1"]["winningTeams"]["teams"]
        bracketDict["r2"]["teams"]["0-1"] = bracketDict["r1"]["losingTeams"]["teams"]
        bracketDict["r2"] = Parts.SwissRound2.addTeams(bracketDict["r2"])
        #Round3
        bracketDict["r3"]["teams"]["2-0"] = bracketDict["r2"]["winningTeams"]["teams"]
        bracketDict["r3"]["teams"]["1-1"] = bracketDict["r2"]["midTeams"]["teams"]
        bracketDict["r3"]["teams"]["0-2"] = bracketDict["r2"]["losingTeams"]["teams"]
        bracketDict["r3"] = Parts.SwissRound3.addTeams(bracketDict["r3"])
        #Round4
        bracketDict["r4"]["teams"]["2-1"] = bracketDict["r3"]["highTeams"]["teams"]
        bracketDict["r4"]["teams"]["1-2"] = bracketDict["r3"]["lowTeams"]["teams"]
        bracketDict["r4"] = Parts.SwissRound4.addTeams(bracketDict["r4"])
        #Round5
        bracketDict["r5"]["teams"] = bracketDict["r4"]["losingTeams"]["teams"] + \
                                     bracketDict["r4"]["winningTeams"]["teams"]
        bracketDict["r5"] = Parts.SwissRound5.addTeams(bracketDict["r5"])
        return bracketDict

    @staticmethod
    def checkResults(bracketDict):
        if not bracketDict[bracketDict["currentPart"]]["current"]:
            bracketDict = Parts.seeding(bracketDict, bracketDict[bracketDict["currentPart"]])
            bracketDict = Swiss.addTeams(bracketDict)

        bracketDict["placements"]["1-2"] = bracketDict["r3"]["placements"]["1-2"]["teams"]
        bracketDict["placements"]["3-5"] = bracketDict["r4"]["placements"]["3-5"]["teams"]
        bracketDict["placements"]["6-8"] = bracketDict["r5"]["placements"]["6-8"]["teams"]
        bracketDict["placements"]["9-11"] = bracketDict["r5"]["placements"]["9-11"]["teams"]
        bracketDict["placements"]["12-14"] = bracketDict["r4"]["placements"]["12-14"]["teams"]
        bracketDict["placements"]["15-16"] = bracketDict["r3"]["placements"]["15-16"]["teams"]
        return bracketDict


class B16_8Q_U_16L8D_8Q:
    @staticmethod
    def initialize(bracketId, variation):
        variations = {
            1: {
                "ur1bo": 5,
                "lr1bo": 5,
                "lr2bo": 5
            }
        }
        return {
            "id": bracketId,
            "type": "16-8Q-U-16L8D-8Q",
            "current": False,
            "currentPart": "",
            "upcomingParts": ["ur1", "lr1", "lr2"],
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "placements": {
                "qualified": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                              "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "eliminated": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                               "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
            },
            "ur1": Parts.RoundOf16.initialize(bracketId + "_UR1", variations[variation]["ur1bo"]),
            "lr1": Parts.RoundOf16.initialize(bracketId + "_LR1", variations[variation]["lr1bo"]),
            "lr2": Parts.RoundOf16.initialize(bracketId + "_LR2", variations[variation]["lr2bo"])
        }

    @staticmethod
    def addTeams(bracketDict):
        bracketDict["ur1"]["teams"] = bracketDict["teams"][:16]
        bracketDict["ur1"] = Parts.RoundOf16.addTeams(bracketDict["ur1"])

        bracketDict["lr1"]["teams"] = bracketDict["teams"][16:]
        bracketDict["lr1"] = Parts.RoundOf16.addTeams(bracketDict["lr1"])

        bracketDict["lr2"]["teams"] = bracketDict["ur1"]["losingTeams"][::-1]
        bracketDict["lr2"]["teams"] = bracketDict["lr2"]["teams"] + bracketDict["lr1"]["winningTeams"]
        bracketDict["lr2"] = Parts.RoundOf16.addTeams(bracketDict["lr2"])

        return bracketDict

    @staticmethod
    def checkResults(bracketDict):
        bracketDict["placements"]["qualified"] = bracketDict["ur1"]["winningTeams"] + bracketDict["lr2"]["winningTeams"]
        bracketDict["placements"]["eliminated"] = bracketDict["lr1"]["losingTeams"] + bracketDict["lr2"]["losingTeams"]

        bracketDict = B16_8Q_U_16L8D_8Q.addTeams(bracketDict)

        return bracketDict


class B16_4Q_U_32L8DSL4D_4Q:
    @staticmethod
    def initialize(bracketId, variation):
        variations = {
            1: {
                "ur1bo": 5,
                "ur2bo": 5,
                "lr1bo": 5,
                "lr2bo": 5,
                "lr3bo": 5,
                "lr4bo": 5,
                "lr5bo": 5
            }
        }
        return {
            "id": bracketId,
            "type": "16-4Q-U-32L8DSL4D-4Q",
            "current": False,
            "currentPart": "",
            "upcomingParts": ["lr1", "lr2", "ur1", "lr3", "lr4", "ur2", "lr5"],
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "placements": {
                "qualified": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
                "eliminated": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                               "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                               "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                               "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                               "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"]
            },
            "ur1": Parts.RoundOf16.initialize(bracketId + "_UR1", variations[variation]["ur1bo"]),
            "ur2": Parts.QuarterFinals.initialize(bracketId + "_UR2", variations[variation]["ur2bo"]),
            "lr1": Parts.RoundOf32.initialize(bracketId + "_LR1", variations[variation]["lr1bo"]),
            "lr2": Parts.RoundOf16.initialize(bracketId + "_LR2", variations[variation]["lr2bo"]),
            "lr3": Parts.RoundOf16.initialize(bracketId + "_LR3", variations[variation]["lr3bo"]),
            "lr4": Parts.QuarterFinals.initialize(bracketId + "_LR4", variations[variation]["lr4bo"]),
            "lr5": Parts.QuarterFinals.initialize(bracketId + "_LR5", variations[variation]["lr5bo"])
        }

    @staticmethod
    def addTeams(bracketDict):
        bracketDict["ur1"]["teams"] = bracketDict["teams"][:16]
        bracketDict["ur1"] = Parts.RoundOf16.addTeams(bracketDict["ur1"])

        bracketDict["ur2"]["teams"] = bracketDict["ur1"]["winningTeams"]
        bracketDict["ur2"] = Parts.QuarterFinals.addTeams(bracketDict["ur2"])

        bracketDict["lr1"]["teams"] = bracketDict["teams"][16:]
        bracketDict["lr1"] = Parts.RoundOf32.addTeams(bracketDict["lr1"])

        bracketDict["lr2"]["teams"] = bracketDict["lr1"]["winningTeams"]
        bracketDict["lr2"] = Parts.RoundOf16.addTeams(bracketDict["lr2"])

        bracketDict["lr3"]["teams"] = bracketDict["ur1"]["losingTeams"] + bracketDict["lr2"]["winningTeams"]
        bracketDict["lr3"] = Parts.RoundOf16.addTeams(bracketDict["lr3"])

        bracketDict["lr4"]["teams"] = bracketDict["lr3"]["winningTeams"]
        bracketDict["lr4"] = Parts.QuarterFinals.addTeams(bracketDict["lr4"])

        bracketDict["lr5"]["teams"] = bracketDict["ur2"]["losingTeams"] + bracketDict["lr4"]["winningTeams"]
        bracketDict["lr5"] = Parts.QuarterFinals.addTeams(bracketDict["lr5"])

        return bracketDict

    @staticmethod
    def checkResults(bracketDict):
        bracketDict["placements"]["qualified"] = bracketDict["ur2"]["winningTeams"] + bracketDict["lr5"]["winningTeams"]
        bracketDict["placements"]["eliminated"] = bracketDict["lr1"]["losingTeams"] + \
                                                  bracketDict["lr2"]["losingTeams"] + \
                                                  bracketDict["lr3"]["losingTeams"] + \
                                                  bracketDict["lr4"]["losingTeams"] + bracketDict["lr5"]["losingTeams"]

        bracketDict = B16_4Q_U_32L8DSL4D_4Q.addTeams(bracketDict)

        return bracketDict

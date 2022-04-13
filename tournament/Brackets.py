import tournament.BracketParts as Parts


def submitScore(bracketDict, partDict, condition):
    bracketDict[bracketDict["currentPart"]] = partDict
    if condition:
        bracketDict = checkResults(bracketDict)
        bracketDict[bracketDict["currentPart"]]["current"] = False
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
        print("check SE8")
        return SE8.checkResults(bracketDict)


class SE8:
    @staticmethod
    def initialize(bracketId, variation):
        variations = {
            1: {
                "qfbo": 7,
                "sfbo": 7,
                "fset": 3,
                "fbo": 7
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

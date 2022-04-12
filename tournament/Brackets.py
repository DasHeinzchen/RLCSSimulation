import tournament.BracketParts as Parts


def submitScore(bracketDict, partDict, condition):
    bracketDict[bracketDict["currentPart"]] = partDict
    if condition:
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
            "current": False,
            "currentPart": "",
            "upcomingParts": ["quarterFinals", "semiFinals", "finals"],
            "teams": [],
            "quarterFinals": Parts.QuarterFinals.initialize(bracketId + "_QF", variations[variation]["qfbo"]),
            "semiFinals": Parts.SemiFinals.initialize(bracketId + "_SF", variations[variation]["sfbo"]),
            "finals":
                Parts.Finals.initialize(bracketId + "_FIN", variations[variation]["fbo"], variations[variation]["fset"])
        }

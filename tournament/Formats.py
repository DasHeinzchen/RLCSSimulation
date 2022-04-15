import tournament.Brackets as Brackets


def startFormat(formatDict):
    formatDict["current"] = True
    formatDict["currentBracket"] = formatDict["upcomingBrackets"].pop(0)
    formatDict[formatDict["currentBracket"]] = Brackets.startBracket(formatDict[formatDict["currentBracket"]])
    return formatDict


def submitScore(formatDict, bracketDict, condition):
    formatDict[formatDict["currentBracket"]] = bracketDict
    if condition:
        formatDict = checkResults(formatDict)
        formatDict[formatDict["currentBracket"]]["current"] = False
        if len(formatDict["upcomingBrackets"]) > 0:
            formatDict = startFormat(formatDict)
            return formatDict, False
        else:
            return formatDict, True
    else:
        return formatDict, False


def checkResults(formatDict):
    if formatDict["type"] == "Fall_Format":
        return FallFormat.checkResults(formatDict)


class FallFormat:
    @staticmethod
    def initialize(formatId):
        return {
            "type": "Fall_Format",
            "current": False,
            "currentBracket": "",
            "upcomingBrackets": ["swissStage", "playoffs"],
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "placements": {
                "1": "_tbd",
                "2": "_tbd",
                "3-4": ["_tbd", "_tbd"],
                "5-8": ["_tbd", "_tbd", "_tbd", "_tbd"],
                "9-11": ["_tbd", "_tbd", "_tbd"],
                "12-14": ["_tbd", "_tbd", "_tbd"],
                "15-16": ["_tbd", "_tbd"]
            },
            "swissStage": Brackets.Swiss.initialize(formatId + "_SWISS", 1),
            "playoffs": Brackets.SE8.initialize(formatId + "_PO", 1)
        }

    @staticmethod
    def addTeams(formatDict):
        formatDict["swissStage"]["teams"] = formatDict["teams"]
        formatDict["swissStage"] = Brackets.Swiss.addTeams(formatDict["swissStage"])
        return formatDict

    @staticmethod
    def checkResults(formatDict):
        formatDict["playoffs"]["teams"] = formatDict["swissStage"]["placements"]["1-2"] + \
                                          formatDict["swissStage"]["placements"]["3-5"] + \
                                          formatDict["swissStage"]["placements"]["6-8"]

        formatDict["placements"].update(formatDict["playoffs"]["placements"])
        formatDict["placements"].update({
            "9-11": formatDict["swissStage"]["placements"]["9-11"],
            "12-14": formatDict["swissStage"]["placements"]["12-14"],
            "15-16": formatDict["swissStage"]["placements"]["15-16"]
        })

        formatDict["playoffs"] = Brackets.SE8.addTeams(formatDict["playoffs"])
        return formatDict


def initializeFormat(formatType, formatId):
    if formatType == "Fall_Format":
        return FallFormat.initialize(formatId)
    else: return {}


def addTeams(formatDict, teams):
    formatDict["teams"] = teams
    if formatDict["type"] == "Fall_Format":
        return FallFormat.addTeams(formatDict)

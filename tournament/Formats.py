import EventHandler
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
    elif formatDict["type"] == "Swiss":
        return Swiss.checkResults(formatDict)
    elif formatDict["type"] == "OQD3:16-8Q-U-16L8D-8Q":
        return OpenQualDay3.checkResults(formatDict)
    elif formatDict["type"] == "QD2:16-4Q-U-32L8DSL4D-4Q":
        return QualDay2.checkResults(formatDict)


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


class Swiss:
    @staticmethod
    def initialize(formatId, variation):
        return {
            "type": "Swiss",
            "current": False,
            "currentBracket": "",
            "upcomingBrackets": ["swissStage"],
            "teams": ["_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd",
                      "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd", "_tbd"],
            "placements": {
                "1-2": ["_tbd", "_tbd"],
                "3-5": ["_tbd", "_tbd", "_tbd"],
                "6-8": ["_tbd", "_tbd", "_tbd"],
                "9-11": ["_tbd", "_tbd", "_tbd"],
                "12-14": ["_tbd", "_tbd", "_tbd"],
                "15-16": ["_tbd", "_tbd"]
            },
            "swissStage": Brackets.Swiss.initialize(formatId + "_SWISS", variation)
        }

    @staticmethod
    def addTeams(formatDict):
        formatDict["swissStage"]["teams"] = formatDict["teams"]
        formatDict["swissStage"] = Brackets.Swiss.addTeams(formatDict["swissStage"])
        return formatDict

    @staticmethod
    def checkResults(formatDict):
        formatDict["placements"].update({
            "1-2": formatDict["swissStage"]["placements"]["1-2"],
            "3-5": formatDict["swissStage"]["placements"]["3-5"],
            "6-8": formatDict["swissStage"]["placements"]["6-8"],
            "9-11": formatDict["swissStage"]["placements"]["9-11"],
            "12-14": formatDict["swissStage"]["placements"]["12-14"],
            "15-16": formatDict["swissStage"]["placements"]["15-16"]
        })
        return formatDict


class QualDay2:
    @staticmethod
    def initialize(formatId):
        return {
            "type": "QD2:16-4Q-U-32L8DSL4D-4Q",
            "current": False,
            "currentBracket": "",
            "upcomingBrackets": ["qualification"],
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
            "qualification": Brackets.B16_4Q_U_32L8DSL4D_4Q.initialize(formatId + "_QUAL", 1)
        }

    @staticmethod
    def addTeams(formatDict):
        for i in range(48 - len(formatDict["teams"])):
            formatDict["teams"].append("_bye")
        formatDict["qualification"]["teams"] = formatDict["teams"]
        formatDict["qualification"] = Brackets.B16_4Q_U_32L8DSL4D_4Q.addTeams(formatDict["qualification"])

        return formatDict

    @staticmethod
    def checkResults(formatDict):
        formatDict["placements"].update({
            "qualified": formatDict["qualification"]["placements"]["qualified"],
            "eliminated": formatDict["qualification"]["placements"]["eliminated"]
        })

        return formatDict


class OpenQualDay3:
    @staticmethod
    def initialize(formatId):
        return {
            "type": "OQD3:16-8Q-U-16L8D-8Q",
            "current": False,
            "currentBracket": "",
            "upcomingBrackets": ["qualification"],
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
            "qualification": Brackets.B16_8Q_U_16L8D_8Q.initialize(formatId + "_QUAL", 1)
        }

    @staticmethod
    def addTeams(formatDict):
        for i in range(32 - len(formatDict["teams"])):
            formatDict["teams"].append("_bye")
        formatDict["qualification"]["teams"] = formatDict["teams"]
        formatDict["qualification"] = Brackets.B16_8Q_U_16L8D_8Q.addTeams(formatDict["qualification"])
        return formatDict

    @staticmethod
    def checkResults(formatDict):
        formatDict["placements"].update({
            "qualified": formatDict["qualification"]["placements"]["qualified"],
            "eliminated": formatDict["qualification"]["placements"]["eliminated"]
        })
        return formatDict


def initializeFormat(formatType, formatId):
    if formatType == "Fall_Format":
        return FallFormat.initialize(formatId)
    elif formatType == "QualDay2":
        return QualDay2.initialize(formatId)
    elif formatType == "QualDay3":
        return Swiss.initialize(formatId, 1)
    elif formatType == "OpenQualDay3":
        return OpenQualDay3.initialize(formatId)
    elif formatType == "Invitational":
        return Swiss.initialize(formatId, 1)
    else: return {}


def addTeams(formatDict, teams):
    formatDict["teams"] = teams
    if formatDict["type"] == "Fall_Format":
        formatDict = FallFormat.addTeams(formatDict)
    elif formatDict["type"] == "Swiss":
        formatDict = Swiss.addTeams(formatDict)
    elif formatDict["type"] == "OQD3:16-8Q-U-16L8D-8Q":
        formatDict = OpenQualDay3.addTeams(formatDict)
    elif formatDict["type"] == "QD2:16-4Q-U-32L8DSL4D-4Q":
        formatDict = QualDay2.addTeams(formatDict)

    bye = True and formatDict["current"]
    while bye:
        formatDict, condition, bye = EventHandler.checkForBye(formatDict)
    return formatDict

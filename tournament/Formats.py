import tournament.Brackets as Brackets


def startFormat(formatDict):
    formatDict["current"] = True
    formatDict["currentBracket"] = formatDict["upcomingBrackets"].pop(0)
    formatDict[formatDict["currentBracket"]] = Brackets.startBracket(formatDict[formatDict["currentBracket"]])
    return formatDict


class FallFormat():
    @staticmethod
    def initialize(formatId):
        return {
            "type": "Fall_Format",
            "current": False,
            "currentBracket": "",
            "upcomingBrackets": ["playoffs"],
            "teams": [],
            "playoffs": Brackets.SE8.initialize(formatId + "_PO", 1)          #TODO current to False
        }


def initializeFormat(formatType, formatId):
    if formatType == "Fall_Format":
        return FallFormat.initialize(formatId)
    else: return {}


def loadFormat(dict, formatType):
    if formatType == "Fall_Format":
        return FallFormat(dict=dict)

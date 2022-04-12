import tournament.Brackets as Brackets


class FallFormat():
    @staticmethod
    def initialize(formatId, current):
        return {
            "type": "Fall_Format",
            "current": current,
            "currentBracket": "playoffs",                  #TODO change first
            "teams": [],
            "playoffs": Brackets.SE8.initialize(formatId + "_PO", current, 1)          #TODO current to False
        }


def initializeFormat(formatType, formatId, current):
    if formatType == "Fall_Format":
        return FallFormat.initialize(formatId, current)
    else: return {}


def loadFormat(dict, formatType):
    if formatType == "Fall_Format":
        return FallFormat(dict=dict)

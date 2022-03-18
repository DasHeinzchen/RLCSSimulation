import tournament.Brackets as Brackets


class Format:
    def __init__(self, teams=[]):
        self._teams = teams
        self._dict = {
            "teams": teams
        }

    @property
    def dict(self):
        return self._dict

    def updateDict(self, dict):
        self._dict.update(dict)


class FallFormat(Format):
    def __init__(self, id, teams=[]):
        super().__init__(teams=teams)
        self._type = "Fall_Format"
        self._playoffs = Brackets.SE8(id + "_PO", 1)

        super().updateDict({
            "playoffs": self._playoffs.dict
        })

def initializeFormat(formatType, id):
    if formatType == "Fall_Format":
        return FallFormat(id).dict
    else: return {}

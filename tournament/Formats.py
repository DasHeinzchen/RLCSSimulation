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
    def __init__(self, teams=[]):
        super().__init__(teams=teams)
        self._type = "Fall_Format"
        self._playoffs = Brackets.SE8(1)

        super().updateDict({
            "playoffs": self._playoffs.dict
        })

def initializeFormat(formatType):
    if formatType == "Fall_Format":
        return FallFormat().dict
    else: return {}

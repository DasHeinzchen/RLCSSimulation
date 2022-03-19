import tournament.Brackets as Brackets


class Format:
    def __init__(self, teams=[]):
        self._teams = teams
        self._dict = {
            "teams": teams
        }

        self._matchesToPlay = []
        self._playedMatches = []
        self._seriesToPlay = []
        self._playedSeries = []

    @property
    def dict(self):
        return self._dict

    def updateDict(self, dict):
        self._dict.update(dict)

    @property
    def teams(self):
        return self._teams

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

    def appendMatchesToPlay(self, list):
        for match in list:
            self._matchesToPlay.append(match)

    @property
    def seriesToPlay(self):
        return self._seriesToPlay

    def appendSeriesToPlay(self, list):
        for series in list:
            self._seriesToPlay.append(series)


class FallFormat(Format):
    def __init__(self, id, teams=[], current=False):
        super().__init__(teams=teams)
        self._type = "Fall_Format"
        self._playoffs = Brackets.SE8(id + "_PO", 1, current=current)   #Put current just at first Bracket of Format

        super().updateDict({
            "playoffs": self._playoffs.dict
        })

        super().appendMatchesToPlay(self._playoffs.matchesToPlay)
        super().appendSeriesToPlay(self._playoffs.seriesToPlay)


def initializeFormat(formatType, id, current=False):
    if formatType == "Fall_Format":
        return FallFormat(id, current=current).dict
    else: return {}

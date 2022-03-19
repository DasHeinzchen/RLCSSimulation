import tournament.BracketParts as Parts


class SE8:
    def __init__(self, id, variation, teams=[], current=False):
        variations = {
            1: {
                "qfbo": 7,
                "sfbo": 7,
                "fset": 3,
                "fbo": 7
            }
        }

        self._id = id
        self._teams = teams
        self._quarterFinals = Parts.QuarterFinals(id + "_QF", variations[variation]["qfbo"], current=current)
        self._currentPart = self._quarterFinals

        self._dict = {
            "id": id,
            "teams": teams,
            "quarterFinals": self._quarterFinals.dict
        }

        self._matchesToPlay = self._quarterFinals.matchesToPlay     #Add more with '+ list'
        self._playedMatches = []
        self._seriesToPlay = self._quarterFinals.seriesToPlay
        self._playedSeries = []

    @property
    def dict(self):
        return self._dict

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

    @property
    def seriesToPlay(self):
        return self._seriesToPlay

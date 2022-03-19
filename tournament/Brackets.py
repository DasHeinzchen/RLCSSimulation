import tournament.BracketParts as Parts


class SE8:
    def __init__(self, bracketId="", variation=0, teams=[], current=False, dict={}):
        variations = {
            1: {
                "qfbo": 7,
                "sfbo": 7,
                "fset": 3,
                "fbo": 7
            }
        }

        if dict == {}:
            self._id = bracketId
            self._teams = teams
            self._quarterFinals = Parts.QuarterFinals(partId=bracketId + "_QF", bo=variations[variation]["qfbo"], current=current)
            self._currentPart = self._quarterFinals

            self._dict = {
                "id": self._id,
                "teams": self._teams,
                "quarterFinals": self._quarterFinals.dict
            }
        else:
            self._dict = dict
            self._quarterFinals = Parts.QuarterFinals(dict=dict["quarterFinals"])
            self.loadFromDict()

        self._matchesToPlay = self._quarterFinals.matchesToPlay     #Add more with '+ list'
        self._playedMatches = []
        self._seriesToPlay = self._quarterFinals.seriesToPlay
        self._playedSeries = []

    def loadFromDict(self):
        self._id = self._dict["id"]
        self._teams = self._dict["teams"]

    @property
    def dict(self):
        return self._dict

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

    @property
    def seriesToPlay(self):
        return self._seriesToPlay

    @property
    def id(self):
        return self._id

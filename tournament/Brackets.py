import tournament.BracketParts as Parts
import Team


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
            self._quarterFinals = Parts.QuarterFinals(partId=bracketId + "_QF", bo=variations[variation]["qfbo"], current=current, teams=teams)
            self._semiFinals = Parts.SemiFinals(partId=bracketId + "_SF", bo=variations[variation]["sfbo"])
            self._currentPart = self._quarterFinals

            self._dict = {
                "id": self._id,
                "teams": self.teamIds(),
                "quarterFinals": self._quarterFinals.dict,
                "semiFinals": self._semiFinals.dict
            }
        else:
            self._teams = []
            self._dict = dict
            self._quarterFinals = Parts.QuarterFinals(dict=dict["quarterFinals"])
            self._semiFinals = Parts.SemiFinals(dict=dict["semiFinals"])
            self.loadFromDict()

        self._matchesToPlay = self._quarterFinals.matchesToPlay + self._semiFinals.matchesToPlay
        self._playedMatches = []
        self._seriesToPlay = self._quarterFinals.seriesToPlay + self._semiFinals.seriesToPlay
        self._playedSeries = []

    def loadFromDict(self):
        self._id = self._dict["id"]
        self.teamsFromIds(self._dict["teams"])

    def saveBracket(self):
        self._dict.update({"quarterFinals": self._quarterFinals.savePart()})
        if self._dict["quarterFinals"]["qf4"]["finished"]:
            self._semiFinals.start(self._quarterFinals.winningTeams())
        self._dict.update({"semiFinals": self._semiFinals.savePart()})

        return self._dict

    @staticmethod
    def initialize(bracketId, current, variation):
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
            "current": current,
            "currentPart": bracketId + "_QF",
            "teams": [],
            "quarterFinals": Parts.QuarterFinals.initialize(bracketId + "_QF", current, variations[variation]["qfbo"])
        }

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

    def teamIds(self):
        teamIds = []
        for team in self._teams:
            teamIds.append(team.id)
        return teamIds

    def teamsFromIds(self, ids):
        for teamId in ids:
            self._teams.append(Team.getTeamById(teamId))

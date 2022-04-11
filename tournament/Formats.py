import tournament.Brackets as Brackets
import Globals, Team


class Format:
    def __init__(self, teams=[]):
        self._teams = teams
        self._currentBracket = None

        self._dict = {
            "teams": self.teamIds()
        }

        self._matchesToPlay = []
        self._playedMatches = []
        self._seriesToPlay = []
        self._playedSeries = []

    @property
    def currentBracket(self):
        return self._currentBracket

    @currentBracket.setter
    def currentBracket(self, bracket):
        self._currentBracket = bracket

    @property
    def dict(self):
        return self._dict

    def updateDict(self, dict):
        self._dict.update(dict)

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, teams):
        self._teams = teams

    def teamIds(self):
        teamIds = []
        for team in self._teams:
            teamIds.append(team.id)
        return teamIds

    def teamsFromIds(self, ids):
        for teamId in ids:
            self._teams.append(Team.getTeamById(teamId))

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
    def __init__(self, formatId="", teams=[], current=False, dict={}):
        if dict == {}:
            super().__init__(teams=teams)
            self._type = "Fall_Format"
            self._playoffs = Brackets.SE8(bracketId=formatId + "_PO", variation=1, current=current, teams=teams)   #Put current just at first Bracket of Format
            self._currentBracket = self._playoffs

            self.updateDict({
                "currentBracket": self._currentBracket.id,
                "playoffs": self._playoffs.dict
            })
        else:
            super().__init__()
            self.updateDict(dict)
            self._playoffs = Brackets.SE8(dict=dict["playoffs"])
            self.loadFromDict()

        self.appendMatchesToPlay(self._playoffs.matchesToPlay)
        self.appendSeriesToPlay(self._playoffs.seriesToPlay)

    def loadFromDict(self):
        self._currentBracket = self.dict["currentBracket"]
        self.teamsFromIds(self.dict["teams"])

    def saveFormat(self):
        self.updateDict({"playoffs": self._playoffs.saveBracket()})
        return self.dict

    @staticmethod
    def initialize(formatId, current):
        return {
            "type": "Fall_Format",
            "current": current,
            "currentBracket": formatId + "_PO",                  #TODO change first
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

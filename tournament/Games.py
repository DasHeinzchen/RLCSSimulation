import Team
import Globals


class Match:
    def __init__(self, id="", current=False, dict={}):
        if dict == {}:
            self._id = id
            self._current = current
            self._finished = False
            self._score1 = 0
            self._score2 = 0
            self._winner = 0

            self._dict = {
                "id": self._id,
                "current": self._current,
                "finished": self._finished,
                "score1": self._score1,
                "score2": self._score2,
                "winner": self._winner
            }
        else:
            self._dict = dict
            self.loadFromDict()

        if self._current: Globals.current_match = self

    def loadFromDict(self):
        self._id = self._dict["id"]
        self._current = self._dict["current"]
        self._finished = self._dict["finished"]
        self._score1 = self._dict["score1"]
        self._score2 = self._dict["score2"]
        self._winner = self._dict["winner"]

    @property
    def score1(self):
        return self._score1

    @score1.setter
    def score1(self, score):
        self._score1 = score

    @property
    def score2(self):
        return self._score2

    @score2.setter
    def score2(self, score):
        self._score2 = score

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, winner):
        self._winner = winner

    @property
    def dict(self):
        return self._dict

    @property
    def id(self):
        return self._id


class Series:
    def __init__(self, seriesId="", bo=0, current=False, dict={}):
        if dict == {}:
            self._current = current
            self._id = seriesId
            self._team1 = Team.placeholder
            self._team2 = Team.placeholder
            self._score1 = 0
            self._score2 = 0
            self._winner = 0
            self._matchesToPlay = []
            self._playedMatches = []
            matchDicts = {}
            for i in range(int((bo + 1) / 2)):
                if self._current and i == 0:
                    self._matchesToPlay.append(Match(self._id + "_M" + str(i + 1), current=self._current))
                else:
                    self._matchesToPlay.append(Match(self._id + "_M" + str(i + 1)))
                matchDicts.update({("Match" + str(i + 1)): self._matchesToPlay[i].dict})

            self._dict = {
                "id": self._id,
                "current": self._current,
                "team1": self._team1.id,
                "team2": self._team2.id,
                "score1": self._score1,
                "score2": self._score2,
                "winner": self._winner,
                "matches": matchDicts
            }
        else:
            self._matchesToPlay = []
            self._playedMatches = []
            self._dict = dict
            matchDicts = self._dict["matches"]
            for i in range(len(matchDicts)):
                matchDict = matchDicts["Match" + str(i + 1)]
                if matchDict["finished"]:
                    self._playedMatches.append(Match(dict=matchDict))
                else:
                    self._matchesToPlay.append(Match(dict=matchDict))
            self.loadFromDict()

        if self._current: Globals.current_series = self

    def loadFromDict(self):
        self._id = self._dict["id"]
        self._current = self._dict["current"]
        self._team1 = Team.getTeamById(self._dict["team1"])
        self._team2 = Team.getTeamById(self._dict["team2"])
        self._score1 = self._dict["score1"]
        self._score2 = self._dict["score2"]
        self._winner = self._dict["winner"]

    @property
    def team1(self):
        return self._team1

    @property
    def team2(self):
        return self._team2

    @property
    def score1(self):
        return self._score1

    @property
    def score2(self):
        return self._score2

    @property
    def winner(self):
        return self._winner

    @property
    def dict(self):
        return self._dict

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

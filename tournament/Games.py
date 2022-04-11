import Team
import Globals


class Match:
    def __init__(self, id="", dict={}):
        if dict == {}:
            self._id = id
            self._finished = False
            self._score1 = 0
            self._score2 = 0
            self._winner = 0

            self.saveMatch()
        else:
            self._dict = dict
            self.loadFromDict()

    def loadFromDict(self):
        self._id = self._dict["id"]
        self._finished = self._dict["finished"]
        self._score1 = self._dict["score1"]
        self._score2 = self._dict["score2"]
        self._winner = self._dict["winner"]

    def saveMatch(self):
        self._dict = {
            "id": self._id,
            "finished": self._finished,
            "score1": self._score1,
            "score2": self._score2,
            "winner": self._winner
        }
        return self._dict

    @staticmethod
    def initialize(matchId, current):
        return {
            "id": matchId,
            "current": current,
            "score1": 0,
            "score2": 0,
            "winner": 0
        }

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
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, finished):
        self._finished = finished

    @property
    def dict(self):
        return self._dict

    @property
    def id(self):
        return self._id


class Series:
    def __init__(self, seriesId="", bo=0, current=False, dict={}, teams=[]):
        if dict == {}:
            self._current = current
            self._finished = False
            self._id = seriesId
            self._bestOf = bo
            if teams == []:
                self._team1 = Team.placeholder
                self._team2 = Team.placeholder
            else:
                self._team1 = teams[0]
                self._team2 = teams[1]
            self._score1 = 0
            self._score2 = 0
            self._winner = 0
            self._matchesToPlay = []
            self._playedMatches = []
            self._matchDicts = {}
            for i in range(int((self._bestOf + 1) / 2)):
                self._matchesToPlay.append(Match(id=self._id + "_M" + str(i + 1)))
                self._matchDicts.update({("Match" + str(i + 1)): self._matchesToPlay[i].dict})

            self.toDict()
            self._dict.update({"matches": self._matchDicts})

        else:
            self._matchesToPlay = []
            self._playedMatches = []
            self._dict = dict
            self._matchDicts = self._dict["matches"]
            for i in range(len(self._matchDicts)):
                matchDict = self._matchDicts["Match" + str(i + 1)]
                if matchDict["finished"]:
                    self._playedMatches.append(Match(dict=matchDict))
                else:
                    self._matchesToPlay.append(Match(dict=matchDict))
            self.loadFromDict()

        if self._current: Globals.current_series = self

    def loadFromDict(self):
        self._id = self._dict["id"]
        self._current = self._dict["current"]
        self._finished = self._dict["finished"]
        self._bestOf = self._dict["bestOf"]
        self._team1 = Team.getTeamById(self._dict["team1"])
        self._team2 = Team.getTeamById(self._dict["team2"])
        self._score1 = self._dict["score1"]
        self._score2 = self._dict["score2"]
        self._winner = self._dict["winner"]

    def saveSeries(self):
        self.toDict()
        self._dict.update({"matches": {}})

        if len(self._playedMatches) > 0:
            for i in range(len(self._playedMatches)):
                self._dict["matches"].update({"Match" + str(i + 1): self._playedMatches[i].saveMatch()})

        if len(self._matchesToPlay) > 0:
            length = len(self._dict["matches"])
            for i in range(len(self._matchesToPlay)):
                self._dict["matches"].update({"Match" + str(i + 1 + length): self._matchesToPlay[i].saveMatch()})
        return self._dict

    def toDict(self):
        self._dict = {
            "id": self._id,
            "current": self._current,
            "finished": self._finished,
            "bestOf": self._bestOf,
            "team1": self._team1.id,
            "team2": self._team2.id,
            "score1": self._score1,
            "score2": self._score2,
            "winner": self._winner
        }

    def submitScore(self, score1, score2):
        match = self._matchesToPlay.pop(0)
        match.score1 = score1
        match.score2 = score2
        if score1 > score2:
            match.winner = 1
            self._score1 += 1
        else:
            match.winner = 2
            self._score2 += 1

        match.finished = True
        self._playedMatches.append(match)
        if (self._score1 >= self._score2 and not len(self._matchesToPlay) == 4 - self._score1)\
                or (self._score1 <= self._score2 and not len(self._matchesToPlay) == 4 - self._score2):
            self._matchesToPlay.append(Match(id=self._id + "_M" + str(len(self._playedMatches)
                                                                      + len(self._matchesToPlay) + 1)))

        if self._score1 == int((self._bestOf + 1) / 2):
            self.seriesFinished(1)
        elif self._score2 == int((self._bestOf + 1) / 2):
            self.seriesFinished(2)

    def seriesFinished(self, winner):
        self._winner = winner

    @staticmethod
    def initialize(seriesId, current, bo):
        matches = []
        for i in range(int((bo + 1) / 2)):
            if i == 0: matches.append(Match.initialize(seriesId + "_M1", current))
            else: matches.append(Match.initialize(seriesId + "_M" + str(i + 1), False))

        return {
            "id": seriesId,
            "current": current,
            "currentMatch": seriesId + "",
            "bestOf": bo,
            "team1": Team.placeholder.id,
            "score1": 0,
            "team2": Team.placeholder.id,
            "score2": 0,
            "winner": 0,
            "matches": matches
        }

    @property
    def team1(self):
        return self._team1

    @team1.setter
    def team1(self, team):
        self._team1 = team

    @property
    def team2(self):
        return self._team2

    @team2.setter
    def team2(self, team):
        self._team2 = team

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

    @property
    def playedMatches(self):
        return self._playedMatches

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, finished):
        self._finished = finished

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current

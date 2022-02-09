import EventHandler


class Match:
    def __init__(self, team1, team2):
        self._team1 = team1
        self._team2 = team2
        self._score = [0, 0]
        self._winner = 0
        self._id = ""
        self._previousMatch = None
        self._nextMatch = None

    @property
    def team1(self):
        return self._team1

    @team1.setter
    def team1(self, team1):
        self._team1 = team1

    @property
    def team2(self):
        return self._team2

    @team2.setter
    def team2(self, team2):
        self._team2 = team2

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score
        if score[0] > score[1]:
            self._winner = 0
        else:
            self._winner = 1

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, winner):
        self._winner = winner

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def previousMatch(self):
        return self._previousMatch

    @previousMatch.setter
    def previousMatch(self, previousMatch):
        self._previousMatch = previousMatch

    @property
    def nextMatch(self):
        return self._nextMatch

    @nextMatch.setter
    def nextMatch(self, nextMatch):
        self._nextMatch = nextMatch


class Series:
    def __init__(self, team1, team2, bestOf):
        self._team1 = team1
        self._team2 = team2
        self._id = ""
        self._matchesToPlay = []
        self._finishedMatches = []
        self._score = [0, 0]
        self._winner = 0
        self._bestOf = bestOf
        self._finished = False
        self._current = False

        for i in range(int(str(self._bestOf / 2 + 0.5)[0])):
            self._matchesToPlay.append(Match(self._team1, self._team2))

    def addMatch(self, match):
        if self._finished:
            print("Can't add Match to finished Series")
        else:
            self._matches.append(match)
            self._score[match.winner] += 1
            if self._score[match.winner] > (self._bestOf / 2):
                self._finished = True
                self._winner = match.winner
                EventHandler.seriesFinished()

    @property
    def team1(self):
        return self._team1

    @team1.setter
    def team1(self, team1):
        self._team1 = team1

    @property
    def team2(self):
        return self._team2

    @team2.setter
    def team2(self, team2):
        self._team2 = team2

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, winner):
        self._winner = winner

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def matches(self):
        return self._matches

    @matches.setter
    def matches(self, matches):
        self._matches = matches

    @property
    def bestOf(self):
        return self._bestOf

    @bestOf.setter
    def bestOf(self, bestOf):
        self._bestOf = bestOf

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


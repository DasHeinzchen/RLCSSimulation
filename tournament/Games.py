import Team


class Match:
    def __init__(self, id):
        self._id = id
        self._current = False
        self._score1 = 0
        self._score2 = 0
        self._winner = 0

        self._dict = {
            "id": self._id,
            "current": self._current,
            "score1": self._score1,
            "score2": self._score2,
            "winner": self._winner
        }

    @property
    def dict(self):
        return self._dict


class Series:
    def __init__(self, id, bo):
        self._current = False
        self._id = id
        self._team1 = Team.placeholder
        self._team2 = Team.placeholder
        self._score1 = 0
        self._score2 = 0
        self._matches = []
        matchDicts = {}
        for i in range(int((bo + 1) / 2)):
            self._matches.append(Match(id + "_M" + str(i + 1)))
            matchDicts.update({("Match" + str(i + 1)): self._matches[i].dict})

        self._dict = {
            "id": self._id,
            "current": self._current,
            "team1": self._team1.id,
            "team2": self._team2.id,
            "score1": self._score1,
            "score2": self._score2,
            "matches": matchDicts
        }

    @property
    def dict(self):
        return self._dict

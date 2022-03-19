import Team
import Globals


class Match:
    def __init__(self, id, current=False):
        self._id = id
        self._current = current
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

        if current: Globals.current_match = self

    @property
    def dict(self):
        return self._dict

    @property
    def id(self):
        return self._id


class Series:
    def __init__(self, id, bo, current=False):
        self._current = current
        self._id = id
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
                self._matchesToPlay.append(Match(id + "_M" + str(i + 1), current=self._current))
            else:
                self._matchesToPlay.append(Match(id + "_M" + str(i + 1)))
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

        if current: Globals.current_series = self

    @property
    def dict(self):
        return self._dict

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

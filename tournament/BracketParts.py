from tournament import Games


class QuarterFinals:
    def __init__(self, id, bo, current=False):
        self._id = id
        self._bestOf = bo
        if current:
            self._qf1 = Games.Series(id + "_1", bo, current=True)
        else:
            self._qf1 = Games.Series(id + "_1", bo)
        self._qf2 = Games.Series(id + "_2", bo)
        self._qf3 = Games.Series(id + "_3", bo)
        self._qf4 = Games.Series(id + "_4", bo)

        self._dict = {
            "id": self._id,
            "bestOf": self._bestOf,
            "qf1": self._qf1.dict,
            "qf2": self._qf2.dict,
            "qf3": self._qf3.dict,
            "qf4": self._qf4.dict
        }

        self._matchesToPlay = []
        self._playedMatches = []
        self._seriesToPlay = [self._qf1, self._qf2, self._qf3, self._qf4]
        self._playedSeries = []

        for series in self._seriesToPlay:
            for match in series.matchesToPlay:
                self._matchesToPlay.append(match)

    @property
    def dict(self):
        return self._dict

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

    @property
    def seriesToPlay(self):
        return self._seriesToPlay

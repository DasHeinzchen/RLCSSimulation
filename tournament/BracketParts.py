from tournament import Games


class QuarterFinals:
    def __init__(self, partId="", bo=0, current=False, dict={}):
        if dict == {}:
            self._id = partId
            self._bestOf = bo
            if current:
                self._qf1 = Games.Series(seriesId=partId + "_1", bo=bo, current=True)
            else:
                self._qf1 = Games.Series(seriesId=partId + "_1", bo=bo)
            self._qf2 = Games.Series(seriesId=partId + "_2", bo=bo)
            self._qf3 = Games.Series(seriesId=partId + "_3", bo=bo)
            self._qf4 = Games.Series(seriesId=partId + "_4", bo=bo)

            self._dict = {
                "id": self._id,
                "bestOf": self._bestOf,
                "qf1": self._qf1.dict,
                "qf2": self._qf2.dict,
                "qf3": self._qf3.dict,
                "qf4": self._qf4.dict
            }

        else:
            self._dict = dict
            self._qf1 = Games.Series(dict=dict["qf1"])
            self._qf2 = Games.Series(dict=dict["qf2"])
            self._qf3 = Games.Series(dict=dict["qf3"])
            self._qf4 = Games.Series(dict=dict["qf4"])
            self.loadFromDict()

        self._matchesToPlay = []
        self._playedMatches = []
        self._seriesToPlay = [self._qf1, self._qf2, self._qf3, self._qf4]
        self._playedSeries = []

        for series in self._seriesToPlay:
            if series.finished:
                self._playedSeries.append(self._seriesToPlay.pop(0))
                for match in series.playedMatches:
                    self._playedMatches.append(match)
            else:
                for match in series.matchesToPlay:
                    if match.finished:
                        self._playedMatches.append(match)
                    else:
                        self._matchesToPlay.append(match)

    def loadFromDict(self):
        self._id = self._dict["id"]
        self._bestOf = self._dict["bestOf"]

    def savePart(self):
        self._dict.update({"qf1": self._qf1.saveSeries(), "qf2": self._qf2.saveSeries(), "qf3": self._qf3.saveSeries(),
                           "qf4": self._qf4.saveSeries()})
        return self._dict

    @property
    def dict(self):
        return self._dict

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

    @property
    def seriesToPlay(self):
        return self._seriesToPlay

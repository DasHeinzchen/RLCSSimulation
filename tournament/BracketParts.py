from tournament import Games
import Globals
import Team

class BracketPart:
    def __init__(self, dict, partId="", bo=0, current=False, teams=[]):
        if dict == {}:
            self._id = partId
            self._bestOf = bo

            self._dict = {
                "id": self._id,
                "bestOf": self._bestOf
            }
        else:
            self._dict = dict
            self.loadFromDict

        self._matchesToPlay = []
        self._playedMatches = []
        self._seriesToPlay = []
        self._playedSeries = []

    def loadFromDict(self):
        self._id = self._dict["id"]
        self._bestOf = self._dict["bestOf"]

    @property
    def dict(self):
        return self._dict

    @property
    def matchesToPlay(self):
        return self._matchesToPlay

    @property
    def seriesToPlay(self):
        return self._seriesToPlay


class QuarterFinals(BracketPart):
    def __init__(self, partId="", bo=0, current=False, dict={}, teams=[]):
        if dict == {}:
            super().__init__(dict, partId=partId, bo=bo)
            if teams == []:
                if current:
                    self._qf1 = Games.Series(seriesId=partId + "_1", bo=bo, current=True)
                else:
                    self._qf1 = Games.Series(seriesId=partId + "_1", bo=bo)
                self._qf2 = Games.Series(seriesId=partId + "_2", bo=bo)
                self._qf3 = Games.Series(seriesId=partId + "_3", bo=bo)
                self._qf4 = Games.Series(seriesId=partId + "_4", bo=bo)
            else:
                if current:
                    self._qf1 = Games.Series(seriesId=partId + "_1", bo=bo, current=True, teams=[teams[0], teams[7]])
                else:
                    self._qf1 = Games.Series(seriesId=partId + "_1", bo=bo, teams=[teams[0], teams[7]])
                self._qf2 = Games.Series(seriesId=partId + "_2", bo=bo, teams=[teams[1], teams[6]])
                self._qf3 = Games.Series(seriesId=partId + "_3", bo=bo, teams=[teams[2], teams[5]])
                self._qf4 = Games.Series(seriesId=partId + "_4", bo=bo, teams=[teams[3], teams[4]])

            self._dict.update({
                "qf1": self._qf1.dict,
                "qf2": self._qf2.dict,
                "qf3": self._qf3.dict,
                "qf4": self._qf4.dict
            })

        else:
            super().__init__(dict)
            self._qf1 = Games.Series(dict=dict["qf1"])
            self._qf2 = Games.Series(dict=dict["qf2"])
            self._qf3 = Games.Series(dict=dict["qf3"])
            self._qf4 = Games.Series(dict=dict["qf4"])

        self._seriesToPlay.extend([self._qf1, self._qf2, self._qf3, self._qf4])

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

    def savePart(self):
        if (len(self._qf1.matchesToPlay) == 0 and not self._qf2.current and not self._qf3.current and not self._qf4.current)\
                or (len(self._qf2.matchesToPlay) == 0 and not self._qf3.current and not self._qf4.current)\
                or (len(self._qf3.matchesToPlay) == 0 and not self._qf4.current):
            self._seriesToPlay[0].finished = True
            self._playedSeries.append(self._seriesToPlay.pop(0))
            self._seriesToPlay[0].current = True
            Globals.current_series = self._seriesToPlay[0]
        elif len(self._qf4.matchesToPlay) == 0:
            self._seriesToPlay[0].finished = True
        self._dict.update({"qf1": self._qf1.saveSeries(), "qf2": self._qf2.saveSeries(), "qf3": self._qf3.saveSeries(),
                           "qf4": self._qf4.saveSeries()})

        return self._dict

    def winningTeams(self, seeded=True):
        teams = [Team.getTeamById(self._dict["qf1"]["team" + str(self._dict["qf1"]["winner"])]),
                 Team.getTeamById(self._dict["qf2"]["team" + str(self._dict["qf2"]["winner"])]),
                 Team.getTeamById(self._dict["qf3"]["team" + str(self._dict["qf3"]["winner"])]),
                 Team.getTeamById(self._dict["qf4"]["team" + str(self._dict["qf4"]["winner"])])]
        if seeded:
            teams.insert(1, teams.pop(3))
            return teams
        else:
            return teams

    @staticmethod
    def initialize(partId, current, bo):
        return {
            "id": partId,
            "current": current,
            "currentSeries": partId + "_1",
            "bestOf": bo,
            "teams": [],
            "qf1": Games.Series.initialize(partId + "_1", current, bo),
            "qf2": Games.Series.initialize(partId + "_2", False, bo),
            "qf3": Games.Series.initialize(partId + "_3", False, bo),
            "qf4": Games.Series.initialize(partId + "_4", False, bo)
        }


class SemiFinals(BracketPart):
    def __init__(self, partId="", bo=0, current=False, dict={}, teams=[]):
        if dict == {}:
            super().__init__(dict, partId=partId, bo=bo)

            if teams == []:
                if current:
                    self._sf1 = Games.Series(seriesId=partId + "_1", bo=bo, current=True)
                else:
                    self._sf1 = Games.Series(seriesId=partId + "_1", bo=bo)
                self._sf2 = Games.Series(seriesId=partId + "_2", bo=bo)
            else:
                if current:
                    self._sf1 = Games.Series(seriesId=partId + "_1", bo=bo, current=True, teams=[teams[0], teams[3]])
                else:
                    self._sf1 = Games.Series(seriesId=partId + "_1", bo=bo, teams=[teams[0], teams[3]])
                self._sf2 = Games.Series(seriesId=partId + "_2", bo=bo, teams=[teams[1], teams[2]])

            self._dict = {
                "sf1": self._sf1.dict,
                "sf2":  self._sf2.dict
            }
        else:
            super().__init__(dict)
            self._sf1 = Games.Series(dict=dict["sf1"])
            self._sf2 = Games.Series(dict=dict["sf2"])

        self._seriesToPlay.extend([self._sf1, self._sf2])

    def savePart(self):
        if len(self._sf1.matchesToPlay) == 0 and not self._sf2.current:
            self._seriesToPlay[0].finished = True
            self._playedSeries.append(self._seriesToPlay.pop(0))
            self._seriesToPlay[0].current = True
            Globals.current_series = self._seriesToPlay[0]
        elif len(self._sf2.matchesToPlay) == 0:
            self._seriesToPlay[0].finished = True
        self._dict.update({"sf1": self._sf1.saveSeries(), "sf2": self._sf2.saveSeries()})
        return self._dict

    def start(self, teams):
        self._sf1.team1, self._sf1.team2 = teams[0], teams[3]
        self._sf2.team1, self._sf1.team2 = teams[1], teams[2]
        self._sf1.current = True
        self._seriesToPlay = [self._sf1, self._sf2]
        Globals.current_series = self._seriesToPlay[0]

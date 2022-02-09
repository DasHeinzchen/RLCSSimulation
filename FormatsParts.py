
import Games

class Final:
    def __init__(self, seededTeams, bestOfSeries, bestOfSet=1):
        self._teams = seededTeams
        self._bestOfSeries = bestOfSeries
        self._bestOfSet = bestOfSet
        self._seriesToPlay = []
        self._finishedSeries = []

        for i in range(int(str(self._bestOfSet / 2 + 0.5)[0])):
            self._seriesToPlay.append(Games.Series(self._teams[0], self._teams[1], self._bestOfSeries))

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, seededTeams):
        self._teams = seededTeams



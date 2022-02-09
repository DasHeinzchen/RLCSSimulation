import Games
import random

class SingleEliminationBracket8Team:
    def __init__(self, teams, bestOf, seeding=None):
        self._series = [[], [], []]     #Quarterfinals, Semifinals, Finals
        self._teams = teams
        self._placements = [[], [], None, None]   #5th-8th, 3rd-4th, 2nd, 1st
        self._seeding = seeding
        self._bestOf = bestOf


    def initializeQuarterfinals(self):
        if self._seeding == None:
            for i in range(4):
                self._series[0].append(Games.Series(self._teams[i], self._teams[7 - i], self._bestOf[0]))
        else:
            for i in range(4):
                self._series[0].append(
                    Games.Series(self._teams[self._seeding.Index(i + 1)], self._teams[self._seeding.Index(8 - i)], self._bestOf[0]))


    def initializeHalfFinals(self):
        self._series[1].append(Games.Series(self._series[0][0].winner[1], self._series[0][1].winner[1], self._bestOf[1]))
        self._series[1].append(Games.Series(self._series[0][2].winner[1], self._series[0][3].winner[1], self._bestOf[1]))


    def initializeFinals(self):
        for i in range(self._bestOf[2][0]):
            self._series[2] = Games.Series(self._series[1][0].winner[1], self._series[1][1].winner[1], self._bestOf[2][1])


class SwissSystem:
    def __init__(self, teams, bestOf, seeding=None):
        self._series = [[], [[], []], [[], [], []], [[], []], []]     #Round 1 - Round 5
        self._teams = teams
        self._placements = [[], [], [], [], [], []]     #15th-16th, 12th-14th, 9th-11th, 6th-8th, 3rd-5th, 1st-2nd
        self._seeding = seeding
        self._bestOf = bestOf
        self._placementsR1 = [[], []]   #Higher, Lower
        self._placementsR2 = [[], [], []]   #Higher, Mid, Lower
        self._placementsR3 = [[], []]   #Higher, Lower
        self._placementsR4 = []


    def initializeRound1(self):
        if self._seeding == None:
            for i in range(8):
                self._series[0].append(Games.Series(self._teams[i], self._teams[15-i], self._bestOf))
        else:
            for i in range(8):
                self._series[0].append(Games.Series(self._teams[self._seeding.Index(i + 1)], self._teams[self._seeding.Index(16 - i)], self._bestOf))

    def initializeRound2(self):
        random.shuffle(self._placementsR1[0])
        random.shuffle(self._placementsR1[1])

        for i in range(4):
            self._series[1][0].append(Games.Series(self._placementsR1[0][i], self._placementsR1[0][7-i], self._bestOf))
            self._series[1][1].append(Games.Series(self._placementsR1[1][i], self._placementsR1[1][7-i], self._bestOf))


    def initializeRound3(self):
        random.shuffle(self._placementsR2[0])
        random.shuffle(self._placementsR2[1])
        random.shuffle(self._placementsR2[2])

        for i in range(2):
            self._series[2][0].append(Games.Series(self._placementsR2[0][i], self._placementsR2[0][3-i], self._bestOf))
            self._series[2][2].append(Games.Series(self._placementsR2[2][i], self._placementsR2[2][3-i], self._bestOf))

        for i in range(4):
            self._series[2][1].append(Games.Series(self._placementsR2[1][i], self._placementsR2[1][7-i], self._bestOf))


    def initializeRound4(self):
        random.shuffle(self._placementsR3[0])
        random.shuffle(self._placementsR3[1])

        for i in range(3):
            self._series[3][0].append(Games.Series(self._placementsR3[0][i], self._placementsR3[0][5-i], self._bestOf))
            self._series[3][1].append(Games.Series(self._placementsR3[1][i], self._placementsR3[1][5-i], self._bestOf))


    def intitializeRound5(self):
        random.shuffle((self._placementsR4))

        for i in range(3):
            self._series[4].append(Games.Series(self._placementsR4[i], self._placementsR4[5-i], self._bestOf))


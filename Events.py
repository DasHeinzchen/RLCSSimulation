import Formats


class FallEvent:
    def __init__(self, teams, seeding=None):
        self._swiss = Formats.SwissSystem(teams, 3, seeding)
        self._playoffs = Formats.SingleEliminationBracket8Team(teams, [5, 5,[3, 7]])
        self._teams = teams
        self._placements = [[], [], [], [], [], None, None]     #15th - 16th, 12th-14th, 9th-11th, 5th-8th, 3rd-4th, 2nd, 1st

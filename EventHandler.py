import Globals
import Team
import structure.Season as Season


def addMatchScore(score):
    Globals.current_match.score = score
    Globals.current_series.addMatch(Globals.current_match)


def seriesFinished():
    print()


def close():
    Team.saveAllTeamData()
    Season.getSeasonById(Globals.current_season).saveData()


def initializeSeason():
    Season.addSeason()

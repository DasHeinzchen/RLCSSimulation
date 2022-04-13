import Globals
import Team
from structure import Season, Split, Major
from tournament import Brackets, BracketParts, Formats, Games


def close():
    Team.saveAllTeamData()


def initializeSeason():
    Season.setupSeason()
    Season.Season(Globals.current_season).start()


def load():
    season = Season.Season(Globals.current_season)
    split = Split.Split(season.currentSplit)
    event = None
    if split.currentEvent[-3:] == "MJR":
        event = Major.Major(split.currentEvent)

    return season, split, event


def loadFormat(format):
    bracket = format[format["currentBracket"]]
    bracketPart = bracket[bracket["currentPart"]]
    series = bracketPart[bracketPart["currentSeries"]]
    match = series["matches"][series["currentMatch"]]

    return bracket, bracketPart, series, match


def submitScore(score1, score2, formatDict):
    bracket, bracketPart, series, match = loadFormat(formatDict)
    condition = False
    sideCondition = False
    match = Games.Match.submitScore(score1, score2, match)
    series, condition = Games.Series.submitScore(series, match)
    sideCondition += condition
    bracketPart, condition = BracketParts.submitScore(bracketPart, series, condition)
    if sideCondition:
        bracket, condition = Brackets.submitScore(bracket, bracketPart, condition)
        bracket = Brackets.checkResults(bracket)
    else:
        bracket, condition = Brackets.submitScore(bracket, bracketPart, condition)
    formatDict[formatDict["currentBracket"]] = bracket

    return formatDict

import Globals
import Team
from structure import Season, Split, Major, Regional, Qualification
from tournament import Brackets, BracketParts, Formats, Games


def close():
    Team.saveAllTeamData()


def initializeSeason(dictionaryQual):
    Season.setupSeason(dictionaryQual)
    Season.Season(Globals.current_season).start()


def load():
    season = Season.Season(Globals.current_season)
    split = Split.Split(season.currentSplit)
    event = None
    if split.currentEvent[-3:] == "MJR":
        event = Major.Major(split.currentEvent)
    elif split.currentEvent[-4:-1] == "REG":
        event = Regional.Regional(split.currentEvent)
    elif split.currentEvent[-5:-1] == "QUAL" or split.currentEvent[-5:] == "INVIT":
        event = Qualification.QualDay(split.currentEvent)

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
    if bool(sideCondition):
        bracket, condition = Brackets.submitScore(bracket, bracketPart, condition)
        bracket = Brackets.checkResults(bracket)
    else:
        bracket, condition = Brackets.submitScore(bracket, bracketPart, condition)
    formatDict, sideCondition = Formats.submitScore(formatDict, bracket, condition)

    bye = True
    while bye:
        formatDict, condition, bye = checkForBye(formatDict)

    return formatDict, condition or sideCondition


def checkForBye(formatDict):
    bracket, bracketPart, series, match = loadFormat(formatDict)
    if series["team1"] == "_bye" or series["team2"] == "_bye":
        if series["team1"] == "_bye": series["winner"] = 2
        elif series["team2"] == "_bye": series["winner"] = 1
        series["current"] = False
        series["currentMatch"] = -1
        series["matches"] = []

        bracketPart, condition = BracketParts.submitScore(bracketPart, series, True)
        bracket, condition = Brackets.submitScore(bracket, bracketPart, condition)
        bracket = Brackets.checkResults(bracket)
        formatDict, condition = Formats.submitScore(formatDict, bracket, condition)
        return formatDict, condition, True
    else:
        return formatDict, False, False


def eventFinished():
    season, split, event = load()
    event.finish()
    if event.formatType == "OpenQualDay3":
        regional = Regional.Regional(event.id[:-6])
        regional.teams = event.qualifiedTeams
        regional.seeding()
    condition = split.nextEvent() #Condition: True if last event of split finished

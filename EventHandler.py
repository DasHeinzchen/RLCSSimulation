import Globals
import Team
from structure import Season, Split, Major


def matchFinished():
    Globals.format.saveFormat()


def close():
    Team.saveAllTeamData()
    Season.getSeasonById(Globals.current_season).saveData()
    split = Split.getSplitById(Globals.current_split)
    split.saveData()

    eventId = split.currentEvent
    eventId = eventId.split("_")
    if eventId[2] == "MJR":
        event = Major.getMajorById(eventId[0] + "_" + eventId[1] + "_" + eventId[2])
        event.saveData()


def initializeSeason():
    Season.addSeason()

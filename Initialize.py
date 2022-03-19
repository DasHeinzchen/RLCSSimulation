import Gui
import Globals
import Team
import json
from structure import Season, Split, Major
from tournament import Formats


with open("settings.json") as config_file:
    Globals.settings = json.load(config_file)

Team.readTeamsJson()
Season.readSeasonsJson()
if not Globals.current_season == "":
    season = Season.getSeasonById(Globals.current_season)
    for splitId in season.splits:
        split = Split.getSplitById(splitId)
        if split.current:
            Globals.current_split = splitId

            eventId = split.currentEvent
            eventId = eventId.split("_")
            if eventId[2] == "MJR":
                event = Major.getMajorById(eventId[0] + "_" + eventId[1] + "_" + eventId[2])
                format = Formats.loadFormat(event.dict["format"], event.formatType)

        del split

window = Gui.MainWindow()

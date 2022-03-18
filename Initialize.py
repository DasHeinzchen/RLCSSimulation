import Gui
import Globals
import Team
import json
import structure.Season as Season


with open("settings.json") as config_file:
    Globals.settings = json.load(config_file)

Team.readTeamsJson()
Season.readSeasonsJson()
if not Globals.current_season == "":
    Season.getSeasonById(Globals.current_season)

window = Gui.MainWindow()

import Gui
import Globals
import Team
import json
from structure import Season


with open("settings.json") as config_file:
    Globals.settings = json.load(config_file)

Team.readTeamsJson()
Season.readSeasonsJson()

window = Gui.MainWindow()

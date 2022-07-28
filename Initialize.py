import Gui
import Globals
import Log
import Team
import json
from structure import Season

Log.new("i", "Program started")

with open("settings.json") as config_file:
    Log.new("i", "Loading config file")
    Globals.settings = json.load(config_file)
    if Globals.settings is None: Log.new("e", "No settings imported")

Team.readTeamsJson()
Season.readSeasonsJson()

window = Gui.MainWindow()

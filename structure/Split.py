import os
import Globals
import json

class Split:
    def __init__(self, id="", current=False, name=""):
        self._dict = {}
        self._id = id
        self._current = current
        self._name = name

    def loadData(self):
        if not os.path.isfile(Globals.settings["path"] + "seasons\\" + self._id + "\\" + self._id + ".json"):
            file = open(Globals.settings["path"] + "seasons\\" + self._id + "\\" + self._id + ".json", "a")
            file.write("{}")
            file.close()
        else:
            file = open(Globals.settings["path"] + "seasons\\" + self._id + "\\" + self._id + ".json")
            self._dict = json.load(file)

            file.close()

    def saveData(self):
        print()


def initializeSplit(id):
    id = id.split("_")
    os.mkdir(Globals.settings["path"] + "seasons\\" + id[0] + "\\" + id[1])
    file = open(Globals.settings["path"] + "seasons\\" + id[0] + "\\" + id[1] + "\\" + id[1] + ".json", "a")
    file.write("{}")
    file.close()

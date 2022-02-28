import Globals
import json

class Major:
    def __init__(self, id="", current=False, name=""):
        self._id = id
        self._current = current
        self._name = name
        self._teams = [] #seeded
        self._dict = {}

    def loadData(self):
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[2] + ".json")
        self._dict = json.load(file)

        self._id = self._dict["id"]
        self._current = self._dict["current"]
        self._name = self._dict["name"]

        file.close()

    def saveData(self):
        self._dict.update({"id": self._id, "current": self._current, "name": self._name})
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[2] + ".json", "w")
        file.write(json.dumps(self._dict, indent=5))
        file.close()


def initializeMajor(id):
    id = id.split("_")
    file = open(Globals.settings["path"] + "seasons\\" + id[0] + "\\" + id[1] + "\\" + id[2] + ".json", "a")
    file.write("{}")
    file.close()
    id = id[0] + "_" + id[1] + "_" + id[2]
    Major(id=id).saveData()
import Globals
import json

class Major:
    def __init__(self, id="", current=False, name="", formatType=""):
        self._id = id
        self._current = current
        self._name = name
        self._teams = [] #seeded
        self._formatType = formatType
        self._dict = {}

    def loadData(self):
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[2] + ".json")
        self._dict = json.load(file)

        self._id = self._dict["id"]
        self._current = self._dict["current"]
        self._name = self._dict["name"]
        self._formatType = self._dict["formatType"]

        file.close()

    def saveData(self):
        self._dict.update({
            "id": self._id,
            "current": self._current,
            "name": self._name,
            "formatType": self._formatType
        })
        file = open(Globals.settings["path"] + "seasons\\" + self._id.split("_")[0] + "\\" + self._id.split("_")[1] + "\\" + self._id.split("_")[2] + ".json", "w")
        file.write(json.dumps(self._dict, indent=5))
        file.close()


def initializeMajor(id):
    id = id.split("_")
    file = open(Globals.settings["path"] + "seasons\\" + id[0] + "\\" + id[1] + "\\" + id[2] + ".json", "a")
    file.write("{}")
    file.close()
    splitNbr = int(id[1][3:])
    format = ""
    if splitNbr == 1: format = "Fall_Format"
    elif splitNbr == 2: format = "Winter_Format"
    elif splitNbr == 3: format = "Spring_Format"
    id = id[0] + "_" + id[1] + "_" + id[2]
    Major(id=id, formatType=format).saveData()

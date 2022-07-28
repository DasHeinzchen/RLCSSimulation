from datetime import datetime

import Globals


class LogItem:
    def __init__(self, key, message):
        self._key = key
        self._message = message
        self._time = str(datetime.now())

    def __str__(self):
        return "[" + self._time + "] [" + self._key + "]  " + self._message


logs = []


def new(key, message):
    if key == "i":
        key = "INFO"
    elif key == "w":
        key = "WARNING"
    elif key == "e":
        key = "ERROR"
        print(message)
    logs.append(LogItem(str(key), str(message)))


def message(message):
    print(message)
    logs.append(LogItem("PRINT", str(message)))


def saveLog():
    new("i", "Saving logs")
    path = Globals.settings["path"] + "logs\\Log" + str(datetime.now()).replace(".", ":").replace(":", "-")
    with open(path + ".txt", "a") as logFile:
        for log in logs:
            logFile.write(str(log) + "\n")

        logFile.close()


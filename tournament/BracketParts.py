from tournament import Games
import Globals
import Team

class BracketPart:
    @staticmethod
    def submitScore(partDict, seriesDict, condition):
        partDict[partDict["currentSeries"]] = seriesDict
        if condition:
            if len(partDict["upcomingSeries"]) > 0:
                partDict["currentSeries"] = partDict["upcomingSeries"].pop(0)
                partDict[partDict["currentSeries"]]["current"] = True
                partDict[partDict["currentSeries"]]["matches"][partDict[partDict["currentSeries"]]["currentMatch"]]["current"] = True
                return partDict, False
            else:
                return partDict, True
        else:
            return partDict, False


class QuarterFinals(BracketPart):
    @staticmethod
    def initialize(partId, current, bo):
        return {
            "id": partId,
            "current": current,
            "currentSeries": "qf1",
            "upcomingSeries": ["qf2", "qf3", "qf4"],
            "bestOf": bo,
            "teams": [],
            "qf1": Games.Series.initialize(partId + "_1", current, bo),
            "qf2": Games.Series.initialize(partId + "_2", False, bo),
            "qf3": Games.Series.initialize(partId + "_3", False, bo),
            "qf4": Games.Series.initialize(partId + "_4", False, bo)
        }


class SemiFinals(BracketPart):
    @staticmethod
    def initialize(partId, current, bo):
        return {

        }

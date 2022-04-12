import tournament.BracketParts as Parts


class SE8:
    @staticmethod
    def initialize(bracketId, current, variation):
        variations = {
            1: {
                "qfbo": 7,
                "sfbo": 7,
                "fset": 3,
                "fbo": 7
            }
        }
        return {
            "id": bracketId,
            "current": current,
            "currentPart": "quarterFinals",
            "teams": [],
            "quarterFinals": Parts.QuarterFinals.initialize(bracketId + "_QF", current, variations[variation]["qfbo"])
        }

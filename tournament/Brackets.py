import tournament.BracketParts as Parts


class SE8:
    def __init__(self, id, variation, teams=[]):
        variations = {
            1: {
                "qfbo": 7,
                "sfbo": 7,
                "fset": 3,
                "fbo": 7
            }
        }

        self._id = id
        self._teams = teams
        self._quarterFinals = Parts.QuarterFinals(id + "_QF", variations[variation]["qfbo"])

        self._dict = {
            "id": id,
            "teams": teams,
            "quarterFinals": self._quarterFinals.dict
        }

    @property
    def dict(self):
        return self._dict

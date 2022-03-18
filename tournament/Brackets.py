import tournament.BracketParts as Parts


class SE8:
    def __init__(self, variation, teams=[]):
        variations = {
            1: {
                "qfbo": 7,
                "sfbo": 7,
                "fset": 3,
                "fbo": 7
            }
        }

        self._teams = teams
        self._quarterFinals = Parts.QuarterFinals(variations[variation]["qfbo"])

        self._dict = {
            "teams": teams,
            "quarterFinals": self._quarterFinals.dict
        }

    @property
    def dict(self):
        return self._dict

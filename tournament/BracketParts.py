import Games


class QuarterFinals:
    def __init__(self, bo):
        self._bestOf = bo
        self._dict = {}

    @property
    def dict(self):
        return self._dict

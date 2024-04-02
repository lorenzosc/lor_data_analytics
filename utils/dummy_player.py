from player import Player
import itertools

class DummyPlayer(Player):

    id_above_all_player_numbers = 1000000000
    id_iter = itertools.count(id_above_all_player_numbers)

    def __init__ (
        self
    ):
        super().__init__(name="Dummy", strategy = None, score=0)
        self.id = next(self.id_iter)
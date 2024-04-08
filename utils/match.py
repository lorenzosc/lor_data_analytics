from .player import Player
from .dummy_player import DummyPlayer
import random

class Match:

    player1: Player
    player2: Player
    status: str
    result: int

    def __init__ (
        self, player1: Player, player2: Player
    ):
        self.player1 = player1
        self.player2 = player2
        self.status = "ongoing"
        self.result = None

    def get_result (
        self
    ) -> int:
        return self.result
    
    def get_status (
        self
    ) -> str:
        return self.status
    
    # Virtual method
    def resolve (
        self
    ) -> None:
        if isinstance(self.player1, DummyPlayer):
            self.result = 1
        elif isinstance(self.player2, DummyPlayer):
            self.result = 0
        else:
            self.result = random.randint(0, 2)
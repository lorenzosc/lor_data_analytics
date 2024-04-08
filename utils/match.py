from .player import Player
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
        self.result = random.randint(0, 2)
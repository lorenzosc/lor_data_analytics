from player import Player

class Match:

    player1: Player
    player2: Player
    status: str
    result: tuple[int,int]

    def __init__ (
        self, player1: Player, player2: Player
    ):
        self.player1 = player1
        self.player2 = player2
        self.status = "ongoing"
        self.result = None

    def get_result (
        self
    ) -> tuple[int,int]:
        return self.result
    
    def get_status (
        self
    ) -> str:
        return self.status
    
    def resolve (
        self
    ) -> None:
        pass
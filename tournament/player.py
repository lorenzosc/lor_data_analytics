from utils.lineup import Lineup

class Player():
    
    id: int
    strategy: Lineup
    score: int
    opponent_list: list
    
    def __init__(
            self, strategy: Lineup, score: int = 0, opponent_list: list = []
            ):
        self.strategy = strategy
        self.score = score
        self.opponent_list = opponent_list

    def decks (
        self
    ):
        return self.strategy.decks()
    
    def update_score (
            self, new_score: int
    ) -> None:
        self.score = new_score
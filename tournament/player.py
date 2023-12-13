from lineup import Lineup

class Player():
    
    id: int
    lineup: Lineup
    score: int
    opponent_list: list
    
    def __init__(
            self, lineup: Lineup, score: int = 0, opponent_list: list = []
            ):
        self.lineup = lineup
        self.score = score
        self.opponent_list = opponent_list

    def decks (
        self
    ):
        return self.lineup.decks()
    
    def update_score (
            self, new_score: int
    ) -> None:
        self.score = new_score
from typing import Any
import itertools

class Player():
    
    id: int
    id_iter: int = itertools.count()
    name: str
    strategy: Any
    score: int
    
    def __init__(
            self, name: str, strategy: Any, score: int = 0
        ):
        self.id = next(Player.id_iter)
        self.name = name
        self.strategy = strategy
        self.score = score
    
    def change_score (
        self, score_change: int
    ) -> None:
        self.score += score_change

    def get_score (
        self
    ) -> int:
        return self.score
    
    def get_id (
        self
    ) -> int:
        return self.id

    def set_score (
            self, new_score: int
    ) -> None:
        self.score = new_score
    
    def get_strategy (
        self
    ) -> Any:
        return self.strategy
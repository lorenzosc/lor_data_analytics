from utils.player import Player
from utils.match import Match
from .swiss_tournament import SwissTournament

class SwissTournamentSimulator(SwissTournament):

    number_of_rounds: int
    players: dict[int, Player]
    standings: list[list[int]]
    player_adversaries: dict[int,list[int]]
    bye: Player
    current_round: int
    number_players: int
    dropped_players: dict[int,bool]
    rounds: list[list[tuple[int,int]]]

    def __init__ (
        self, players: list[Player], current_round = 0
    ):
        super().__init__(players, current_round)

    def execute_round (
        self
    ) -> None:
        
        players = self.number_players-1 + self.dropped_players[self.bye.get_id()] - sum(self.dropped_players.values())

        if players % 2 == 0 and not self.dropped_players[self.bye.get_id()]:
            self.drop_player(self.bye.get_id())
        if players % 2 == 1 and self.dropped_players[self.bye.get_id()]:
            self.undrop_player()    
        
        self.make_round()

        matches = [Match(self.players[match[0]], self.players[match[1]]) for match in self.rounds[-1]]

        for new_match in matches:
            p1 = new_match.player1
            p2 = new_match.player2
            new_match.resolve()
            result = new_match.get_result()

            if result == 0:
                self.update_player_score(p1.get_id(), 2)
            elif result == 1:
                self.update_player_score(p2.get_id(), 2)
            elif result == 2:
                self.update_player_score(p1.get_id(), 1)
                self.update_player_score(p2.get_id(), 1)

            self.update_adversaries(p1.get_id(), p2.get_id())
        
    def run (
        self
    ) -> None:
        
        while (self.number_of_rounds > self.current_round):
            self.current_round += 1

            new_players = []
            for player in new_players:
                self.add_player(player)

            dropping_players = []
            for player in dropping_players:
                self.drop_player(player)
            
            self.execute_round()

        print(self.view_standings())
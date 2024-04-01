from utils.player import Player
import math

class SwissTournament():

    number_of_rounds: int
    players: dict[int, Player]
    standings: list[list[int]]
    player_adversaries: list[list[int]]
    current_round: int
    number_players: int
    dropped_players: list[bool]

    def __init__ (
        self, players: list[Player], current_round = 0
    ):
        self.number_of_rounds = math.ceil(math.log2(len(players)))

        self.players = {}
        self.standings = [ [] for _ in range(3*self.number_of_rounds)] # Most tournaments won't go above 3 points per round
        for player in players:
            self.players[player.get_id()] = player
            self.standings[player.get_score()].append(player)

        self.number_players = len(self.players)
        self.player_adversaries = [ [] for _ in range(self.number_players)]

        self.current_round = current_round

        self.dropped_players = [ False for _ in range(self.number_players) ]

    def make_round (
            
    ):
        pass

    def view_standings (
            
    ):
        pass
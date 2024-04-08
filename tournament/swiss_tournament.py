from utils.player import Player
from utils.dummy_player import DummyPlayer
import math
from utils.graph.blossom import Blossom

class SwissTournament():

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
        self.number_of_rounds = math.ceil(math.log2(len(players)))

        self.players = {}
        self.number_players = 0
        self.player_adversaries = {}
        self.dropped_players = {}
        self.standings = [ [] for _ in range(3*self.number_of_rounds)] # Most tournaments won't go above 3 points per round
        for player in players:
            self.add_player(player)

        dummy = DummyPlayer()
        self.bye = dummy
        self.add_player(dummy)

        self.current_round = current_round
        self.rounds = []
    
    def make_round (
        self
    ) -> None:
        
        matches = []
        players_separed_by_points = [standing.copy() for standing in self.standings if standing]
        players_separed_by_points.reverse()
        for ind, points in enumerate(players_separed_by_points):
            if len(points) % 2 == 1 and ind == len(players_separed_by_points)-1:
                raise ValueError("Too many points")

            if len(points) % 2 == 1:
                matched_below_player = self.find_lower_standing_neighbors(ind, players_separed_by_points)
                points.remove(matched_below_player)
                players_separed_by_points[ind+1].append(matched_below_player)

            player_to_node = {player: ind for ind, player in enumerate(points)}
            node_to_player = {ind: player for ind, player in enumerate(points)}
            number_vertex = len(player_to_node)
            edges = []

            for node in node_to_player:
                for opponent in self.player_adversaries[node_to_player[node]]:
                    if opponent in player_to_node:
                        edges.append((node, player_to_node[opponent], 0))

            graph = Blossom(number_vertex, edges)
            matching, non_matched = graph.maximum_matching()

            for player in non_matched:
                points.remove(player)
                players_separed_by_points[ind+1].append(player)

            for face_off in matching:
                p1 = face_off[0]
                p2 = face_off[1]
                matches.append((node_to_player[p1], node_to_player[p2]))

        self.rounds.append(matches)

    def find_lower_standing_neighbors (
        self, standing: int, player_separated_by_points: list
    ) -> int:
        min_opponents = self.number_players
        matched_below_player = -1

        for player in player_separated_by_points[standing]:
            cur_previous_opponent = 0
            for previous_opponent in self.player_adversaries[player]:
                if previous_opponent in player_separated_by_points[standing+1]:
                    cur_previous_opponent += 1

            if cur_previous_opponent < min_opponents:
                min_opponents = cur_previous_opponent
                matched_below_player = player
            
        return matched_below_player

    def drop_player (
        self, player_id: int
    ) -> None:
        self.dropped_players[player_id] = True
        self.standings[self.players[player_id].get_score()].remove(player_id)

    def undrop_player (
        self, player_id: int = None
    ) -> None:
        if player_id == None:
            player_id = self.bye.get_id()
        
        self.dropped_players[player_id] = False
        self.standings[self.players[player_id].get_score()].append(player_id)

    def update_player_score (
        self, player_id: int, score_change: int
    ) -> None:
        self.standings[self.players[player_id].get_score()].remove(player_id)
        self.players[player_id].update_score(score_change)
        self.standings[self.players[player_id].get_score()].append(player_id)

    def set_player_score (
        self, player_id: int, new_score: int
    ) -> None:
        self.standings[self.players[player_id].get_score()].remove(player_id)
        self.players[player_id].set_score(new_score)
        self.standings[self.players[player_id].get_score()].append(player_id)

    def update_adversaries (
        self, player1: int, player2: int
    ) -> None:
        self.player_adversaries[player1].append(player2)
        self.player_adversaries[player2].append(player1)

    def view_standings (
        self
    ) -> list[tuple[int]]:
        highest_to_lowest = []

        for player_id, player in self.players.items():
            opp_points = 0

            for opp in self.player_adversaries[player_id]:
                opp_points += self.players[opp].get_score()
            
            player_info = (player_id, player.get_score(), opp_points)
            highest_to_lowest.append(player_info)

        highest_to_lowest = sorted(highest_to_lowest, key= lambda x: (x[1], x[2]), reverse=True)

        return highest_to_lowest

    def execute_round (
        self
    ) -> None:
        pass
        
    def run (
        self
    ) -> None:
        pass

    def add_player (
        self, player: Player
    ) -> None:
        
        if player.get_score() < 0 or player.get_score() >= 3* self.number_of_rounds:
            raise AttributeError("Player score can't be negative or higher than limit")
        
        self.players[player.get_id()] = player
        self.standings[player.get_score()].append(player.get_id())
        self.player_adversaries[player.get_id()] = []
        self.dropped_players[player.get_id()] = False
        self.number_players += 1
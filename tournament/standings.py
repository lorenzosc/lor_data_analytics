from player import Player

class Standings():

    players: list
    standings: dict

    def __init__ (
            self, players: list
            ) -> None:
        self.players = players
        self.standings = {}

    def update_round (
            self, players: list
            ):
        for player in players:
            self.update_player_standing(player)

    def update_player_standing (
            self, player: Player, new_score = None
            ) -> None:
        
        if new_score == None:
            new_score = player.score + 1
        
        self.standings[player.score].remove(player)
        self.standings[new_score].append(player)
        player.update_score(new_score)

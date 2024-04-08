
from tournament.swiss_tournament_simulator import SwissTournamentSimulator
from utils.player import Player

players = []
for i in range(8):
    players.append(
        Player(
            name=f"Player{i}",
            strategy=None
        )
    )

tournament = SwissTournamentSimulator(players)
tournament.run()
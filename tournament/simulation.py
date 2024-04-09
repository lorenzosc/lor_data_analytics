from time import time
from tournament.swiss_tournament_simulator import SwissTournamentSimulator
from utils.player import Player
start = time()
for _ in range(200):
    for j in [5, 7, 9, 17, 33]:
        players = []
        for i in range(j):
            players.append(
                Player(
                    name=f"Player{i}",
                    strategy=None
                )
            )

        tournament = SwissTournamentSimulator(players)
        tournament.run()
print(time()-start, " Segundos")
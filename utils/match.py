from player import Player
from matchup_table import MatchupTable
import numpy as np
import random

class Match():

    player1: Player
    player2: Player
    
    def __init__(
            self, player1: Player, player2: Player
        ):
        self.player1 = player1
        self.player2 = player2
        
    def resolve_match(
            self, matchup_table: MatchupTable
        ):
        matchup = []
        for deck1 in self.player1.decks():
            matchup.append([])
            for deck2 in self.player2.decks():
                matchup[-1].append(matchup_table[deck1][deck2])
            matchup[-1].extend(matchup[-1][:2])
        matchup.append(matchup[0])
        matchup.append(matchup[1])

        matriz_ban_1 = np.zeros((3,3))
        matriz_ban_2 = np.zeros((3,3))
        matriz_ban_media = np.zeros((3,3))

        for i in range(3):
            for j in range(3):
                matriz_ban_1[i,j] = matchup[i+1][j+1] * (1 - (1 - matchup[i+2][j+1])*(1 - matchup[i+2][j+2])) \
                                    + (1 - matchup[i+1][j+1]) * matchup[i+1][j+2] * matchup[i+2][j+2]
                matriz_ban_2[i,j] = matchup[i+1][j+2] * (1 - (1 - matchup[i+2][j+1])*(1 - matchup[i+2][j+2])) \
                                    + (1 - matchup[i+1][j+2]) * matchup[i+1][j+1] * matchup[i+2][j+1]
                matriz_ban_media[i,j] = (matriz_ban_1+matriz_ban_2)/2
        
        wr_ban_player_1 = []
        wr_ban_player_2 = []
        for i in range(3):
            av_p1 = 0
            av_p2 = 0
            for j in range(3):
                av_p1 += matriz_ban_media[j,i]
                av_p2 += matriz_ban_media[i,j]
            av_p1 /= 3
            av_p2 /= 3
            wr_ban_player_1.append(av_p1)
            wr_ban_player_2.append(av_p2)
        
        ban1 = wr_ban_player_1.index(max(wr_ban_player_1))
        ban2 = wr_ban_player_2.index(min(wr_ban_player_2))

        wr = matriz_ban_media[ban2, ban1]
        randomizer = random.random()
        
        return self.player1 if randomizer < wr else self.player2
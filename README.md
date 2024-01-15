# LEGENDS OF RUNETERRA DATA ANALYTICS

## DECK CORRELATION
Module with an implementation of pearson's correlation coefficient, but weighted with the playrates of each deck for 50 most played archetypes.

This is based on a widely used strategy in the competitive scenery, since the competitve format for the game is a best-of-three conquest using 3 different decks and 1 ban. Decks who share their strenghts are viewed as a strong pair due to the constraints of the conquest mode. As such, the idea is to identify decks who perform above their average against similar opponents in order to provide insights that should help to build a line up, while also keeping their overall winrates in mind as to not give up too much on deck quality for the synergy.

Each deck's winrates is treated as a random variable, whose value depends on which deck they're facing. Therefore, a correlation can be traced by using two decks winrate values against the same field of opponents. A limitation of this analysis is the fact that the decks can only be correlated 2 by 2, and when making a lineup with 3 decks, one would have 3 total correlations (AxB, AxC, BxC), and even when all those 3 are in a similar, relevant value, such as 0.5, while they may share strenghts when taken two by two against several decks, the 3 decks together might not share the same strenghts, as illustrated in the example below by a venn diagram of how the weakness and strenghts might be distributed.

## TOURNAMENT
A module for simulation of several tournaments by respecting the play rate and winrate of decks. The analysis aims to record how well each deck did and which decks overperformed (had a better topcut rate than their playrate) across several simulation tournaments to reduce the statistical variance inevitably allowed by the binary nature of a match. Still to be finished

## EXACT ALGORITHM
A module for the decision of the best lineup by checking their performance against every possible opponent, weighted by the likelihood of facing that opponent. The complexity of this algorithm is O(m^2), where m is the number of possible lineups, and due to the nature of the calculus of a match between two lineups, it can't be diminished. While a squared algorithm is not bad for a one time analysis, it is important to remember that the number of valid lineups is O(n^3), where n is the number of different archetypes in the analysis, resulting in a O(n^6) algorithm when taken the number of archetypes as an input. 

Luckily, the number of relevant archetypes which relevant data for an analysis will barely go above 30, and here we will keep it as the 50 decks with the higher playrates, so the algorithm is still fast enough.
class Lineup():
    
    deck1: str
    deck2: str
    deck3: str
    
    def __init__ (
            self, deck1: str, deck2: str, deck3: str
            ) -> None:
        self.deck1 = deck1
        self.deck2 = deck2
        self.deck3 = deck3

    def decks (
            self
    ):
        return [self.deck1, self.deck2, self.deck3]
    
    def verify_lineup (
            self
    ):
        pass
    


deck1 = "A"
deck2 = "b"
deck3 = "c"

meus_decks = Lineup(deck1, deck2, deck3)

print(meus_decks)
print(meus_decks.deck1)
print(meus_decks.decks())
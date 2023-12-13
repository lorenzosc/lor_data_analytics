class MatchupTable():
    
    decks: list
    table: dict

    def __init__(
            self, table: dict
    ):
        self.table = table
        self.decks = [deck for deck in table]
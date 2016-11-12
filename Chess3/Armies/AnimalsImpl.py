from Chess3 import ArmyBase, ARMY_WHITE, Coordinate
from Chess3.Pieces.KingImpl import King
from Chess3.Pieces.PawnImpl import Pawn
from Chess3.Pieces.AnimalsPieces import Tiger, WildHorse, Elephant, JungleQueen


class Animals(ArmyBase):

    promotions = {'promote to Wild Horse': WildHorse,
                  'promote to Tiger': Tiger,
                  'promote to Elephant': Elephant,
                  'promote to Jungle Queen': JungleQueen}

    def setup(self):
        if self.color == ARMY_WHITE:
            pawnrow = 1
            piecerow = 0
        else:
            pawnrow = 6
            piecerow = 7

        for x in range(8):
            self.pieces.append(Pawn(self, Coordinate(pawnrow, x)))

        self.pieces.append(Elephant(self, Coordinate(piecerow, 0)))
        self.pieces.append(WildHorse(self, Coordinate(piecerow, 1)))
        self.pieces.append(Tiger(self, Coordinate(piecerow, 2)))
        self.pieces.append(JungleQueen(self, Coordinate(piecerow, 3)))
        self.pieces.append(Tiger(self, Coordinate(piecerow, 5)))
        self.pieces.append(WildHorse(self, Coordinate(piecerow, 6)))
        self.pieces.append(Elephant(self, Coordinate(piecerow, 7)))

        king = King(self, Coordinate(piecerow, 4))
        self.pieces.append(king)
        self.kings.append(king)

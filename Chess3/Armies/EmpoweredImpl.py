from Chess3 import ArmyBase, ARMY_WHITE, Coordinate
from Chess3.Pieces.EmpoweredPieces import EmpoweredBishop, EmpoweredKnight, EmpoweredRook, EmpoweredQueen
from Chess3.Pieces.KingImpl import King
from Chess3.Pieces.PawnImpl import Pawn


class Empowered(ArmyBase):
    promotions = {'promote to Knight': EmpoweredKnight,
                  'promote to Bishop': EmpoweredBishop,
                  'promote to Rook': EmpoweredRook,
                  'promote to Queen': EmpoweredQueen}

    def setup(self):
        if self.color == ARMY_WHITE:
            pawnrow = 1
            piecerow = 0
        else:
            pawnrow = 6
            piecerow = 7

        for x in range(8):
            self.pieces.append(Pawn(self, Coordinate(pawnrow, x)))

        self.pieces.append(EmpoweredRook(self, Coordinate(piecerow, 0)))
        self.pieces.append(EmpoweredKnight(self, Coordinate(piecerow, 1)))
        self.pieces.append(EmpoweredBishop(self, Coordinate(piecerow, 2)))
        self.pieces.append(EmpoweredQueen(self, Coordinate(piecerow, 3)))
        self.pieces.append(EmpoweredBishop(self, Coordinate(piecerow, 5)))
        self.pieces.append(EmpoweredKnight(self, Coordinate(piecerow, 6)))
        self.pieces.append(EmpoweredRook(self, Coordinate(piecerow, 7)))

        king = King(self, Coordinate(piecerow, 4))
        self.pieces.append(king)
        self.kings.append(king)

from Chess3 import ArmyBase, ARMY_WHITE, Coordinate
from Chess3.Pieces.BishopImpl import Bishop
from Chess3.Pieces.KingImpl import King
from Chess3.Pieces.KnightImpl import Knight
from Chess3.Pieces.NemesisPieces import Nemesis as NemesisPiece, NemesisPawn
from Chess3.Pieces.RookImpl import Rook


class Nemesis(ArmyBase):

    promotions = {'promote to Knight': Knight,
                  'promote to Bishop': Bishop,
                  'promote to Rook': Rook,
                  'promote to Nemesis': NemesisPiece}

    def setup(self):
        if self.color == ARMY_WHITE:
            pawnrow = 1
            piecerow = 0
        else:
            pawnrow = 6
            piecerow = 7

        for x in range(8):
            self.pieces.append(NemesisPawn(self, Coordinate(pawnrow, x)))

        self.pieces.append(Rook(self, Coordinate(piecerow, 0)))
        self.pieces.append(Knight(self, Coordinate(piecerow, 1)))
        self.pieces.append(Bishop(self, Coordinate(piecerow, 2)))
        self.pieces.append(NemesisPiece(self, Coordinate(piecerow, 3)))
        self.pieces.append(Bishop(self, Coordinate(piecerow, 5)))
        self.pieces.append(Knight(self, Coordinate(piecerow, 6)))
        self.pieces.append(Rook(self, Coordinate(piecerow, 7)))

        king = King(self, Coordinate(piecerow, 4))
        self.pieces.append(king)
        self.kings.append(king)

from Chess3 import ArmyBase, ARMY_WHITE, Coordinate
from Chess3.Pieces.BishopImpl import Bishop
from Chess3.Pieces.KingImpl import ClassicKing
from Chess3.Pieces.KnightImpl import Knight
from Chess3.Pieces.PawnImpl import Pawn
from Chess3.Pieces.QueenImpl import Queen
from Chess3.Pieces.RookImpl import ClassicRook


class Classic(ArmyBase):

    promotions = {'promote to Knight': Knight,
                  'promote to Bishop': Bishop,
                  'promote to Rook': ClassicRook,
                  'promote to Queen': Queen}

    def setup(self):
        if self.color == ARMY_WHITE:
            pawnrow = 1
            piecerow = 0
        else:
            pawnrow = 6
            piecerow = 7

        for x in range(8):
            self.pieces.append(Pawn(self, Coordinate(pawnrow, x)))

        self.pieces.append(ClassicRook(self, Coordinate(piecerow, 0)))
        self.pieces.append(Knight(self, Coordinate(piecerow, 1)))
        self.pieces.append(Bishop(self, Coordinate(piecerow, 2)))
        self.pieces.append(Queen(self, Coordinate(piecerow, 3)))
        self.pieces.append(Bishop(self, Coordinate(piecerow, 5)))
        self.pieces.append(Knight(self, Coordinate(piecerow, 6)))
        self.pieces.append(ClassicRook(self, Coordinate(piecerow, 7)))

        king = ClassicKing(self, Coordinate(piecerow, 4))
        self.pieces.append(king)
        self.kings.append(king)

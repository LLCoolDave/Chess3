from Chess3 import ArmyBase, ARMY_WHITE, Coordinate
from Chess3.Pieces.BishopImpl import Bishop
from Chess3.Pieces.KingImpl import King
from Chess3.Pieces.KnightImpl import Knight
from Chess3.Pieces.PawnImpl import Pawn
from Chess3.Pieces.ReaperPieces import Ghost, Reaper as ReaperPiece


class Reaper(ArmyBase):

    promotions = {'promote to Knight': Knight,
                  'promote to Bishop': Bishop,
                  'promote to Ghost': Ghost,
                  'promote to Reaper': ReaperPiece}

    def setup(self):
        if self.color == ARMY_WHITE:
            pawnrow = 1
            piecerow = 0
        else:
            pawnrow = 6
            piecerow = 7

        for x in range(8):
            self.pieces.append(Pawn(self, Coordinate(pawnrow, x)))

        self.pieces.append(Ghost(self, Coordinate(piecerow, 0)))
        self.pieces.append(Knight(self, Coordinate(piecerow, 1)))
        self.pieces.append(Bishop(self, Coordinate(piecerow, 2)))
        self.pieces.append(ReaperPiece(self, Coordinate(piecerow, 3)))
        self.pieces.append(Bishop(self, Coordinate(piecerow, 5)))
        self.pieces.append(Knight(self, Coordinate(piecerow, 6)))
        self.pieces.append(Ghost(self, Coordinate(piecerow, 7)))

        king = King(self, Coordinate(piecerow, 4))
        self.pieces.append(king)
        self.kings.append(king)

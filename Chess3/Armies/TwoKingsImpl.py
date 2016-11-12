from Chess3 import ArmyBase, ARMY_WHITE, Coordinate
from Chess3.Pieces.TwoKingsPieces import WarriorKing, TwoKingsBishop, TwoKingsKnight, TwoKingsPawn, TwoKingsRook


class WarriorKings(ArmyBase):

    promotions = {'promote to Knight': TwoKingsKnight,
                  'promote to Bishop': TwoKingsBishop,
                  'promote to Rook': TwoKingsRook}

    def __init__(self, color, chessboard):
        super(WarriorKings, self).__init__(color, chessboard)
        self.on_king_turn = False

    def setup(self):
        if self.color == ARMY_WHITE:
            pawnrow = 1
            piecerow = 0
        else:
            pawnrow = 6
            piecerow = 7

        for x in range(8):
            self.pieces.append(TwoKingsPawn(self, Coordinate(pawnrow, x)))

        self.pieces.append(TwoKingsRook(self, Coordinate(piecerow, 0)))
        self.pieces.append(TwoKingsKnight(self, Coordinate(piecerow, 1)))
        self.pieces.append(TwoKingsBishop(self, Coordinate(piecerow, 2)))
        self.pieces.append(TwoKingsBishop(self, Coordinate(piecerow, 5)))
        self.pieces.append(TwoKingsKnight(self, Coordinate(piecerow, 6)))
        self.pieces.append(TwoKingsRook(self, Coordinate(piecerow, 7)))

        king1 = WarriorKing(self, Coordinate(piecerow, 3))
        self.pieces.append(king1)
        self.kings.append(king1)

        king2 = WarriorKing(self, Coordinate(piecerow, 4))
        self.pieces.append(king2)
        self.kings.append(king2)

    def check_special_loss(self):
        return len(self.kings) < 2

    def deep_copy(self, new_cb):
        copy = super(WarriorKings, self).deep_copy(new_cb)
        copy.on_king_turn = self.on_king_turn
        return copy

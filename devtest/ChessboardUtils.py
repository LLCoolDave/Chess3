from Chess3 import Chessboard, ArmyBase, ARMY_WHITE, ARMY_BLACK, PieceBase


class MockArmy(ArmyBase):
    pass


class MockPiece(PieceBase):
    pass


class MockBoard(Chessboard):

    def __init__(self, *args):
        super(MockBoard, self).__init__()
        self.black_army = MockArmy(ARMY_BLACK, self)
        self.white_army = MockArmy(ARMY_WHITE, self)
        for arg in args:
            self.add_piece(*arg)

    def add_piece(self, piececlass, color, coord):
        if color == ARMY_WHITE:
            army = self.white_army
        else:
            army = self.black_army
        piece = piececlass(army, coord)
        army.pieces.append(piece)
        if piece.is_king():
            army.kings.append(piece)

    def mock_piece(self, color, coord):
        self.add_piece(MockPiece, color, coord)

from Chess3 import PieceBase, MovementUtils


class Rook(PieceBase):

    picture = 'Rook'

    def get_all_possible_moves(self):
        return MovementUtils.multimove_until_obstructed(self, [(1, 0), (0, 1), (-1, 0), (0, -1)])


# required for castling
class ClassicRook(Rook):

    def __init__(self, army, coord):
        super(ClassicRook, self).__init__(army, coord)
        self.has_moved = False

    def deep_copy(self, new_army):
        new_piece = super(ClassicRook, self).deep_copy(new_army)
        new_piece.has_moved = self.has_moved
        return new_piece

    def movement_callback(self, move):
        self.has_moved = True
        return super(ClassicRook, self).movement_callback(move)

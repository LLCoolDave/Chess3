from Chess3 import PieceBase, MovementUtils


class Queen(PieceBase):

    picture = 'Queen'

    def get_all_possible_moves(self):
        return MovementUtils.multimove_until_obstructed(self, [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)])

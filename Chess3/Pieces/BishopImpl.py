from Chess3 import PieceBase, MovementUtils


class Bishop(PieceBase):

    picture = 'Bishop'

    def get_all_possible_moves(self):
        return MovementUtils.multimove_until_obstructed(self, [(1, 1), (-1, 1), (1, -1), (-1, -1)])

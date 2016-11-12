from Chess3 import PieceBase, MovementUtils


class Knight(PieceBase):

    picture = 'Knight'

    def get_all_possible_moves(self):
        ret = []
        for possible_target in MovementUtils.possible_knight_moves(self.coord):
            if self.chessboard.get_field(possible_target).is_empty():
                ret.append(MovementUtils.move_from_to(self.coord, possible_target))
            elif self.chessboard.get_field(possible_target).has_enemy(self):
                ret.append(MovementUtils.move_and_capture(self.coord, possible_target))

        return ret

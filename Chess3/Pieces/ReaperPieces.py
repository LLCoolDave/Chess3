from Chess3 import Coordinate, PieceBase, MovementUtils


class Reaper(PieceBase):

    # ToDo update
    picture = 'Queen'

    def get_all_possible_moves(self):
        ret = []
        for i in range(8):
            for j in range(8):
                possible_target = Coordinate(i, j)
                if self.chessboard.get_field(possible_target).is_empty():
                    ret.append(MovementUtils.move_from_to(self.coord, possible_target))
                elif 0 < i < 7 and self.chessboard.get_field(possible_target).has_enemy(self):
                    if not self.chessboard.get_piece(possible_target).is_king():
                        ret.append(MovementUtils.move_and_capture(self.coord, possible_target))
        return ret

    def get_threatened_fields(self):
        return []


class Ghost(PieceBase):

    # ToDo update
    picture = 'Rook'

    def is_capturable(self, attacker):
        return False

    def get_all_possible_moves(self):
        ret = []
        for i in range(8):
            for j in range(8):
                possible_target = Coordinate(i, j)
                if self.chessboard.get_field(possible_target).is_empty():
                    ret.append(MovementUtils.move_from_to(self.coord, possible_target))
        return ret

    def get_threatened_fields(self):
        return []

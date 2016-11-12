from Chess3 import PieceBase, MovementUtils


def _get_all_rook_moves(piece):
    return MovementUtils.multimove_until_obstructed(piece, [(1, 0), (0, 1), (-1, 0), (0, -1)])


def _get_all_bishop_moves(piece):
    return MovementUtils.multimove_until_obstructed(piece, [(1, 1), (-1, 1), (-1, -1), (1, -1)])


def _get_all_knight_moves(piece):
    ret = []
    for possible_target in MovementUtils.possible_knight_moves(piece.coord):
        if piece.chessboard.get_field(possible_target).is_empty():
            ret.append(MovementUtils.move_from_to(piece.coord, possible_target))
        elif piece.chessboard.get_field(possible_target).has_enemy(piece):
            ret.append(MovementUtils.move_and_capture(piece.coord, possible_target))
    return ret


class EmpoweredPiece(PieceBase):

    def get_all_possible_moves(self):
        moves = set()
        ret = []
        for field_to_check in [MovementUtils.get_relative_coord(self.coord, x, y) for x, y in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]]:
            if field_to_check is not None:
                piece = self.chessboard.get_piece(field_to_check)
                if piece is not None:
                    if piece.color == self.color:
                        if isinstance(piece, EmpoweredBishop):
                            moves.add(_get_all_bishop_moves)
                        elif isinstance(piece, EmpoweredKnight):
                            moves.add(_get_all_knight_moves)
                        elif isinstance(piece, EmpoweredRook):
                            moves.add(_get_all_rook_moves)

        for move in moves:
            ret.extend(move(self))
        return ret


class EmpoweredBishop(EmpoweredPiece):

    # ToDo
    picture = 'Bishop'


class EmpoweredKnight(EmpoweredPiece):

    # ToDo
    picture = 'Knight'


class EmpoweredRook(EmpoweredPiece):

    # ToDo
    picture = 'Rook'


class EmpoweredQueen(PieceBase):

    # ToDo
    picture = 'Queen'

    def get_all_possible_moves(self):
        ret = []
        for possible_target in MovementUtils.possible_king_moves(self.coord):
            if self.chessboard.get_field(possible_target).is_empty():
                ret.append(MovementUtils.move_from_to(self.coord, possible_target))
            elif self.chessboard.get_field(possible_target).has_enemy(self):
                ret.append(MovementUtils.move_and_capture(self.coord, possible_target))
        return ret

from Chess3 import PieceBase, MovementUtils, Move, MoveAction


class WildHorse(PieceBase):

    # ToDo
    picture = 'Knight'

    def get_all_possible_moves(self):
        ret = []
        for possible_target in MovementUtils.possible_knight_moves(self.coord):
            if self.chessboard.get_field(possible_target).is_empty():
                ret.append(MovementUtils.move_from_to(self.coord, possible_target))
            elif self.chessboard.get_piece(possible_target).is_capturable(self):
                ret.append(MovementUtils.move_and_capture(self.coord, possible_target))

        return ret


class JungleQueen(PieceBase):

    # ToDo
    picture = 'Queen'

    def get_all_possible_moves(self):
        ret = MovementUtils.multimove_until_obstructed(self, [(1, 0), (0, 1), (-1, 0), (0, -1)])
        for possible_target in MovementUtils.possible_knight_moves(self.coord):
            if self.chessboard.get_field(possible_target).is_empty():
                ret.append(MovementUtils.move_from_to(self.coord, possible_target))
            elif self.chessboard.get_field(possible_target).has_enemy(self):
                ret.append(MovementUtils.move_and_capture(self.coord, possible_target))

        return ret


class Tiger(PieceBase):

    # ToDo
    picture = 'Bishop'

    def get_all_possible_moves(self):
        ret = []

        for row_delta, column_delta in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            target = MovementUtils.get_relative_coord(self.coord, row_delta, column_delta)
            if target is not None:
                if self.chessboard.get_field(target).is_empty():
                    ret.append(MovementUtils.move_from_to(self.coord, target))
                    target = MovementUtils.get_relative_coord(self.coord, 2 * row_delta, 2 * column_delta)
                    if target is not None:
                        if self.chessboard.get_field(target).is_empty():
                            ret.append(MovementUtils.move_from_to(self.coord, target))
                        elif self.chessboard.get_field(target).has_enemy(self) and \
                                self.chessboard.get_piece(target).is_capturable(self):
                            ret.append(Move('pounce', self.coord, target, [], [target], True))
                elif self.chessboard.get_field(target).has_enemy(self) and \
                        self.chessboard.get_piece(target).is_capturable(self):
                    ret.append(Move('pounce', self.coord, target, [], [target], True))

        return ret


class Elephant(PieceBase):

    # ToDo
    picture = 'Rook'

    def is_capturable(self, attacker):
        delta_row, delta_colum = MovementUtils.get_deltas(self.coord, attacker.coord)
        return abs(delta_row) <= 2 and abs(delta_colum) <= 2

    def _get_rampage(self, rowdelta, columndelta):
        endpoint = self.coord
        captures = []
        for i in range(1, 4):
            target = MovementUtils.get_relative_coord(self.coord, i * rowdelta, i * columndelta)
            if target is not None:
                if self.chessboard.get_piece(target) is not None:
                    if not self.chessboard.get_piece(target).is_capturable(self):
                        break
                    else:
                        captures.append(target)
                endpoint = target
        return endpoint, captures

    def get_all_possible_moves(self):
        ret = []

        for row_delta, column_delta in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 4):
                target = MovementUtils.get_relative_coord(self.coord, i * row_delta, i * column_delta)
                if target is not None:
                    if self.chessboard.get_field(target).is_empty():
                        ret.append(MovementUtils.move_from_to(self.coord, target))
                    else:
                        # there is a piece, we rampage
                        endpoint, captures = self._get_rampage(row_delta, column_delta)
                        # if we can actually capture the piece in question we offer the move
                        if target in captures:
                            ret.append(Move('rampage', self.coord, target, [MoveAction(self.coord, endpoint)], captures, True))
                        break

        return ret
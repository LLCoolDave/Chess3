from Chess3 import ARMY_BLACK, ARMY_WHITE
from Chess3 import PieceBase, MovementUtils, Coordinate, Move, MoveAction
from .RookImpl import ClassicRook


class King(PieceBase):

    picture = 'King'

    def __init__(self, army, coord):
        super(King, self).__init__(army, coord)
        self.king = True

    def get_all_possible_moves(self):
        ret = []
        for possible_target in MovementUtils.possible_king_moves(self.coord):
            if self.chessboard.get_field(possible_target).is_empty():
                ret.append(MovementUtils.move_from_to(self.coord, possible_target))
            elif self.chessboard.get_field(possible_target).has_enemy(self):
                ret.append(MovementUtils.move_and_capture(self.coord, possible_target))
        return ret

    def get_threatened_fields(self):
        # Kings threaten all squares around them, even if they are not technically allowed to legally move into them (!)
        return set(MovementUtils.possible_king_moves(self.coord))


# required for castling
class ClassicKing(King):

    def __init__(self, army, coord):
        super(ClassicKing, self).__init__(army, coord)
        self.has_moved = False

    def deep_copy(self, new_army):
        new_piece = super(ClassicKing, self).deep_copy(new_army)
        new_piece.has_moved = self.has_moved
        return new_piece

    def movement_callback(self, move):
        self.has_moved = True
        return super(ClassicKing, self).movement_callback(move)

    def get_all_possible_moves(self):
        ret = super(ClassicKing, self).get_all_possible_moves()

        # check for castling, this can probably be significantly improved
        if not self.has_moved and not self.army.is_in_check():
            kingrow = self.coord.row
            # we're on initial square, so check our rooks

            qs_rook = self.chessboard.get_piece(Coordinate(kingrow, 0))
            if qs_rook is not None and qs_rook.color == self.color and\
                    isinstance(qs_rook, ClassicRook) and not qs_rook.has_moved:
                # castling might be possible, check intermediate fields
                qs_castle_possible = True
                for clmn in (1, 2, 3):
                    qs_castle_possible &= self.chessboard.get_field(Coordinate(kingrow, clmn)).is_empty()
                if qs_castle_possible:
                    # space is empty, check if neighbouring field is threatened
                    new_cb = self.chessboard.deep_copy()
                    # put king on empty space and see if we would be in check there
                    new_cb.execute_move(MovementUtils.move_from_to(self.coord, Coordinate(kingrow, 3)))
                    if not new_cb.get_army(self.color).is_in_check():
                        ret.append(Move('O-O-O', self.coord, Coordinate(kingrow, 2),
                                        [MoveAction(self.coord, Coordinate(kingrow, 2)), MoveAction(qs_rook.coord, Coordinate(kingrow, 3))],
                                        [], True))

            ks_rook = self.chessboard.get_piece(Coordinate(kingrow, 7))
            if ks_rook is not None and ks_rook.color == self.color and\
                    isinstance(ks_rook, ClassicRook) and not ks_rook.has_moved:
                # castling might be possible, check intermediate fields
                ks_castle_possible = True
                for clmn in (5, 6):
                    ks_castle_possible &= self.chessboard.get_field(Coordinate(kingrow, clmn)).is_empty()
                if ks_castle_possible:
                    # space is empty, check if neighbouring field is threatened
                    new_cb = self.chessboard.deep_copy()
                    # put king on empty space and see if we would be in check there
                    new_cb.execute_move(MovementUtils.move_from_to(self.coord, Coordinate(kingrow, 5)))
                    if not new_cb.get_army(self.color).is_in_check():
                        ret.append(Move('O-O', self.coord, Coordinate(kingrow, 6),
                                        [MoveAction(self.coord, Coordinate(kingrow, 6)), MoveAction(ks_rook.coord, Coordinate(kingrow, 5))],
                                        [], True))
        return ret

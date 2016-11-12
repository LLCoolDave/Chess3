from Chess3 import PieceBase, ARMY_WHITE, Move, MoveAction
from Chess3.MovementUtils import move_and_capture, move_from_to, get_relative_coord, get_deltas


class Pawn(PieceBase):

    picture = 'Pawn'

    def __init__(self, army, coord):
        super(Pawn, self).__init__(army, coord)
        self.unmoved = True
        self.en_passant = False

    def deep_copy(self, new_army):
        new_piece = super(Pawn, self).deep_copy(new_army)
        new_piece.unmoved = self.unmoved
        new_piece.en_passant = self.en_passant
        return new_piece

    def advance_tick(self):
        super(Pawn, self).advance_tick()
        self.en_passant = False

    def get_all_possible_moves(self):
        ret = []

        if self.color == ARMY_WHITE:
            row_delta = 1
            promotionrow = 7
        else:
            row_delta = -1
            promotionrow = 0

        # single move
        target = get_relative_coord(self.coord, row_delta, 0)
        if target is not None:
            if self.chessboard.get_field(target).is_empty():
                ret.append(move_from_to(self.coord, target))

                # double move
                if self.unmoved:
                    target = get_relative_coord(self.coord, 2*row_delta, 0)
                    if target is not None:
                        if self.chessboard.get_field(target).is_empty():
                            ret.append(move_from_to(self.coord, target, 'double move'))

        # diagonal capture
        for column_delta in [-1, 1]:
            target = get_relative_coord(self.coord, row_delta, column_delta)
            if target is not None:
                if self.chessboard.get_field(target).has_enemy(self):
                    ret.append(move_and_capture(self.coord, target))

        # check for en passant
        for column_delta in [-1, 1]:
            target = get_relative_coord(self.coord, 0, column_delta)
            movement_target = get_relative_coord(self.coord, row_delta, column_delta)
            if target is not None and movement_target is not None and self.chessboard.get_field(movement_target).is_empty():
                if self.chessboard.get_field(target).has_enemy(self):
                    if isinstance(self.chessboard.get_piece(target), Pawn) and self.chessboard.get_piece(target).en_passant:
                        ret.append(Move('en passant', self.coord, movement_target, [MoveAction(self.coord, movement_target)], [target]))

        # check if promotions are to be offered
        promotions = []
        for move in ret:
            if move.target.row == promotionrow:
                # add new option that includes promotion
                for promotionstr in self.army.promotions.keys():
                    promotions.append(Move(promotionstr, move.origin, move.target, move.movements, move.captures, move.end_turn))

        ret.extend(promotions)

        return ret

    def move_executed(self, move):
        self.unmoved = False
        # check for en passant
        if move.name == 'double move':
            # we were moved two spaces, en passant is enabled for a tick
            self.en_passant = True
        # check for promotion
        if move.name.startswith('promote to'):
            self.army.promote_piece(self, move.name)
        super(Pawn, self).move_executed(move)

from Chess3 import ARMY_WHITE, ARMY_BLACK
from Chess3 import PieceBase, MovementUtils
from .PawnImpl import Pawn


class Nemesis(PieceBase):

    # ToDo update
    picture = 'Queen'

    def get_all_possible_moves(self):
        ret = []
        for row_delta, column_delta in [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]:
            origin = self.coord
            cb = self.chessboard
            target = MovementUtils.get_relative_coord(origin, row_delta, column_delta)
            while target is not None:
                if cb.get_field(target).is_empty():
                    ret.append(MovementUtils.move_from_to(origin, target))
                    target = MovementUtils.get_relative_coord(target, row_delta, column_delta)
                elif cb.get_field(target).has_enemy(self) and cb.get_piece(target).is_king():
                    ret.append(MovementUtils.move_and_capture(origin, target))
                    target = None
                else:
                    target = None

        return ret

    def is_capturable(self, attacker):
        return attacker.is_king()


class NemesisPawn(PieceBase):

    picture = 'Pawn'

    def get_all_possible_moves(self):
        ret = []

        if self.color == ARMY_WHITE:
            direction = 1
            promotionrow = 7
        else:
            direction = -1
            promotionrow = 0

        # always allowed to move forward
        allowed_directions = {(direction, 0)}

        opposite_color = ARMY_BLACK if self.color == ARMY_WHITE else ARMY_WHITE
        for king in self.chessboard.get_army(opposite_color).kings:
            # check all opposing kings to get allowed directions
            row_delta, column_delta = MovementUtils.get_deltas(self.coord, king.coord)
            sign_row = (row_delta > 0) - (row_delta < 0)
            sign_column = (column_delta > 0) - (column_delta < 0)

            allowed_directions.add((sign_row, sign_column))
            if sign_row != 0:
                allowed_directions.add((0, sign_column))
            if sign_column != 0:
                allowed_directions.add((sign_row, 0))

        # get valid moves
        for row_delta, column_delta in allowed_directions:
            target = MovementUtils.get_relative_coord(self.coord, row_delta, column_delta)
            if target is not None:
                if self.chessboard.get_field(target).is_empty():
                    ret.append(MovementUtils.move_from_to(self.coord, target))

        # diagonal capture
        for column_delta in [-1, 1]:
            target = MovementUtils.get_relative_coord(self.coord, direction, column_delta)
            if target is not None:
                if self.chessboard.get_field(target).has_enemy(self):
                    ret.append(MovementUtils.move_and_capture(self.coord, target))

        # check for en passant
        for column_delta in [-1, 1]:
            target = MovementUtils.get_relative_coord(self.coord, 0, column_delta)
            movement_target = MovementUtils.get_relative_coord(self.coord, direction, column_delta)
            if target is not None and movement_target is not None and self.chessboard.get_field(movement_target).is_empty():
                if self.chessboard.get_field(target).has_enemy(self):
                    if isinstance(self.chessboard.get_piece(target), Pawn) and self.chessboard.get_piece(target).en_passant:
                        ret.append(MovementUtils.Move('en passant', self.coord, movement_target, [MovementUtils.MoveAction(self.coord, movement_target)], [target]))

        # check if promotions are to be offered
        promotions = []
        for move in ret:
            if move.target.row == promotionrow:
                # add new option that includes promotion
                for promotionstr in self.army.promotions.keys():
                    promotions.append(MovementUtils.Move(promotionstr, move.origin, move.target, move.movements, move.captures, move.end_turn))

        ret.extend(promotions)

        return ret

    def move_executed(self, move):
        # check for promotion
        if move.name.startswith('promote to'):
            self.army.promote_piece(self, move.name)
        super(NemesisPawn, self).move_executed(move)

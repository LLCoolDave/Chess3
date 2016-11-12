from .MoveImpl import Coordinate
from .FieldImpl import Field
from .ArmyBaseImpl import ARMY_BLACK, ARMY_WHITE


class Chessboard(object):

    def __init__(self):
        self.fields = [[Field(Coordinate(row, column), self) for column in range(8)] for row in range(8)]
        self.white_army = None
        self.black_army = None

    def get_field(self, coord):
        return self.fields[coord.row][coord.column]

    def get_piece(self, coord):
        return self.fields[coord.row][coord.column].piece

    def get_army(self, color):
        if color == ARMY_WHITE:
            return self.white_army
        elif color == ARMY_BLACK:
            return self.black_army
        else:
            return None

    def deep_copy(self):
        new_cb = Chessboard()
        if self.white_army:
            new_cb.white_army = self.white_army.deep_copy(new_cb)
        if self.black_army:
            new_cb.black_army = self.black_army.deep_copy(new_cb)
        return new_cb

    def execute_move(self, move):
        end_turn = move.end_turn

        # get originator of move
        originator = self.get_piece(move.origin)

        # first all capture actions are taken
        for capture in move.captures:
            target_piece = self.get_field(capture).piece
            if target_piece is not None:
                capture_actions = target_piece.capture_callback(move)
                # recursively take care of actions caused by capturing this piece
                for capture_action in capture_actions:
                    end_turn |= self.execute_move(capture_action)

                target_piece.army.capture_piece(target_piece, originator)

        # next, do a safe execution of movements. As this may involve swapping of pieces, we have to grab all pieces before we can move them
        movements = []
        for movement in move.movements:
            piece_to_move = self.get_field(movement.origin).piece
            piece_to_move.field.set_piece(None)
            movements.append((piece_to_move, movement.target))
        for piece_to_move, target in movements:
            # the piece could have been invalidated by all kinds of reasons
            if piece_to_move is not None:
                movement_actions = piece_to_move.movement_callback(move)
                # recursively take care of actions caused by moving this piece
                for movement_action in movement_actions:
                    end_turn |= self.execute_move(movement_action)

                piece_to_move.field = piece_to_move.chessboard.get_field(target)
                piece_to_move.field.set_piece(piece_to_move)

        # callback to originator that the move has been executed
        if originator is not None:
            originator.move_executed(move)

        # finally, return if this is a turn ending move
        return move.end_turn

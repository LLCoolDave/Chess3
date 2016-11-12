from .BishopImpl import Bishop
from .RookImpl import Rook
from .KingImpl import King
from .KnightImpl import Knight
from .PawnImpl import Pawn

from Chess3 import Move, MovementUtils


class TwoKingsPawn(Pawn):
    
    def get_all_possible_moves(self):
        if self.army.on_king_turn:
            return []
        else:
            return [Move(move.name, move.origin, move.target, move.movements, move.captures, False) for move in super(TwoKingsPawn, self).get_all_possible_moves()]

    def move_executed(self, move):
        # we did the first move, now we are on the king turn
        self.army.on_king_turn = True
        super(TwoKingsPawn, self).move_executed(move)


class TwoKingsKnight(Knight):
    def get_all_possible_moves(self):
        if self.army.on_king_turn:
            return []
        else:
            return [Move(move.name, move.origin, move.target, move.movements, move.captures, False) for move in super(TwoKingsKnight, self).get_all_possible_moves()]

    def move_executed(self, move):
        # we did the first move, now we are on the king turn
        self.army.on_king_turn = True
        super(TwoKingsKnight, self).move_executed(move)


class TwoKingsBishop(Bishop):

    def get_all_possible_moves(self):
        if self.army.on_king_turn:
            return []
        else:
            return [Move(move.name, move.origin, move.target, move.movements, move.captures, False) for move in super(TwoKingsBishop, self).get_all_possible_moves()]

    def move_executed(self, move):
        # we did the first move, now we are on the king turn
        self.army.on_king_turn = True
        super(TwoKingsBishop, self).move_executed(move)


class TwoKingsRook(Rook):

    def get_all_possible_moves(self):
        if self.army.on_king_turn:
            return []
        else:
            return [Move(move.name, move.origin, move.target, move.movements, move.captures, False) for move in super(TwoKingsRook, self).get_all_possible_moves()]

    def move_executed(self, move):
        # we did the first move, now we are on the king turn
        self.army.on_king_turn = True
        super(TwoKingsRook, self).move_executed(move)


class WarriorKing(King):

    # ToDo update
    picture = 'King'

    def get_all_possible_moves(self):
        kingmoves = super(WarriorKing, self).get_all_possible_moves()
        kingmoves.extend(self._get_whirlwind())
        if self.army.on_king_turn:
            kingmoves.append(Move('pass', self.coord, self.coord, [], [], True))
            return kingmoves
        else:
            return [Move('first move', move.origin, move.target, move.movements, move.captures, False) for move in kingmoves]

    def move_executed(self, move):
        self.army.on_king_turn = not self.army.on_king_turn
        super(WarriorKing, self).move_executed(move)

    def _get_whirlwind(self):
        # check for captures to do
        fields_to_check = MovementUtils.possible_king_moves(self.coord)
        captures = []
        for field in fields_to_check:
            pc = self.chessboard.get_piece(field)
            if pc is not None:
                if pc.color == self.color and pc.is_king():
                    # cannot whirlwind own kings!
                    return []
                elif pc.is_capturable(self):
                    captures.append(field)
        return [Move('whirlwind', self.coord, self.coord, [], captures, True)]

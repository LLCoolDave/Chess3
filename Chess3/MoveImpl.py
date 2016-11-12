class Coordinate(object):

    def __init__(self, row, column):
        if 0 <= row < 8 and 0 <= column < 8:
            self.row = row
            self.column = column
        else:
            raise ArithmeticError('Coordinate invalid')

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __hash__(self):
        return hash((self.row, self.column))

    def __repr__(self):
        return '%s%s' % (chr(ord('A') + self.column), self.row + 1)

    @classmethod
    def from_string(cls, repr):
        column = ord(repr[0]) - ord('A')
        row = int(repr[1]) - 1
        return cls(row, column)


class MoveAction(object):

    def __init__(self, origin, target):
        self.origin = origin
        self.target = target

    def __eq__(self, other):
        return self.origin == other.origin and self.target == other.target

    def __hash__(self):
        return hash((self.origin, self.target))

    def __repr__(self):
        return '%s -> %s' % (self.origin, self.target)


class Move(object):

    def __init__(self, name, origin, target, movements, captures, end_turn=True):
        self.name = name
        self.origin = origin
        self.target = target
        self.movements = movements
        self.captures = captures
        self.end_turn = end_turn

    def __eq__(self, other):
        # for Moves, the order of movements and captures actually matters, as they may have sideeffects, as does the name
        return self.name == other.name and self.origin == other.origin and self.movements == other.movements \
               and self.captures == other.captures and self.end_turn == other.end_turn

    def __hash__(self):
        return hash((self.name, self.origin, tuple(self.movements), tuple(self.captures), self.end_turn))

    def __repr__(self):
        return 'Move "%s" of %s: Movements %s capturing %s. Ends turn: %s' % (self.name, self.origin, self.movements, self.captures, self.end_turn)

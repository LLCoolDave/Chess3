class PieceBase(object):

    picture = 'Unknown'

    def __init__(self, army, coord):
        self.army = army
        self.color = army.color
        self.king = False
        self.frozen = 0
        self.chessboard = army.chessboard
        self.field = self.chessboard.get_field(coord)
        self.field.set_piece(self)

    @property
    def coord(self):
        return self.field.get_coordinate()

    def get_all_possible_moves(self):
        """
        abstract

        This lists all moves this piece could currently do. The filtering out of illegal moves due to check is done during aggregation.

        :return list of Chess3.Move:
        """
        return []

    def get_threatened_fields(self):
        """
        abstract

        by default, a piece threatens all fields it can currently capture

        :return set of Chess3.Coordinate:
        """
        ret = set()
        for possible_moves in self.get_all_possible_moves():
            ret.update(possible_moves.captures)
        return ret

    def is_king(self):
        return self.king

    def is_friendly(self, piece):
        return self.color == piece.color

    def is_enemy(self, piece):
        return self.color != piece.color

    def is_frozen(self):
        return self.frozen > 0

    def is_capturable(self, attacker):
        return True

    def advance_tick(self):
        if self.frozen > 0:
            self.frozen -= 1

    def deep_copy(self, new_army):
        clazz = self.__class__
        new_piece = clazz(new_army, self.coord)
        if self.is_king():
            new_piece.king = True
        new_piece.frozen = self.frozen
        return new_piece

    def capture_callback(self, move):
        """
        abstract

        :return list of Chess3.Move: List of moves that happen as a result of this piece being captured
        """
        return []

    def movement_callback(self, move):
        """
        abstract

        :return list of Chess3.Move: List of moves that happen as a result of this piece being moved
        """
        return []

    def move_executed(self, move):
        """
        abstract
        """

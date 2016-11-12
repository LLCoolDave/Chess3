from .MoveImpl import Coordinate


class Field(object):

    def __init__(self, coord, chessboard):
        self.row = coord.row
        self.column = coord.column
        self.chessboard = chessboard
        self.piece = None

    def get_coordinate(self):
        return Coordinate(self.row, self.column)

    def set_piece(self, piece):
        self.piece = piece

    def is_empty(self):
        return self.piece is None

    def has_enemy(self, piece):
        """
        :return: True if field contains a piece of opposing color
        """
        if self.piece is None:
            return False
        else:
            return self.piece.is_enemy(piece)

    def __repr__(self):
        if self.piece is None:
            return 'Empty'
        else:
            return self.piece.__class__.__name__

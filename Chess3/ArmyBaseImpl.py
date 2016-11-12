from .MovementUtils import Move


ARMY_WHITE = 'White'
ARMY_BLACK = 'Black'


class ArmyBase(object):

    promotions = {}

    def __init__(self, color, chessboard):
        self.color = color
        self.chessboard = chessboard
        self.kings = []
        self.pieces = []

    def setup(self):
        """
        abstract

        position initial pieces on the board
        :return:
        """

    def check_special_loss(self):
        """
        by default, checks if there are no kings left (this can happen
        if captured by an army with non threatening pieces)

        :return bool: True if army is in losing position
        """
        return not self.kings

    def check_special_win(self):
        """
        by default, checks for midline invasion

        :return bool: True if army is in winning position
        """
        ret = True

        for king in self.kings:
            if self.color == ARMY_WHITE:
                if king.coord.row < 4:
                    ret = False
                    break
            else:
                if king.coord.row >= 4:
                    ret = False
                    break

        return ret

    def is_in_check(self):
        ret = False
        opposite_color = ARMY_BLACK if self.color == ARMY_WHITE else ARMY_WHITE
        threatened_fields = self.chessboard.get_army(opposite_color).get_threatened_fields()
        for king in self.kings:
            if king.coord in threatened_fields:
                ret = True
        return ret

    def is_in_checkmate(self):
        return not self.get_all_legal_moves()

    def is_legal_move(self, move):
        # first check if all pieces that are to be captured may be captured
        for capture in move.captures:
            if self.chessboard.get_piece(capture) is not None:
                if not self.chessboard.get_piece(capture).is_capturable(self.chessboard.get_piece(move.origin)):
                    # this piece cannot be captured
                    # if something were to also move onto its currently occupied square in this move
                    # it is not possible to execute it
                    for movement in move.movements:
                        if capture == movement.target:
                            return False
                    # otherwise, we build a new move without the capture and check if it is still legal
                    newcaptures = list(move.captures)
                    newcaptures.remove(capture)
                    newmove = Move(move.name, move.origin, move.target, move.movements, newcaptures, move.end_turn)
                    # we check if there is some action left, passing moves as a result of removing illegal captures are illegal
                    if not newmove.movements and not newmove.captures:
                        return False
                    else:
                        return self.is_legal_move(newmove)
        # create copy of gamestate
        new_cb = self.chessboard.deep_copy()
        # execute move
        color = new_cb.get_piece(move.origin).color
        new_cb.execute_move(move)
        # if we are not in check afterwards, things are fine
        return not new_cb.get_army(color).is_in_check()

    def get_all_legal_moves(self):
        ret = []
        for piece in self.pieces:
            if not piece.is_frozen():
                ret.extend(piece.get_all_possible_moves())

        # filter out illegal moves
        ret = [move for move in ret if self.is_legal_move(move)]
        return ret

    def advance_tick(self):
        for piece in self.pieces:
            piece.advance_tick()

    def capture_piece(self, piece, attacker):
        if piece.is_capturable(attacker):
            piece.field.set_piece(None)
            piece.field = None
            try:
                self.pieces.remove(piece)
            except ValueError:
                pass
            try:
                self.kings.remove(piece)
            except ValueError:
                pass

    def deep_copy(self, new_cb):
        clazz = self.__class__
        new_army = clazz(self.color, new_cb)
        for piece in self.pieces:
            new_piece = piece.deep_copy(new_army)
            new_army.pieces.append(new_piece)
            if new_piece.is_king():
                new_army.kings.append(new_piece)
        return new_army

    def get_threatened_fields(self):
        ret = set()
        for piece in self.pieces:
            # pieces threaten squares they can attack after being unfrozen next move
            if piece.frozen <= 1:
                ret.update(piece.get_threatened_fields())
        return ret

    def promote_piece(self, piece, promotionstr):
        try:
            promotionpiece = self.promotions[promotionstr]
        except IndexError:
            return

        if piece is not None and piece.color == self.color:
            coord = piece.coord
            piece.field.set_piece(None)
            piece.field = None
            try:
                self.pieces.remove(piece)
            except ValueError:
                pass
            try:
                self.kings.remove(piece)
            except ValueError:
                pass

            newpiece = promotionpiece(self, coord)
            self.pieces.append(newpiece)
            if newpiece.is_king():
                self.kings.append(newpiece)

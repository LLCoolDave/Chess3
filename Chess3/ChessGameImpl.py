from .ChessboardImpl import Coordinate, Chessboard
from .ArmyBaseImpl import ARMY_BLACK, ARMY_WHITE


def opposite_color(color):
    return ARMY_BLACK if color == ARMY_WHITE else ARMY_WHITE


class ChessGame(object):

    def __init__(self):
        self.activeboard = Chessboard()
        self.activeplayer = ARMY_WHITE
        self.legal_moves = []
        self.selected = None
        self.targets = {}

    @property
    def inactiveplayer(self):
        return opposite_color(self.activeplayer)

    @property
    def activearmy(self):
        return self.activeboard.get_army(self.activeplayer)

    @property
    def inactivearmy(self):
        return self.activeboard.get_army(self.inactiveplayer)

    def swap_active_player(self):
        self.activeplayer = opposite_color(self.activeplayer)

    def start_turn(self):
        self.selected = None
        # grab all legal moves for current boardstate
        self.legal_moves = self.activearmy.get_all_legal_moves()
        self._update_targets()

    def end_turn(self):
        self.swap_active_player()
        self.activearmy.advance_tick()
        self.start_turn()

    def handle_field_click(self, coordinate):
        if coordinate in self.targets:
            if len(self.targets[coordinate]) == 1:
                self.execute_move(self.targets[coordinate][0])
            else:
                self.select_multiple_moves(self.targets[coordinate])
        else:
            piece = self.get_piece(coordinate)
            if piece is not None and piece.color == self.activeplayer:
                self.selected = coordinate
                self._update_targets()

    def execute_move(self, move):
        end_turn = self.activeboard.execute_move(move)
        # check for winconditions:
        if self.inactivearmy.is_in_check():
            # ToDo
            print('CHECK')
        if self.inactivearmy.is_in_checkmate():
            # ToDo
            print('CHECKMATE  -  %s wins' % self.activeplayer)
        if self.activearmy.check_special_win() or self.inactivearmy.check_special_loss():
            # ToDo
            print('SPECIALWIN - %s wins' % self.activeplayer)
        if self.inactivearmy.check_special_win() or self.activearmy.check_special_loss():
            # ToDo
            print('SPECIALWIN - %s wins' % self.inactiveplayer)

        if end_turn:
            self.end_turn()
        else:
            self.start_turn()

    def _update_targets(self):
        self.targets = {}
        for move in self.legal_moves:
            if self.selected is not None and move.origin == self.selected:
                if move.target not in self.targets:
                    self.targets[move.target] = [move]
                else:
                    self.targets[move.target].append(move)

    def get_field_attribs(self, coord):
        ret = {}
        if self.selected is not None and self.selected == coord:
            ret['selected'] = True

        if coord in self.targets:
            for targetmove in self.targets[coord]:
                ret['action'] = True
                if coord in targetmove.captures:
                    ret['capture'] = True
                for moveaction in targetmove.movements:
                    if moveaction.target == coord:
                        ret['move'] = True

        return ret

    def get_field(self, coord):
        return self.activeboard.get_field(coord)

    def get_piece(self, coord):
        return self.activeboard.get_field(coord).piece

    def select_multiple_moves(self, movelist):
        # ToDo find responsible place to do this
        from PyQt5.QtWidgets import QMenu
        from PyQt5.QtGui import QCursor
        menu = QMenu()
        actionlist = []
        for move in movelist:
            actionlist.append(menu.addAction(move.name))
        action = menu.exec_(QCursor.pos())
        try:
            chosenmoveindex = actionlist.index(action)
            self.execute_move(movelist[chosenmoveindex])
        except ValueError:
            pass

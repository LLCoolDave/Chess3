from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QFrame, QSizePolicy

from Chess3 import ChessGame, Coordinate, ARMY_BLACK, ARMY_WHITE
from .Constants import *
from . import PictureCache


class BoardFrame(QFrame):

    def __init__(self, *args, **kwargs):
        super(BoardFrame, self).__init__(*args, **kwargs)
        self.activegame = ChessGame()
        self.setObjectName("BoardFrame")
        self.setGeometry(QRect(10, 10, BOARDWIDTH, BOARDHEIGHT))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(BOARDWIDTH, BOARDHEIGHT))
        self.setMaximumSize(QSize(BOARDWIDTH, BOARDHEIGHT))
        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)

    def paintEvent(self, event):
        super(BoardFrame, self).paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(2, 2, BOARDWIDTH - 4, BOARDHEIGHT - 4, QColor(0x000000))
        for row in range(8):
            for column in range(8):
                _draw_field(self.get_field(Coordinate(row, column)),
                            painter,
                            column * (FIELDWIDTH + BOARDINNERFRAME) + BOARDOUTERFRAME,
                            BOARDHEIGHT - (row + 1) * (FIELDHEIGHT + BOARDINNERFRAME) - BOARDOUTERFRAME + BOARDINNERFRAME,
                            FIELDWIDTH,
                            FIELDHEIGHT,
                            **self.activegame.get_field_attribs(Coordinate(row, column)))
        painter.end()

    def mousePressEvent(self, event):
        coord = self._get_coord_from_event(event.x(), event.y())
        if coord is not None:
            try:
                self.activegame.handle_field_click(coord)
            except Exception:
                import traceback
                traceback.print_exc()
        self.update()

    def _get_coord_from_event(self, x, y):
        y = BOARDHEIGHT - y - 1
        if BOARDOUTERFRAME <= x < BOARDWIDTH - BOARDOUTERFRAME and BOARDOUTERFRAME <= y < BOARDHEIGHT - BOARDOUTERFRAME:
            x -= BOARDOUTERFRAME
            y -= BOARDOUTERFRAME
            if x % (FIELDWIDTH + BOARDINNERFRAME) < FIELDWIDTH and y % (FIELDHEIGHT + BOARDINNERFRAME) < FIELDHEIGHT:
                return Coordinate(y // (FIELDHEIGHT + BOARDINNERFRAME), x // (FIELDWIDTH + BOARDINNERFRAME))
        return None

    def get_field(self, coord):
        # ToDo: figure out who is responsible for this
        return self.activegame.activeboard.get_field(coord)

    def start(self, whitearmy, blackarmy):
        # ToDo Move to appropriate responsible, just hacked for now
        self.activegame = ChessGame()
        black = blackarmy(ARMY_BLACK, self.activegame.activeboard)
        white = whitearmy(ARMY_WHITE, self.activegame.activeboard)
        self.activegame.activeboard.black_army = black
        self.activegame.activeboard.white_army = white
        black.setup()
        white.setup()
        self.activegame.activeplayer = ARMY_WHITE
        self.activegame.start_turn()


def _draw_field(field, painter, x, y, width, height, **kwargs):
    if (field.row + field.column) % 2 == 0:
        color = QColor(0x8B4513)
    else:
        color = QColor(0xFFF8DC)

    if 'selected' in kwargs:
        color = QColor(0x00FF00)

    if 'action' in kwargs:
        color = QColor(0xFFFF44)

    if 'move' in kwargs:
        color = QColor(0x0080FF)

    if 'capture' in kwargs:
        color = QColor(0xFF8000)

    if 'move' in kwargs and 'capture' in kwargs:
        color = QColor(0xAA0000)

    painter.fillRect(x, y, width, height, color)

    if field.piece is not None:
        pixmap = PictureCache.get_pixmap(field.piece.picture, field.piece.color)
        painter.drawPixmap(x + 2, y + 2, width - 2, height - 2, pixmap, 0, 0, width - 2, height - 2)
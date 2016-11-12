from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import Qt

from .Constants import *
from .BoardFrameImpl import BoardFrame
from Chess3 import Armies
from Chess3 import ArmyBase

import importlib
import pkgutil
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Chess 3')
        self.setFixedSize(958, 596)
        self.boardframe = BoardFrame(parent=self)

        self._armies = self._load_all_armies()

        startButton = QPushButton("&Start", self)
        startButton.setFocusPolicy(Qt.NoFocus)
        startButton.setGeometry(BOARDWIDTH + 40, 20, 50, 20)
        startButton.clicked.connect(self.start)

        activePlayer = QLabel(self)
        activePlayer.setGeometry(QRect(BOARDWIDTH + 40, 110, 60, 30))

        check = QLabel(self)
        check.setGeometry(QRect(BOARDWIDTH + 40, 150, 60, 30))

        winner = QLabel(self)
        winner.setGeometry(QRect(BOARDWIDTH + 40, 190, 60, 30))

        self.whiteArmyBox = QComboBox(self)
        self.whiteArmyBox.setGeometry(QRect(BOARDWIDTH + 110, 20, 100, 20))
        for armyname in self._armies.keys():
            self.whiteArmyBox.addItem(armyname)
            self.whiteArmyBox.setCurrentIndex(0)

        self.blackArmyBox = QComboBox(self)
        self.blackArmyBox.setGeometry(QRect(BOARDWIDTH + 110, 50, 100, 20))
        for armyname in self._armies.keys():
            self.blackArmyBox.addItem(armyname)
            self.blackArmyBox.setCurrentIndex(0)

    def start(self):
        try:
            self.boardframe.start(self._armies[str(self.whiteArmyBox.currentText())], self._armies[str(self.blackArmyBox.currentText())])
        except:
            import traceback
            traceback.print_exc()
            raise
        self.boardframe.update()

    def _load_all_armies(self):

        ret = {}

        if not getattr(sys, 'frozen', False):
            # in non deployment version, we discover dynamically
            def import_submodules(package):
                if isinstance(package, str):
                    package = importlib.import_module(package)
                for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
                    full_name = package.__name__ + '.' + name
                    try:
                        importlib.import_module(full_name)
                        if is_pkg:
                            import_submodules(full_name)
                    except ImportError:
                        pass

            import_submodules(Armies)

        for army in ArmyBase.__subclasses__():
            if army is not ArmyBase:
                # ToDo: catch duplicates, add explicit name attribute
                ret[army.__name__] = army

        return ret

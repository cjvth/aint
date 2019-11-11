import sqlite3

from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QLabel, QPushButton, QGraphicsWidget

from src.colorChoose import ColorChoose
from src.field import Field
from src.instrument import Instrument
from ui.mainWindowUI import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_buttons()
        self.instruments_db = sqlite3.connect('db/instruments.db')
        self.i_cur = self.instruments_db.cursor()
        ins = self.i_cur.execute("SELECT id, name FROM instruments")
        self.instruments = []
        for i in ins:
            inst = Instrument(i[0], i[1], self)
            self.instruments.append(inst)
            self.instrumentsBar.addAction(inst)
        self.current_instrument = 0
        self.delta_x = 0
        self.delta_y = 0

        self.colorChoose = ColorChoose(self.foregroundColorChange,
                                       self.backgroundColorChange, self.swapColors)

    def connect_buttons(self):
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)

    def new(self):
        self.field.layers = []
        self.field.layers.append(Image.new('RGB', (200, 200), color=(255, 255, 255)))
        self.field.draw()
        self.update_deltas()

    def open(self):
        self.instrumented(50, 50)

    def save(self):
        pass

    def instrumented(self, x, y):
        if id == 0:  # Если будут инструменты, которые надо по-другому обрабатывать
            pass
        else:
            self.field.instrumented(self.current_instrument, x - self.delta_x, y - self.delta_y)

    def mousePressEvent(self, event):
        self.field.new_drawing_layer()
        self.instrumented(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.instrumented(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.field.paste_drawing_layer()

    def update_deltas(self):
        try:
            sz = self.field.pixmap().size()
        except AttributeError:
            return
        imho_geom = self.imHolder.geometry()
        self.delta_x = imho_geom.x() + imho_geom.width() // 2 - (sz.width() + 1) // 2
        self.delta_y = imho_geom.y() + imho_geom.height() // 2 - (sz.height() + 1) // 2 + \
                       self.menubar.height() + self.instrumentsBar.height()

    def resizeEvent(self, event):
        self.update_deltas()

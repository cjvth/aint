import sqlite3

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from src.field import Field
from src.instrument import Instrument
from ui.mainWindowUI import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_buttons()
        self.instruments_db = sqlite3.connect('db/instruments.db')
        self.field = Field(self.imHolderContents)
        self.field.setObjectName("field")
        self.pictureHolder.addWidget(self.field, 0, 0, 1, 1)
        self.i_cur = self.instruments_db.cursor()
        ins = self.i_cur.execute("SELECT id, name FROM instruments")
        self.instruments = []
        for i in ins:
            inst = Instrument(i[0], i[1], self)
            self.instruments.append(inst)
            self.instrumentsBar.addAction(inst)


    def connect_buttons(self):
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)

    def new(self):
        self.field.layers = []
        self.field.layers.append(Image.new('RGB', (200, 200), color=(255, 255, 255)))
        self.field.draw()

    def open(self):
        pass

    def save(self):
        pass

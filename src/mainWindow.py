from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from src.field import Field
from ui.mainWindowUI import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_buttons()
        self.horizontalScrollBar.hide()
        self.verticalScrollBar.hide()
        self.field = Field(self.centralwidget)
        self.field.setObjectName("field")
        self.gridLayout.addWidget(self.field, 0, 2, 1, 1)
        self.field.setAlignment(QtCore.Qt.AlignCenter)

    def connect_buttons(self):
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)

    def new(self):
        self.field.layers.append(Image.new('RGB', (200, 200), color=(255, 255, 255)))
        self.field.draw()

    def open(self):
        pass

    def save(self):
        pass

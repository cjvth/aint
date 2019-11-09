from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class Field(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.layers = []

    def draw(self):
        self.setPixmap(QPixmap.fromImage(ImageQt(self.layers[0])))

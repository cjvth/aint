from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView


class ClickableGraphicsView(QGraphicsView):
    clicked = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit()

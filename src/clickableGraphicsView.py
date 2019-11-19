from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView


class ClickableGraphicsView(QGraphicsView):
    """
    QGraphicsView but reacts for pressing
    """
    clicked = pyqtSignal()

    def __init__(self, parent):
        """
        :param parent: parent, let it be
        """
        super().__init__(parent)

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit()

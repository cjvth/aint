from PyQt5.QtWidgets import QMainWindow

from ui.mainWindowUI import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.horizontalScrollBar.hide()
        self.verticalScrollBar.hide()

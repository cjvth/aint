from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QGraphicsView, QWidget, QColorDialog, QGraphicsScene

from src.clickableGraphicsView import ClickableGraphicsView


class ColorChoose:
    def __init__(self, fore: ClickableGraphicsView,
                 back: ClickableGraphicsView, swap: QPushButton):
        self.fore_scene = QGraphicsScene(fore.parent())
        fore.setScene(self.fore_scene)
        self.back_scene = QGraphicsScene(back.parent())
        back.setScene(self.back_scene)
        fore.clicked.connect(self.change_foreground)
        back.clicked.connect(self.change_background)
        swap.clicked.connect(self.swap)
        self.fore_color = QColor(0, 0, 0)
        self.back_color = QColor(255, 255, 255)
        self.fore_scene.addRect(-5, -5, 37, 37, self.fore_color, self.fore_color)
        self.back_scene.addRect(-5, -5, 37, 37, self.back_color, self.back_color)

    def change_foreground(self):
        color = QColorDialog.getColor()
        self.fore_scene.addRect(-5, -5, 37, 37, color, color)
        self.fore_color = color

    def change_background(self):
        color = QColorDialog.getColor()
        self.back_scene.addRect(-5, -5, 37, 37, color, color)
        self.back_color = color

    def swap(self):
        self.fore_color, self.back_color = self.back_color, self.fore_color
        self.fore_scene.addRect(-5, -5, 37, 37, self.fore_color, self.fore_color)
        self.back_scene.addRect(-5, -5, 37, 37, self.back_color, self.back_color)

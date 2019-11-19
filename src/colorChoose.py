import sqlite3

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QColorDialog, QGraphicsScene

from src.clickableGraphicsView import ClickableGraphicsView


# noinspection DuplicatedCode
class ColorChoose:
    """
    Contains two clickableGraphicsView objects
    Allows user to choose color, saves preferences into database
    """
    def __init__(self, fore: ClickableGraphicsView, back: ClickableGraphicsView, swap: QPushButton,
                 connection, cursor: sqlite3.Cursor):
        """
        :param fore: foreground color changer
        :param back: background color changer
        :param swap: swap colors
        :param connection: connection to the database
        :param cursor: connection cursor
        """
        self.connect = connection
        self.cursor = cursor
        self.fore_scene = QGraphicsScene(fore.parent())
        fore.setScene(self.fore_scene)
        self.back_scene = QGraphicsScene(back.parent())
        back.setScene(self.back_scene)
        fore.clicked.connect(self.change_foreground)
        back.clicked.connect(self.change_background)
        # noinspection PyUnresolvedReferences
        swap.clicked.connect(self.swap)
        self.fore_color = self.cursor.execute("""SELECT r, g, b FROM color
        WHERE ground='fore'""").fetchall()[0]
        self.back_color = self.cursor.execute("""SELECT r, g, b FROM color 
        WHERE ground='back'""").fetchall()[0]
        self.fore_scene.addRect(-5, -5, 37, 37, QColor(*self.fore_color), QColor(*self.fore_color))
        self.back_scene.addRect(-5, -5, 37, 37, QColor(*self.back_color), QColor(*self.back_color))

    def change_foreground(self):
        """
        When user changes foreground color
        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.fore_scene.addRect(-5, -5, 37, 37, color, color)
            self.fore_color = (color.red(), color.green(), color.blue())
            self.cursor.execute(f"""UPDATE color SET (r, g, b) = {self.fore_color} 
                                    WHERE ground='fore'""")
            self.connect.commit()

    def change_background(self):
        """
        When user changes background color
        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.back_scene.addRect(-5, -5, 37, 37, color, color)
            self.back_color = (color.red(), color.green(), color.blue())
            self.cursor.execute(f"""UPDATE color SET (r, g, b) = {self.back_color} 
                                    WHERE ground='back'""")
            self.connect.commit()

    def swap(self):
        """
        Swaps colors
        """
        self.fore_color, self.back_color = self.back_color, self.fore_color
        self.fore_scene.addRect(-5, -5, 37, 37, QColor(*self.fore_color), QColor(*self.fore_color))
        self.back_scene.addRect(-5, -5, 37, 37, QColor(*self.back_color), QColor(*self.back_color))
        self.cursor.execute(f"UPDATE color SET (r, g, b) = {self.fore_color} WHERE ground='fore'")
        self.cursor.execute(f"UPDATE color SET (r, g, b) = {self.back_color} WHERE ground='back'")
        self.connect.commit()

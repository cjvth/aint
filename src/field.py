from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QLabel

from src.colorChoose import ColorChoose


class Field(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.layers = []
        self.drawing_layer = None
        self.color_choose = None
        self.mainWindow = None

    def set_color_choose(self, color_choose: ColorChoose):
        self.color_choose: ColorChoose = color_choose

    def set_main_window(self, mw):
        self.mainWindow = mw

    def draw(self):
        if len(self.layers) == 0:
            pass
        elif self.drawing_layer is None:
            self.setPixmap(QPixmap.fromImage(ImageQt(self.layers[0])))
        else:
            res = self.layers[0].copy()
            res.paste(self.drawing_layer.convert('RGB'), (0, 0), self.drawing_layer)
            self.setPixmap(QPixmap.fromImage(ImageQt(res)))
            a = res.load()
            pass

    def new_drawing_layer(self):
        if len(self.layers) > 0:
            self.drawing_layer = Image.new('RGBA', self.layers[0].size)

    def instrumented(self, i_id, x, y):
        if self.drawing_layer is None:
            return
        draw = ImageDraw.Draw(self.drawing_layer)
        r = int(self.mainWindow.brushSize.text())
        if i_id == 1:
            color = self.color_choose.fore_color
            draw.ellipse((x - r // 2, y - r // 2, x + (r + 1) // 2, y + (r + 1) // 2), fill=color)
        elif i_id == 2:
            color = self.color_choose.back_color
            draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
        self.draw()

    def paste_drawing_layer(self):
        if len(self.layers) > 0:
            self.layers[0].paste(self.drawing_layer.convert('RGB'), (0, 0), self.drawing_layer)
            self.drawing_layer = None

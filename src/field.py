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
        self.inst_data = []

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
            pass

    def new_drawing_layer(self):
        if len(self.layers) > 0:
            self.drawing_layer = Image.new('RGBA', self.layers[0].size)

    def drawing_started(self, i_id, x, y):
        if i_id == 5:
            self.inst_data = [(x, y)]

    def drawing_ended(self, i_id, x, y):
        pass

    def instrumented(self, i_id, x, y):
        if self.drawing_layer is None:
            return
        if i_id in (1, 2):
            draw = ImageDraw.Draw(self.drawing_layer)
            r = int(self.mainWindow.brushSize.text()) / 2
            if i_id == 1:
                draw.ellipse((x - r, y - r, x + r, y + r), fill=self.color_choose.fore_color)
            elif i_id == 2:
                draw.ellipse((x - r, y - r, x + r, y + r), fill=self.color_choose.back_color)
        elif i_id == 5:
            self.drawing_layer = Image.new('RGBA', self.layers[0].size)
            draw = ImageDraw.Draw(self.drawing_layer)
            draw.line(self.inst_data[0] + (x, y), fill=self.color_choose.fore_color,
                      width=self.mainWindow.brushSize.value())
        self.draw()

    def paste_drawing_layer(self):
        if len(self.layers) > 0:
            self.layers[0].paste(self.drawing_layer.convert('RGB'), (0, 0), self.drawing_layer)
            self.drawing_layer = None

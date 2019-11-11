from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class Field(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.layers = []
        self.drawing_layer = None

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
        p = self.parent()
        r = 5
        if i_id == 1:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=(0, 0, 0))
        elif i_id == 2:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))
        self.draw()

    def paste_drawing_layer(self):
        if len(self.layers) > 0:
            self.layers[0].paste(self.drawing_layer.convert('RGB'), (0, 0), self.drawing_layer)
            self.drawing_layer = None

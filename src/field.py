from time import sleep

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from src.colorChoose import ColorChoose


class Field(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = Image.new('RGB', (300, 300), (255, 255, 255))
        self.image_draw = ImageDraw.Draw(self.image)
        self.mainWindow = None
        self.color_choose = None
        self.drawer = Drawer(self)
        self.inst_data = []
        self.original_image = None

    def new_image(self):
        self.image = Image.new('RGB', (300, 300), (255, 255, 255))
        self.image_draw = ImageDraw.Draw(self.image)
        self.drawer.stop()
        self.inst_data = []
        self.original_image = None
        self.draw()

    def set_friends(self, color_choose: ColorChoose, mw):
        self.color_choose = color_choose
        self.mainWindow = mw

    def draw(self):
        if self.image is None:
            return
        self.setPixmap(QPixmap.fromImage(ImageQt(self.image)))

    def drawing_started(self, i_id, x, y):
        self.original_image = self.image.copy()
        if i_id == 5:
            self.inst_data = [(x, y)]
        self.drawer.working = True
        if not self.drawer.isRunning():
            self.drawer.start()

    def drawing_ended(self, i_id, x, y):
        self.drawer.stop()
        if i_id == 5:
            self.image_draw = ImageDraw.Draw(self.image)

    def instrumented(self, i_id, x, y):
        if self.image is None:
            return
        if i_id in (1, 2):
            r = int(self.mainWindow.brushSize.text()) / 2
            if i_id == 1:
                self.image_draw.ellipse((x - r, y - r, x + r, y + r),
                                        fill=self.color_choose.fore_color)
            elif i_id == 2:
                self.image_draw.ellipse((x - r, y - r, x + r, y + r),
                                        fill=self.color_choose.back_color)
        elif i_id == 5:
            alpha = Image.new('RGBA', self.image.size)
            draw = ImageDraw.Draw(alpha)
            draw.line(self.inst_data[0] + (x, y), fill=self.color_choose.fore_color,
                      width=self.mainWindow.brushSize.value())
            self.image = self.original_image.copy()
            self.image.paste(alpha.convert('RGB'), (0, 0), alpha)


class Drawer(QThread):
    def __init__(self, field):
        super().__init__()
        self.field = field
        self.working = False

    def run(self):
        while True:
            if self.working:
                self.field.setPixmap(QPixmap.fromImage(ImageQt(self.field.image)))
                sleep(0.02)
            else:
                while not self.working:
                    sleep(0.02)

    def stop(self):
        self.working = False

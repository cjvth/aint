from time import sleep

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QComboBox

from src.colorChoose import ColorChoose


class Field(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = None
        self.image_draw = None
        from src.mainWindow import MainWindow
        # noinspection PyTypeChecker
        self.mainWindow: MainWindow = None
        self.color_choose = None
        self.drawer = Drawer(self)
        self.inst_data = []
        self.original_image = None
        self.history = []
        self.history_pos = 0

    def new_image(self):
        self.image = Image.new('RGBA', (500, 500), (255, 255, 255, 255))
        self.image_draw = ImageDraw.Draw(self.image)
        self.drawer.stop()
        self.inst_data = []
        self.original_image = None
        self.draw()
        self.history = [self.image.copy()]
        self.history_pos = 0
        self.mainWindow.action_undo.setDisabled(True)
        self.mainWindow.action_redo.setDisabled(True)

    def open_image(self, im):
        self.image = im
        self.image_draw = ImageDraw.Draw(self.image)
        self.drawer.stop()
        self.inst_data = []
        self.original_image = None
        self.draw()
        self.history = [self.image.copy()]
        self.history_pos = 0
        self.mainWindow.action_undo.setDisabled(True)
        self.mainWindow.action_redo.setDisabled(True)

    def set_friends(self, color_choose: ColorChoose, mw):
        self.color_choose = color_choose
        self.mainWindow = mw
        self.mainWindow.action_undo.setDisabled(True)
        self.mainWindow.action_redo.setDisabled(True)

    def draw(self):
        if self.image is None:
            return
        self.setPixmap(QPixmap.fromImage(ImageQt(self.image)))

    def drawing_started(self, i_id, x, y):
        if self.image is None:
            return
        self.original_image = self.image.copy()
        self.inst_data = [[x, y]]
        self.drawer.working = True
        if not self.drawer.isRunning():
            self.drawer.start()

    def drawing_ended(self, i_id, x, y, cancel=False):
        if cancel:
            sleep(0.01)
            self.image = self.original_image
            self.image_draw = ImageDraw.Draw(self.image)
            return
        if self.image is None:
            return
        self.drawer.stop()
        if i_id == 5:
            self.image_draw = ImageDraw.Draw(self.image)
        if not self.image == self.history[self.history_pos]:
            self.history = [self.image.copy()] + self.history[self.history_pos:]
            self.history = self.history[:10]
            self.history_pos = 0
            self.mainWindow.action_undo.setEnabled(True)
            self.mainWindow.action_redo.setDisabled(True)
        self.original_image = None

    def instrumented(self, i_id, x, y):
        if self.image is None or len(self.inst_data) == 0:
            return
        if i_id in (1, 2):
            r = self.mainWindow.brushSize.value()
            if i_id == 1:
                color = self.color_choose.fore_color
            else:
                color = self.color_choose.back_color
            self.image_draw.ellipse((x - (r - 1) // 2, y - (r - 1) // 2, x + r // 2, y + r // 2),
                                    fill=color)
            self.image_draw.line(self.inst_data[0] + [x, y], fill=color,
                                 width=self.mainWindow.brushSize.value())
            self.inst_data[0] = [x, y]
        elif i_id == 5:
            alpha = Image.new('RGBA', self.image.size)
            draw = ImageDraw.Draw(alpha)
            figure = self.mainWindow.figure.currentIndex()
            if figure == 0:
                draw.line(self.inst_data[0] + [x, y], fill=self.color_choose.fore_color,
                          width=self.mainWindow.brushSize.value())
            elif figure in (1, 2):
                if self.mainWindow.noFill.isChecked():
                    fill = None
                elif self.mainWindow.frontFill.isChecked():
                    fill = self.color_choose.fore_color
                else:
                    fill = self.color_choose.back_color
                if figure == 1:
                    draw.rectangle(self.inst_data[0] + [x, y], fill=fill,
                                   outline=self.color_choose.fore_color,
                                   width=self.mainWindow.brushSize.value())
                elif figure == 2:
                    a = self.inst_data[0] + [x, y]
                    if a[0] > a[2]:
                        a[0], a[2] = a[2], a[0]
                    if a[1] > a[3]:
                        a[1], a[3] = a[3], a[1]
                    draw.ellipse(self.inst_data[0] + [x, y], fill=fill,
                                 outline=self.color_choose.fore_color,
                                 width=self.mainWindow.brushSize.value())
            self.image = self.original_image.copy()
            self.image.paste(alpha, (0, 0), alpha)
            sleep(0.02)

    def undo(self):
        if len(self.history) > self.history_pos + 1:
            self.history_pos += 1
            self.image = self.history[self.history_pos].copy()
            self.image_draw = ImageDraw.Draw(self.image)
            self.original_image = None
            self.draw()
            self.mainWindow.action_redo.setEnabled(True)
            if len(self.history) <= self.history_pos + 1:
                self.mainWindow.action_undo.setDisabled(True)

    def redo(self):
        if self.history_pos > 0:
            self.history_pos -= 1
            self.image = self.history[self.history_pos].copy()
            self.image_draw = ImageDraw.Draw(self.image)
            self.original_image = None
            self.draw()
            self.mainWindow.action_undo.setEnabled(True)
            if self.history_pos <= 0:
                self.mainWindow.action_redo.setDisabled(True)


class Drawer(QThread):
    def __init__(self, field):
        super().__init__()
        self.field = field
        self.working = False

    def run(self):
        while self.working:
            self.field.setPixmap(QPixmap.fromImage(ImageQt(self.field.image)))
            sleep(0.02)
        sleep(0.02)
        self.field.setPixmap(QPixmap.fromImage(ImageQt(self.field.image)))

    def stop(self):
        self.working = False

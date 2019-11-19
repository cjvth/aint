import sqlite3

from PIL import Image
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from src.colorChoose import ColorChoose
from src.instrument import Instrument
from src.optionsPreferences import OptionsPreferences
from ui.mainWindowUI import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_events()
        self.i_db = sqlite3.connect('db/instruments.db')
        self.i_cursor = self.i_db.cursor()
        self.instruments = []
        self.init_instruments()
        self.curr_inst = 0
        self.init_options()
        self.delta_x = 0
        self.delta_y = 0
        self.must_update_deltas = False

        self.drawing = False

        self.op = OptionsPreferences(self, self.i_db, self.i_cursor)
        self.colorChoose = ColorChoose(self.foregroundColorChange, self.backgroundColorChange,
                                       self.swapColors, self.i_db, self.i_cursor)
        self.field.set_friends(self.colorChoose, self)

    def init_instruments(self):
        ins = self.i_cursor.execute("SELECT id, name FROM instruments")
        for i in ins:
            inst = Instrument(i[0], i[1], self)
            self.instruments.append(inst)
            self.instrumentsBar.addAction(inst)
            if i[0] <= 10:
                inst.setShortcut('CTRL+' + str(i[0] % 10))

    def init_options(self):
        options = [self.colorChanger,
                   self.brushSizeChanger,
                   self.figureChanger,
                   self.figureFillChanger
                   ]
        for i in options:
            i.hide()
        figures = self.i_cursor.execute("SELECT name, id FROM figures").fetchall()
        for i in figures:
            self.figure.addItem(i[0], i[1])
        self.figure.setCurrentIndex(-1)
        self.instrumentName.setText("")

    def connect_events(self):
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)
        self.action_undo.triggered.connect(self.field.undo)
        self.action_redo.triggered.connect(self.field.redo)
        self.imHolder.verticalScrollBar().valueChanged.connect(self.update_delta_y)
        self.imHolder.horizontalScrollBar().valueChanged.connect(self.update_delta_x)

    def new(self):
        self.field.new_image()
        self.must_update_deltas = True

    def open(self):
        f = '*.bmp *.eps *.gif *.icns *.ico *.jpg *.jpeg *.pcx *.png *.ppm *.sgi *.tga *.tif *.tiff'
        filename = QFileDialog.getOpenFileName(self, 'Открыть', './imsave/im.', filter=f)
        if filename[1] == '':
            return
        split = filename[0].split('/')[-1].split('\\')[-1].split('.')
        if split[0] == '' or len(split) > 1 and split[-1] == '':
            self.statusbar.showMessage('Ошибка: не задано имя файла', 5000)
            return
        try:
            im: Image.Image = Image.open(filename[0])
            im = im.convert('RGBA')
        except FileNotFoundError:
            self.statusbar.showMessage('Файл не найден', 5000)
            return
        self.field.open_image(im)
        self.must_update_deltas = True

    def save(self):
        f = '*.bmp *.eps *.gif *.icns *.ico *.jpg *.jpeg *.pcx *.png *.ppm *.sgi *.tga *.tif *.tiff'
        filename = QFileDialog.getSaveFileName(self, 'Сохранить', './imsave/im.', filter=f)
        if filename[1] == '':
            return
        split = filename[0].split('/')[-1].split('\\')[-1].split('.')
        if split[0] == '':
            self.statusbar.showMessage('Ошибка: не задано имя файла', 5000)
            return
        elif len(split) == 1:
            filename = (filename[0] + '.png', filename[1])
        elif split[-1] == '':
            filename = (filename[0][:-1] + '.png', filename[1])
        im: Image.Image = self.field.image
        try:
            im.save(filename[0])
        except FileNotFoundError:
            # Символ / воспринимается как разделитель папки
            self.statusbar.showMessage('Ошибка: использование запрещённых символов', 5000)
        except (ValueError, OSError):
            try:
                im.convert('RGBA').save(filename[0])
            except (ValueError, OSError):
                im.convert('RGB').save(filename[0])
        except AttributeError:
            self.statusbar.showMessage('Ошибка: файл не создан', 5000)
        except ValueError:
            self.statusbar.showMessage('Ошибка: неизвестное расширение файла', 5000)

    def instrumented(self, x, y):
        self.field.instrumented(self.curr_inst, x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.drawing = False
            self.field.drawing_ended(self.curr_inst, 0, 0, True)
        elif event.button() == Qt.LeftButton:
            if self.imHolder.x() <= event.x() <= self.imHolder.x() + self.imHolder.width() and \
                    self.imHolder.y() <= event.y() - self.menubar.height() - \
                    self.instrumentsBar.height() <= self.imHolder.y() + self.imHolder.height():
                self.drawing = True
            else:
                self.drawing = False
                return
            if self.must_update_deltas:
                self.update_delta_x()
                self.update_delta_y()
                self.must_update_deltas = False
            x, y = self.pixel_coords(event.x(), event.y())
            self.field.drawing_started(self.curr_inst, x, y)
            self.instrumented(x, y)

    def mouseMoveEvent(self, event):
        if not self.drawing:
            return
        x, y = self.pixel_coords(event.x(), event.y())
        hor = self.imHolder.horizontalScrollBar()
        if hor.isVisible():
            if x < hor.value():
                hor.setValue(x)
            elif x >= hor.value() + hor.pageStep():
                hor.setValue(x - hor.pageStep())
        ver = self.imHolder.verticalScrollBar()
        if ver.isVisible():
            if y < ver.value():
                ver.setValue(y)
            elif y >= ver.value() + ver.pageStep():
                ver.setValue(y - ver.pageStep())
        self.instrumented(*self.pixel_coords(event.x(), event.y()))

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.field.drawing_ended(self.curr_inst, *self.pixel_coords(event.x(), event.y()))
        self.drawing = False

    def update_delta_x(self):
        try:
            sz = self.field.pixmap().size()
        except AttributeError:
            return
        imho_geom = self.imHolder.geometry()
        if self.imHolder.horizontalScrollBar().isVisible():
            self.delta_x = imho_geom.x() - self.imHolder.horizontalScrollBar().value()
        else:
            self.delta_x = imho_geom.x() + imho_geom.width() // 2 - (sz.width() + 1) // 2

    def update_delta_y(self):
        try:
            sz = self.field.pixmap().size()
        except AttributeError:
            return
        imho_geom = self.imHolder.geometry()
        self.delta_y = self.menubar.height() + self.instrumentsBar.height()
        if self.imHolder.verticalScrollBar().isVisible():
            self.delta_y += imho_geom.y() - self.imHolder.verticalScrollBar().value()
        else:
            self.delta_y += imho_geom.y() + imho_geom.height() // 2 - (sz.height() + 1) // 2

    def resizeEvent(self, event):
        self.must_update_deltas = True

    def pixel_coords(self, x, y):
        return x - self.delta_x, y - self.delta_y


class Drawer(QThread):
    def __init__(self, mw: MainWindow):
        super().__init__()
        self.mw = mw
        self.working = False

    def run(self):
        while self.working:
            pass

    def stop(self):
        self.working = False

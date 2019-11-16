import sqlite3

from PyQt5.QtWidgets import QMainWindow

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
        self.instrumentName.setText("")

    def connect_events(self):
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)

    def new(self):
        self.field.new_image()
        self.update_deltas()

    def open(self):
        self.instrumented(50, 50)

    def save(self):
        pass

    def instrumented(self, x, y):
        if id == 0:  # Если будут инструменты, которые надо по-другому обрабатывать
            pass
        else:
            self.field.instrumented(self.curr_inst, x, y)

    def mousePressEvent(self, event):
        x, y = self.pixel_coords(event.x(), event.y())
        self.field.drawing_started(self.curr_inst, x, y)
        self.instrumented(x, y)

    def mouseMoveEvent(self, event):
        self.instrumented(*self.pixel_coords(event.x(), event.y()))

    def mouseReleaseEvent(self, event):
        self.field.drawing_ended(self.curr_inst, *self.pixel_coords(event.x(), event.y()))

    def update_deltas(self):
        try:
            sz = self.field.pixmap().size()
        except AttributeError:
            return
        imho_geom = self.imHolder.geometry()
        self.delta_x = imho_geom.x() + imho_geom.width() // 2 - (sz.width() + 1) // 2
        self.delta_y = imho_geom.y() + imho_geom.height() // 2 - (sz.height() + 1) // 2 + \
            self.menubar.height() + self.instrumentsBar.height()

    def resizeEvent(self, event):
        self.update_deltas()

    def pixel_coords(self, x, y):
        return x - self.delta_x, y - self.delta_y

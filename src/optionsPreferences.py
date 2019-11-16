class OptionsPreferences:
    def __init__(self, main_window, connection, cursor):
        from src.mainWindow import MainWindow
        self.mw: MainWindow = main_window
        self.con = connection
        self.cur = cursor

        self.mw.brushSize.valueChanged.connect(self.brush_size)
        self.mw.figure.currentIndexChanged.connect(self.figure)

    def brush_size(self):
        x = self.mw.brushSize.value()
        self.cur.execute(f"UPDATE instruments SET size = {x} WHERE id = {self.mw.curr_inst}")
        self.con.commit()

    def figure(self):
        x = self.mw.figure.currentIndex()
        self.cur.execute(f"UPDATE instruments SET figure = {x} WHERE id = {self.mw.curr_inst}")
        self.con.commit()

class OptionsPreferences:
    def __init__(self, main_window, connection, cursor):
        from src.mainWindow import MainWindow
        self.mw: MainWindow = main_window
        self.con = connection
        self.cur = cursor

        self.mw.brushSize.valueChanged.connect(self.brush_size)
        self.mw.figure.currentIndexChanged.connect(self.figure)
        self.mw.figureFillChangerGroup.buttonClicked.connect(self.figure_fill_changer_group)

    def brush_size(self):
        x = self.mw.brushSize.value()
        self.cur.execute(f"UPDATE instruments SET size = {x} WHERE id = {self.mw.curr_inst}")
        self.con.commit()

    def figure(self):
        x = self.mw.figure.currentIndex()
        a = self.cur.execute(f"SELECT fill FROM figures WHERE id = {x}").fetchall()[0][0]
        if a is not None:
            self.mw.figureFillChanger.show()
            if a == 0:
                self.mw.noFill.toggle()
            elif a == 1:
                self.mw.frontFill.toggle()
            else:
                self.mw.backFill.toggle()
        else:
            self.mw.figureFillChanger.hide()
        self.cur.execute(f"UPDATE instruments SET figure = {x} WHERE id = {self.mw.curr_inst}")
        self.con.commit()

    def figure_fill_changer_group(self, chosen):
        if chosen is self.mw.noFill:
            x = 0
        elif chosen is self.mw.frontFill:
            x = 1
        else:
            x = 2
        self.cur.execute(f"""UPDATE figures SET fill = {x} 
                             WHERE id = {self.mw.figure.currentIndex()}""")
        self.con.commit()

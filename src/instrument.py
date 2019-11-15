from PyQt5.QtWidgets import QAction


class Instrument(QAction):
    def __init__(self, id_, name, parent):
        super().__init__(name, parent)
        self.id = id_
        self.triggered.connect(self.chosen)
        self.setObjectName(name)

    def chosen(self):
        from src.mainWindow import MainWindow
        p: MainWindow = self.parent()
        options = [
            (p.colorChanger, 'colorized'),
            (p.brushSizeChanger, 'size')
        ]
        p.cur_inst = self.id
        cur = p.i_cur
        for i in options:
            a = cur.execute(f"SELECT {i[1]} FROM instruments WHERE id = {self.id}").fetchall()[0][0]
            if a is None:
                i[0].hide()
            else:
                i[0].show()
                if i[1] == 'size':
                    p.brushSize.setValue(a)
        p.instrumentName.setText(self.objectName())

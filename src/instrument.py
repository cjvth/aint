from PyQt5.QtWidgets import QAction


class Instrument(QAction):
    def __init__(self, id_, name, parent):
        """
        :param id_: id of an instrument
        :param name: name
        :param parent: parent, let it be here
        """
        super().__init__(name, parent)
        self.id = id_
        # noinspection PyUnresolvedReferences
        self.triggered.connect(self.chosen)
        self.setObjectName(name)

    def chosen(self):
        """
        If instrument is chosen, we need to show or hide and set values for instruments options
        And set its name into label
        """
        from src.mainWindow import MainWindow
        # noinspection PyTypeChecker
        p: MainWindow = self.parent()
        options = [
            (p.colorChanger, 'colorized'),
            (p.brushSizeChanger, 'size', p.brushSize.setValue),
            (p.figureFillChanger, 'figure'),
            (p.figureChanger, 'figure', p.figure.setCurrentIndex)
        ]
        p.curr_inst = self.id
        cur = p.i_cursor
        for i in options:
            a = cur.execute(f"SELECT {i[1]} FROM instruments WHERE id = {self.id}").fetchall()[0][0]
            if a is None:
                i[0].hide()
            else:
                i[0].show()
                if len(i) == 3:
                    i[2](a)
        p.instrumentName.setText(self.objectName())

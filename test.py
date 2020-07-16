import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from pyqtgameboards.HexagonBoard import QHexagonboard

if __name__ == '__main__':

    overlays = []
    overlay1brush = QtGui.QBrush(QtGui.QColor(0,255,0,150))
    overlay1pen = QtGui.QPen(QtGui.QColor(0,255,0))
    overlay1pen.setWidth(3)
    overlay1dict = {
        "Brush": overlay1brush,
        "Pen": overlay1pen,
        "Positions": [
            [1, 1], 
            [2, 1],
            [1, 2],
            [3, 3],
            ],
        }
    overlays.append(overlay1dict)

    global app
    app = QtWidgets.QApplication(sys.argv)
    global main
    main = QtWidgets.QMainWindow()

    main.setCentralWidget(QHexagonboard(
        horizontal = True, 
        rows = 20, 
        columns = 10,
        overlays = overlays,
        ))

    main.showMaximized()
    sys.exit(app.exec_())
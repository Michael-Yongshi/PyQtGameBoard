# PyQtGameBoard
PyQt5 widget that draws a board on the screen to include in games or map drawing application.

## Version
### 0.2
0.2.5   Added optional size parameter for the size of the tiles
        Added a rectangle board
0.2.4   removed some prints
0.2.3   fixed selection deleting previous overlays
        split mousepress method so its easier to subclass
        adding line of sight line
        return list of tiles touched by line of sight

0.2.2   Redone building board, zooming in / out and added selection of tile with drawing adjacent tiles

## Install
```
pip install pyqt-gameboard
```

## Import
```
from pyqtgameboards.HexagonBoard import QHexagonboard
```

## How to
to try out, copying the following to open a widget with a gameboard
This is a gameboard of 20 rows and 10 columns (feels like 20, as it only counts tiles at the same height)
This example creates designated tiles that receive a green fill with a thick green line

```
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
```

## Licence

Licensed under GPL-3.0-or-later, see LICENSE file for details.

Copyright © 2020 Michael-Yongshi.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

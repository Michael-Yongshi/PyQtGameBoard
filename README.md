# PyQtGameBoard
PyQt5 widget that draws a board on the screen to include in games or map drawing application.

## Install
```
pip install yongshi-pyqtgameboard
```

## Import
```
from pyqtgameboards.HexagonBoard import QHexagonboard
```

## How to
to try out, copying the following:
```
if __name__ == '__main__':

    global app
    app = QtWidgets.QApplication(sys.argv)

    global main
    main = QtWidgets.QMainWindow()
    main.setCentralWidget(QHexagonboard(
        horizontal = True, 
        rows = 20, 
        columns = 10
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

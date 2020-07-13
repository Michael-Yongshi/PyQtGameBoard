import sys, math

from PyQt5 import QtCore, QtGui, QtWidgets
from guidarktheme import widget_template

class QHexagonboard(QtWidgets.QFrame):
    def __init__(self, horizontal, rows, columns, specials):
        QtWidgets.QFrame.__init__(self)

        # set board parameters
        self.horizontal = horizontal
        self.rows = rows
        self.columns = columns
        self.specials = specials

    def paintEvent(self, event):
        """
        paints all shapes of the game
        
        Creates a gameboard of rows and columns of hexagons of a sepecific
        size. 
        A row consists of a number of hexagons that touch at the horizontal tip. 
        The offset hexagons in between them, offset above and below, are in
        a different row. This means that 4 columns already look like a board
        with 8 columns as the offset hexes are not counted for the same row.
        """

        #  painter is default white background surrounded by a black 1 width line
        painter = QtGui.QPainter(self)

        row = 0
        while row < self.rows:
            
            col = 0
            while col < self.columns:

                # default is for horizontal aligned board, if not we have to switch rows and columns and set the angle accordingly
                if self.horizontal == False:
                    # if row number is odd, offset the hexes nicely in between the columns of the previous
                    positiony = col * 36 if (row % 2) == 0 else col * 36 + 18
                    positionx = row * 10
                    # set the angle of the hexagon
                    angle = 90

                else:
                    # if row number is odd, offset the hexes nicely in between the columns of the previous
                    positionx = col * 36 if (row % 2) == 0 else col * 36 + 18
                    positiony = row * 10
                    # set the angle of the hexagon
                    angle = 0

                # create the hexagon at the specified location
                hexagon = QHexagon(self.width, self.height, positionx, positiony, 6, 12, angle)

                # set different style for this hex if applicable
                """ TO DO
                add drawing base first and only afterwards draw the 'special' tiles
                """

                # set default values
                brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
                painter.setBrush(brush)
                pen = QtGui.QPen(QtGui.QColor(0,0,0))
                pen.setWidth(1)
                painter.setPen(pen)

                for special in self.specials:
                    for tile in special["Positions"]:
                        if row == tile[0] and col == tile[1]:
                            painter.setBrush(special["Brush"])
                            painter.setPen(special["Pen"])
                            break

                # draw the shape
                painter.drawPolygon(hexagon)

                col += 1
            row += 1

class QHexagonFrame(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

    def paintEvent(self, event):
        # create the hexagon at the specified location
        hexagon = QHexagon(self.width, self.height, 0, 0, 6, 12, 0)

        # prepare draw, painter is default white background surrounded by a black 1 width line
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        painter.setBrush(brush)
        pen = QtGui.QPen(QtGui.QColor(0,0,0))
        pen.setWidth(1)
        painter.setPen(pen)

        # draw the shape
        painter.drawPolygon(hexagon)

class QHexagon(QtGui.QPolygonF):
    """
    polygon with number of sides, a radius, angle of the first point
    hexagon is made with 6 sides
    radius denotes the size of the shape, 
    angle of 
    0 makes a horizontal aligned hexagon (first point points flat), 
    90 makes a vertical aligned hexagon (first point points upwards)
    """

    def __init__(self, width, height, positionx, positiony, sides, radius, angle, brush = None, pen = None):
        QtWidgets.QWidget.__init__(self)
        
        self.positionx = positionx
        self.positiony = positiony
        self.sides = sides
        self.radius = radius
        self.angle = angle

        w = 360/self.sides                                                   # angle per step
        for i in range(self.sides):                                          # add the points of polygon
            t = w*i + self.angle
            x = self.positionx + self.radius*math.cos(math.radians(t))                        # horizontal alignment
            y = self.positiony + self.radius*math.sin(math.radians(t))                        # vertical alignment
            self.append(QtCore.QPointF(width()/2 +x, height()/2 + y)) 

def get_special_tiles():
    """
    Example how to create special tiles.
    List of enemies in red and list of allies in green

    Its created by creating a dictionary of 3 values, a brush value, a pen value
    and a list of positions where it applies
    """

    allybrush = QtGui.QBrush(QtGui.QColor(0,255,0,150))
    allypen = QtGui.QPen(QtGui.QColor(0,255,0))
    allypen.setWidth(3)

    allydict = {
        "Brush": allybrush,
        "Pen": allypen,
        "Positions": [
            [1, 3], 
            [1, 1],
        ],
        }

    enemybrush = QtGui.QBrush(QtGui.QColor(255,0,0,150))
    enemypen = QtGui.QPen(QtGui.QColor(255,0,0))
    enemypen.setWidth(3)

    enemydict = {
        "Brush": enemybrush,
        "Pen": enemypen,
        "Positions": [
            [2, 3],
            [3, 6],
        ],
        }

    specials = [allydict, enemydict]
    return specials


def test_hexagon():

    global app
    app = QtWidgets.QApplication(sys.argv)

    global main
    main = QtWidgets.QMainWindow()

    frame = QHexagonFrame()
    main.setCentralWidget(frame)

    main.showMaximized()
    
    sys.exit(app.exec_())

def test_board():

    global app
    app = QtWidgets.QApplication(sys.argv)

    global main
    main = QtWidgets.QMainWindow()
    
    specials = get_special_tiles()
    frame = QHexagonboard(horizontal = True, rows = 20, columns = 10, specials = specials)
    main.setCentralWidget(frame)

    main.showMaximized()
    
    sys.exit(app.exec_())

if __name__ == '__main__':

    # test_hexagon()
    test_board()
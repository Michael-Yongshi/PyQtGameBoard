import sys, math

from PyQt5 import QtCore, QtGui, QtWidgets
from guidarktheme import widget_template

class QHexagonboard(QtWidgets.QFrame):
    def __init__(self, horizontal, rows, columns, overlays):
        QtWidgets.QFrame.__init__(self)

        # set board parameters
        self.horizontal = horizontal
        self.rows = rows
        self.columns = columns
        self.overlays = overlays

    def paintEvent(self, event):
        """       
        Creates a gameboard of rows and columns of hexagons of a sepecific
        size. 

        the default board consists of a number of hexagons that touch at the horizontal tip. 
        The offset hexagons in between them, offset above and below, are in
        a different row. This means that 4 columns already look like a board
        with 8 columns as the offset hexes are not counted for the same row.
        """

        painter = QtGui.QPainter(self)
        self.paint_underlay(painter)
        self.paint_overlays(painter)

    def paint_underlay(self, painter):
        """
        The basis of the gameboard
        this method creates a hexagon for all the rows and columns
        """

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        painter.setBrush(brush)
        pen = QtGui.QPen(QtGui.QColor(0,0,0))
        pen.setWidth(1)
        painter.setPen(pen)

        # Create hexagons for all the rows and columns
        row = 0
        while row < self.rows:
            
            col = 0
            while col < self.columns:

                # create the hexagon at the specified location
                positionx, positiony, angle = self.get_hexagon_position(row, col, self.horizontal)
                hexagon = QHexagon(self.width, self.height, positionx, positiony, 6, 12, angle)

                # draw the shape
                painter.drawPolygon(hexagon)

                col += 1
            row += 1

    def paint_overlays(self, painter):
        """
        Overlays will be created according to the 'overlays' parameter
        this is a list containing dicts of all overlays, which contains per overlay (dictionary)
        - the fill / brush of the tile type,
        - the pen / line details of the tile type and
        - a list of all the positions of the tile type

        ---------example----------------
            overlays = []

            overlay1brush = QtGui.QBrush(QtGui.QColor(0,255,0,150))
            overlay1pen = QtGui.QPen(QtGui.QColor(0,255,0))
            overlay1pen.setWidth(3)

            overlay1dict = {
                "Brush": overlay1brush,
                "Pen": overlay1pen,
                "Positions": [
                    [tile 1 x coordinate, tile 1 y coordinate], 
                    [tile 2 x coordinate, tile 2 y coordinate],
                    [1, 2],
                    [3, 7],
                    ],
                }

            overlays.append(overlay1dict)
        --------------------------------
        """

        # Create overlays
        for overlay in self.overlays:
            for tile in overlay["Positions"]:

                # create the hexagon at the specified location
                positionx, positiony, angle = self.get_hexagon_position(tile[0], tile[1], self.horizontal)
                hexagon = QHexagon(self.width, self.height, positionx, positiony, 6, 12, angle)

                # set the style of this overlay
                painter.setBrush(overlay["Brush"])
                painter.setPen(overlay["Pen"])

                # draw the shape
                painter.drawPolygon(hexagon)

    def get_hexagon_position(self, row, column, horizontal):
        """
        Method to easily determine the angle and position of a hexagon tile
        within a gameboard
        """

        # default is for horizontal aligned board, if not we have to switch rows and columns and set the angle accordingly
        if horizontal == False:
            # if row number is odd, offset the hexes nicely in between the columns of the previous
            positiony = column * 36 if (row % 2) == 0 else column * 36 + 18
            positionx = row * 10
            # set the angle of the hexagon
            angle = 90

        else:
            # if row number is odd, offset the hexes nicely in between the columns of the previous
            positionx = column * 36 if (row % 2) == 0 else column * 36 + 18
            positiony = row * 10
            # set the angle of the hexagon
            angle = 0
    	
        return positionx, positiony, angle

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

    The hexagon needs the width and height of the current widget or window 
    in order to place itself. 
    the position x and y denote the position relative to the current width and height
    """

    def __init__(self, width, height, positionx, positiony, sides, radius, angle):
        QtWidgets.QWidget.__init__(self)
        
        self.positionx = positionx
        self.positiony = positiony
        self.sides = sides
        self.radius = radius
        self.angle = angle

        # angle per step
        w = 360/self.sides

        # add the points of polygon per side
        for i in range(self.sides):
            t = w*i + self.angle

            # horizontal alignment
            x = self.positionx + self.radius*math.cos(math.radians(t))
            # vertical alignment
            y = self.positiony + self.radius*math.sin(math.radians(t))

            # add side to polygon
            self.append(QtCore.QPointF(width()/2 +x, height()/2 + y)) 



def test_create_overlay():
    """
    Example how to create overlay tiles.
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

    overlays = [allydict, enemydict]
    return overlays

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
    
    overlays = test_create_overlay()
    frame = QHexagonboard(horizontal = True, rows = 20, columns = 10, overlays = overlays)
    main.setCentralWidget(frame)

    main.showMaximized()
    
    sys.exit(app.exec_())

if __name__ == '__main__':

    # test_hexagon()
    test_board()
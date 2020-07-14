import sys, math

from PyQt5 import QtCore, QtGui, QtWidgets

class QHexagonboard(QtWidgets.QFrame):
    def __init__(self, rows, columns, overlays = [], horizontal = True, relative = True):
        QtWidgets.QFrame.__init__(self)

        # set board parameters
        self.rows = rows
        self.columns = columns
        self.overlays = overlays
        self.horizontal = horizontal
        self.relative = relative

        # default parameters
        self.scale = 10 # 100%
        self.setMinimumWidth(800) # start screenwidth
        self.setMinimumHeight(600) # start screenheight

        self.center = QtCore.QPointF(self.width()/2, self.height()/2)
        
    def wheelEvent(self, event):

        # get delta of mousewheel scroll, default is 120 pixels, we devide by 12 to return 10 that calculates easier
        delta = event.angleDelta()
        delta /= 120
        scale = self.scale + delta.y()
        self.scale = scale if scale > 0 else self.scale
        print(f"new scale is {self.scale}")

        # determine location of point to zoom in to / out from
        self.center = event.position()
        print(f"center = {self.center.x()} - {self.center.y()}")

        # update widget to trigger the paintEvent
        self.update()

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

        # draw the basis for the board
        self.paint_underlay(painter)

        # draw all the overlays on top of the basis
        self.paint_overlays(painter)

    def paint_underlay(self, painter):
        """
        The basis of the gameboard
        this method creates a hexagon for all the rows and columns
        """

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        painter.setBrush(brush)
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)

        # Create hexagons for all the rows and columns
        row = 0
        while row < self.rows:
            
            column = 0
            while column < self.columns:

                # create the hexagon at the specified location
                hexagon = self.create_hexagon(row, column)

                # draw the shape
                painter.drawPolygon(hexagon)

                column += 1
            row += 1

    def paint_overlays(self, painter):
        """
        Overlays will be created according to the 'overlays' parameter
        this is a list containing dicts of all overlays, which contains per overlay (dictionary)
        - the fill / brush of the tile type (Brush),
        - the pen / line details of the tile type (Pen) and
        - a list of all the positions of the tile type (Positions)
        """

        # Create overlays
        for overlay in self.overlays:
            for tile in overlay["Positions"]:

                # get position info from the tile list
                row = tile[0]
                column = tile[1]

                # create the hexagon at the specified location
                hexagon = self.create_hexagon(row, column)

                # set the style of this overlay
                painter.setBrush(overlay["Brush"])
                painter.setPen(overlay["Pen"])

                # draw the shape
                painter.drawPolygon(hexagon)

    def create_hexagon(self, row, column):
        """
        Method to easily determine the angle and position of a hexagon tile
        within a gameboard
        """
       
        # tile size
        radius = 2 * self.scale

        # space between tiles between columns and rows to make a snug fit
        column_default = (column * 6) * self.scale
        column_offset = column_default + (3 * self.scale)
        row_default = (row * 1.7) * self.scale

        # set screen adjustments
        if self.relative == True:
            # get relative position of board against center of screen
            offset_x = self.width() / 2 - ((self.columns / 1) * radius)
            offset_y = self.height() / 2 - ((self.rows / 2) * radius)

        else:
            # get absolute position of tiles against top and left of screen
            offset_x = 2 * self.scale
            offset_y = 2 * self.scale

        # default is for horizontal aligned board, if not we have to switch rows and columns and set the angle accordingly
        if self.horizontal == True:
            # if row number is odd, offset the hexes nicely in between the columns of the previous
            positionx = column_default + offset_x if (row % 2) == 0 else column_offset + offset_x
            positiony = row_default + offset_y
            # set the angle of the hexagon
            angle = 0

        # else:
        #     # if row number is odd, offset the hexes nicely in between the columns of the previous
        #     positiony = column_default + offset_x if (row % 2) == 0 else column_offset + offset_x
        #     positionx = row_default + offset_y

        #     # set the angle of the hexagon
        #     angle = 90

        hexagon = QHexagon(positionx, positiony, 6, radius, angle)

        return hexagon

class QHexagonFrame(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

    def paintEvent(self, event):
        # create the hexagon at the specified location
        hexagon = QHexagon(20, 20, 6, 120, 0)

        # prepare draw, painter is default white background surrounded by a black 1 width line
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        painter.setBrush(brush)
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.Solidline)
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

    def __init__(self, positionx, positiony, sides, radius, angle):
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
            self.append(QtCore.QPointF(x, y)) 


    @QtCore.pyqtSlot()
    def zoom_in(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self, self.factor)

        tr = self.view.transform() * scale_tr
        self.view.setTransform(tr)

    @QtCore.pyqtSlot()
    def zoom_out(self):
        scale_tr = QtGui.QTransform()
        scale_tr.scale(self.factor, self.factor)

        scale_inverted, invertible = scale_tr.inverted()

        if invertible:
            tr = self._view.transform() * scale_inverted
            self.view.setTransform(tr)

def test_single_hexagon():

    app()
    frame = QHexagonFrame()
    main(frame)

def test_empty_board():
    
    app()
    frame = QHexagonboard(rows = 21, columns = 11, horizontal=False)
    main(frame)

def test_overlay_board():

    app()
    overlays = test_create_overlay()
    frame = QHexagonboard(rows = 20, columns = 10, overlays = overlays)
    main(frame)

def test_create_overlay():
    """
    Example how to create overlay tiles.
    List of enemies in red and list of allies in green

    Its created by creating a dictionary of 3 values, a brush value, a pen value
    and a list of positions where it applies
    """

    overlays = []

    blockbrush = QtGui.QBrush(QtGui.QColor(0,0,0,255))
    blockpen = QtGui.QPen(QtGui.QColor(0,0,0), 3, QtCore.Qt.NoPen)
    blockdict = {
        "Brush": blockbrush,
        "Pen": blockpen,
        "Positions": [
            [2, 6],
            [3, 6],
            [3, 5],
            [4, 6],
        ],
    }
    overlays.append(blockdict)

    allybrush = QtGui.QBrush(QtGui.QColor(0,255,0,100))
    allypen = QtGui.QPen(QtGui.QColor(0,255,0), 0, QtCore.Qt.NoPen)
    allydict = {
        "Brush": allybrush,
        "Pen": allypen,
        "Positions": [
            [1, 3], 
            [4, 3],
        ],
    }
    overlays.append(allydict)

    enemybrush = QtGui.QBrush(QtGui.QColor(255,0,0,100))
    enemypen = QtGui.QPen(QtGui.QColor(255,0,0), 0, QtCore.Qt.NoPen)
    enemydict = {
        "Brush": enemybrush,
        "Pen": enemypen,
        "Positions": [
            [2, 3],
            [5, 6],
        ],
    }
    overlays.append(enemydict)

    coverbrush = QtGui.QBrush(QtGui.QColor(255,255,255,0))
    coverpen = QtGui.QPen(QtGui.QColor(0,0,0), 3, QtCore.Qt.DashLine)
    coverdict = {
        "Brush": coverbrush,
        "Pen": coverpen,
        "Positions": [
            [2, 2],
            [3, 2],
            [4, 3],
        ],
    }
    overlays.append(coverdict)

    return overlays

def app():

    global app
    app = QtWidgets.QApplication(sys.argv)

def main(frame):

    global main
    main = QtWidgets.QMainWindow()
    main.setCentralWidget(frame)
    # main.show()
    main.showMaximized()
    
    sys.exit(app.exec_())


if __name__ == '__main__':

    # test_single_hexagon()
    # test_empty_board()
    test_overlay_board()
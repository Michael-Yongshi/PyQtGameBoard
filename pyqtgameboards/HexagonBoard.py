import sys, math
import collections

from PyQt5 import QtCore, QtGui, QtWidgets

class QHexagonboard(QtWidgets.QGraphicsView):
    def __init__(self, rows, columns, overlays = [], horizontal = True, relative = True):
        QtWidgets.QGraphicsView.__init__(self)

        # set board parameters
        self.rows = rows
        self.columns = columns
        self.overlays = overlays
        self.horizontal = horizontal
        self.relative = relative

        # default parameters
        self.deltaF = 1.0

        self.scalemanual = 10 # 100%
        self.center = None
        self.shiftfocus = QtCore.QPointF(0, 0)

        self.tiles = {}
        self.selected_overlay = {}

        # build board and set to this widget
        self.scene = QtWidgets.QGraphicsScene()
        self.build_board_scene()
        self.setScene(self.scene)

    def mousePressEvent(self, event):

        selectbrush = QtGui.QBrush(QtGui.QColor(0,0,255,255))
        selectpen = QtGui.QPen(QtGui.QColor(0,0,0), 3, QtCore.Qt.NoPen)
        selectpainter = QtGui.QPainter()
        selectpainter.setPen(selectpen)
        selectpainter.setBrush(selectbrush)

        position = self.mapToScene(event.pos())
        selected_tile = self.scene.itemAt(position, QtGui.QTransform())
        for tile in self.tiles:
            if tile == selected_tile:
                print(self.tiles[tile])
                selected_tile.setBrush(selectbrush)
                selected_tile.update()
                break


    def wheelEvent(self, event):

        # get delta of mousewheel scroll, default is 120 pixels, we devide by 1200 to return 0.10 to get the zoom factor
        delta = event.angleDelta()
        self.deltaF = 1 + float(delta.y() / 1200)
        self.scale(self.deltaF, self.deltaF)

    def build_board_scene(self):
        """       
        Creates a gameboard of rows and columns of hexagons of a sepecific
        size. 

        the default board consists of a number of hexagons that touch at the horizontal tip. 
        The offset hexagons in between them, offset above and below, are in
        a different row. This means that 4 columns already look like a board
        with 8 columns as the offset hexes are not counted for the same row.
        """

        # set focus to center of screen
        self.center = QtCore.QPointF(self.geometry().width() / 2, self.geometry().height() / 2)

        # draw the basis for the board
        self.build_underlay()
        self.build_overlays()

    def build_underlay(self):
        """
        The basis of the gameboard
        this method creates a hexagon for all the rows and columns
        """

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.SolidLine)
        
        # Create hexagons for all the rows and columns
        row = 0
        while row < self.rows:
            
            column = 0
            while column < self.columns:
                
                # create the hexagon at the specified location
                hexagon_shape = self.create_hexagon_shape(row, column)
                tile = self.scene.addPolygon(hexagon_shape, pen, brush)
                self.tiles[tile] = [row, column]

                column += 1
            row += 1

    def build_overlays(self):
        """
        Overlays will be created according to the 'overlays' parameter
        this is a list containing dicts of all overlays, which contains per overlay (dictionary)
        - the fill / brush of the tile type (Brush),
        - the pen / line details of the tile type (Pen) and
        - a list of all the positions of the tile type (Positions)
        """

        # Create overlays
        overlays = self.overlays + self.selected_overlay if self.selected_overlay != {} else self.overlays

        for overlay in overlays:
            for tile in overlay["Positions"]:

                # get position info from the tile list
                row = tile[0]
                column = tile[1]

                # create the hexagon at the specified location
                hexagon_shape = self.create_hexagon_shape(row, column)
                tile = self.scene.addPolygon(hexagon_shape, overlay["Pen"], overlay["Brush"])

    def create_hexagon_shape(self, row, column):
        """
        Method to easily determine the angle and position of a hexagon tile
        within a gameboard
        """
       
        # tile size
        radius = 2 * self.scalemanual

        if self.horizontal == True:
            # set the angle of the hexagon
            angle = 0
        
            # space between tiles in columns and rows to make a snug fit
            column_default = 6 * self.scalemanual
            column_offset = column_default / 2

            column_distance_even = column * column_default
            column_distance_odd = column * column_default + column_offset

            row_default = 1.7 * self.scalemanual
            row_distance = row * row_default

            # set screen adjustments
            if self.relative == True:
                # get relative position of tile against center of screen
                # print(f"center = {self.center}")

                screen_offset_x = self.center.x() - ((self.columns / 2) * column_default) + self.shiftfocus.x()
                screen_offset_y = self.center.y() - ((self.rows / 2) * row_default) + self.shiftfocus.y()
                # print(f"offset x = {screen_offset_x}")
                # print(f"offset y = {screen_offset_y}")

            else:
                # get absolute position of tiles against top and left of screen
                screen_offset_x = 2 * self.scalemanual
                screen_offset_y = 2 * self.scalemanual

            # if row number is odd, offset the hexes nicely in between the columns of the previous
            x = column_distance_even + screen_offset_x if (row % 2) == 0 else column_distance_odd + screen_offset_x
            y = row_distance + screen_offset_y


        elif self.horizontal == False:
            """Needs a lot more work"""
            # set the angle of the hexagon
            angle = 90

            # space between tiles in columns and rows to make a snug fit
            column_default = 3 * self.scalemanual
            column_distance = column * column_default

            row_default = 2.5 * self.scalemanual
            row_offset = 1.5 * self.scalemanual
            row_distance_even = row * row_default
            row_distance_odd = row * row_default + row_offset

            # set screen adjustments
            if self.relative == True:
                # get relative position of tile against center of screen
                # print(f"center = {self.center}")
                
                screen_offset_x = self.center.x() - ((self.columns / 2) * (2 * self.scalemanual))
                screen_offset_y = self.center.y() - ((self.rows / 2) * (2 * self.scalemanual))
                # print(f"offset x = {screen_offset_x}")
                # print(f"offset y = {screen_offset_y}")

            else:
                # get absolute position of tiles against top and left of screen
                screen_offset_x = 2 * self.scalemanual
                screen_offset_y = 2 * self.scalemanual

            # if row number is odd, offset the hexes nicely in between the columns of the previous
            x = column_distance + screen_offset_x
            y = row_distance_even + screen_offset_y if (column % 2) == 0 else row_distance_odd + screen_offset_x

        hexagon_shape = QHexagonShape(x, y, radius, angle)

        return hexagon_shape

class QHexagonShape(QtGui.QPolygonF):
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

    def __init__(self, x, y, radius, angle):
        QtWidgets.QWidget.__init__(self)
        
        self.x = x
        self.y = y
        self.sides = 6
        self.radius = radius
        self.angle = angle

        # angle per step
        w = 360/self.sides

        # add the points of polygon per side
        for i in range(self.sides):
            t = w*i + self.angle

            # horizontal alignment
            x = self.x + self.radius*math.cos(math.radians(t))
            # vertical alignment
            y = self.y + self.radius*math.sin(math.radians(t))

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

class QHexagonTile(QtWidgets.QGraphicsPolygonItem):

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

    def __init__(self, x, y, sides, radius, angle):
        QtWidgets.QGraphicsPolygonItem.__init__(self)
        
        self.x = x
        self.y = y
        self.sides = sides
        self.radius = radius
        self.angle = angle

        # angle per step
        w = 360/self.sides

        # add the points of polygon per side
        for i in range(self.sides):
            t = w*i + self.angle

            # horizontal alignment
            x = self.x + self.radius*math.cos(math.radians(t))
            # vertical alignment
            y = self.y + self.radius*math.sin(math.radians(t))

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

def test_empty_board():
    
    app()
    frame = QHexagonboard(rows = 21, columns = 11, horizontal=True)
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
        "Name": "block",
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
        "Name": "ally",
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
        
        "Name": "enemy",
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
        "Name": "cover",
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
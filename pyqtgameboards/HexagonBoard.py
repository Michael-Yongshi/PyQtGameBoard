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

        self.map_coordinates_by_tile = {}
        self.map_tile_by_coordinates = {}
        self.selected_tile = None

        # build board and set to this widget
        self.scene = QtWidgets.QGraphicsScene()
        self.build_board_scene()
        self.setScene(self.scene)

    def mousePressEvent(self, event):

        # remove selection of current selected tile
        if self.selected_tile != None:  
            
            # repaint selected tile and adjacent tiles to default
            defaultbrush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
            adjacent_tiles = self.get_adjacent_tiles(self.selected_tile)
            tiles = adjacent_tiles + [self.selected_tile]
            self.paint_graphic_items(tiles, brush = defaultbrush)

            # remove selection
            self.selected_tile = None

        # get position (of pixel clicked)
        position = self.mapToScene(event.pos())
        # print(f"tile selected at position {position}")

        # associated tile graphic_item
        self.selected_tile = self.scene.itemAt(position, QtGui.QTransform())
        if self.selected_tile == None:
            return
            
        # coordinates of this tile
        # coordinates = self.get_tile_grid_location(self.selected_tile)
        # print(f"tile selected at coordinates {coordinates}")

        # paint the new tile
        selectbrush = QtGui.QBrush(QtGui.QColor(0,0,255,255))
        self.paint_graphic_items([self.selected_tile], brush = selectbrush)

        # paint adjacent tiles
        adjacent_brush = QtGui.QBrush(QtGui.QColor(0,0,255,100))
        adjacent_tiles = self.get_adjacent_tiles(self.selected_tile)
        self.paint_graphic_items(adjacent_tiles, brush = adjacent_brush)

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

        Overlays will be created according to the 'overlays' parameter
        this is a list containing dicts of all overlays, which contains per overlay (dictionary)
        - the fill / brush of the tile type (Brush),
        - the pen / line details of the tile type (Pen) and
        - a list of all the positions of the tile type (Positions)       
        """

        # set focus to center of screen
        self.center = QtCore.QPointF(self.geometry().width() / 2, self.geometry().height() / 2)

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.SolidLine)
        
        # Create hexagons for all the rows and columns
        row = 1
        while row <= self.rows:

            column = 1
            while column <= self.columns:

                # create the hexagon at the specified location
                hexagon_shape = self.create_hexagon_shape(row, column)

                # Create the background tile
                tile = self.scene.addPolygon(hexagon_shape, pen, brush)
                self.map_coordinates_by_tile[tile] = [row, column]
                self.map_tile_by_coordinates[f"{row}-{column}"] = tile

                column += 1
            row += 1

        # Create overlays
        for overlay in self.overlays:
            
            # Get brush
            if overlay["Brush"] != "":
                brush = overlay["Brush"]
            else:
                brush = None

            # Get pen
            if overlay["Pen"] != "":
                pen = overlay["Pen"]
            else:
                pen = None

            # create tile list to paint for this overlay
            overlay_tiles = []
            
            for overlay_coordinates in overlay["Positions"]:

                # get position info from the tile list
                overlay_coordinates_string = f"{overlay_coordinates[0]}-{overlay_coordinates[1]}"

                # get the respective tile
                tile = self.map_tile_by_coordinates[overlay_coordinates_string]
                
                # move the tile on top of the background tiles
                tile.setZValue(1)
                
                # add to the overlay tiles
                overlay_tiles.append(tile)

            # paint all the respective tiles
            self.paint_graphic_items(overlay_tiles, pen, brush)

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

    def get_tile_grid_location(self, target_tile):
        for tile in self.map_coordinates_by_tile:
            if tile == target_tile:
                coordinates = self.map_coordinates_by_tile[tile]
                return coordinates

    def get_adjacent_tiles(self, target_tile):
        adjacent_tiles = []
        coordinates = self.get_tile_grid_location(target_tile)

        # adjacent coordinates
        if coordinates[0] % 2 == 0:
            adjacent_offset = [
                [-2,0], # top
                [-1,-1], # topleft
                [1,-1], # leftdown
                [2,0], # down
                [1,0], # rightdown
                [-1,0], # rightup
            ]
        else:
            adjacent_offset = [
                [-2,0], # top
                [-1,0], # topleft
                [1,0], # leftdown
                [2,0], # down
                [1,1], # rightdown
                [-1,1], # rightup
            ]

        for offset in adjacent_offset:
            adjacent_coordinate = [coordinates[0] + offset[0], coordinates[1] + offset[1]]
            # print(adjacent_coordinate)

            if adjacent_coordinate[0] >= 1 and adjacent_coordinate[1] >= 1:
                tile = self.map_tile_by_coordinates[f"{adjacent_coordinate[0]}-{adjacent_coordinate[1]}"]
                adjacent_tiles.append(tile)
        
        return adjacent_tiles

    def paint_graphic_items(self, graphic_items, pen = None, brush = None):

        for graphic_item in graphic_items:
            self.paint_graphic_item(graphic_item, pen, brush)

    def paint_graphic_item(self, graphic_item, pen = None, brush = None):
        if pen != None:
            graphic_item.setPen(pen)
        
        if brush != None:
            graphic_item.setBrush(brush)
        
        graphic_item.update()

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
    blockdict = {
        "Name": "block",
        "Brush": blockbrush,
        "Pen": "",
        "Positions": [
            [2, 6],
            [3, 6],
            [3, 5],
            [4, 6],
        ],
    }
    overlays.append(blockdict)

    coverpen = QtGui.QPen(QtGui.QColor(0,0,0), 3, QtCore.Qt.DashLine)
    coverdict = {
        "Name": "cover",
        "Brush": "",
        "Pen": coverpen,
        "Positions": [
            [2, 2],
            [3, 2],
            [4, 3],
        ],
    }
    overlays.append(coverdict)

    allybrush = QtGui.QBrush(QtGui.QColor(0,255,0,100))
    allydict = {
        "Name": "ally",
        "Brush": allybrush,
        "Pen": "",
        "Positions": [
            [1, 3], 
            [4, 3],
        ],
    }
    overlays.append(allydict)

    enemybrush = QtGui.QBrush(QtGui.QColor(255,0,0,100))
    enemydict = {
        "Name": "enemy",
        "Brush": enemybrush,
        "Pen": "",
        "Positions": [
            [2, 3],
            [5, 6],
        ],
    }
    overlays.append(enemydict)

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
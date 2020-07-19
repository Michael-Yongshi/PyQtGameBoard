import sys, math
import collections

from PyQt5 import QtCore, QtGui, QtWidgets


class QGameboard(QtWidgets.QGraphicsView):
    def __init__(self, rows, columns, size = 4, overlays = [], horizontal = True, relative = True):
        QtWidgets.QGraphicsView.__init__(self)

        # set board parameters
        self.rows = rows
        self.columns = columns
        self.size = size
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

        # build board and set to this widget
        self.scene = QtWidgets.QGraphicsScene()
        self.build_board_scene()
        self.setScene(self.scene)

        # selections and stuff
        self.selected_tile = None
        self.adjacent_tiles = None
        self.target_tile = None
        self.line_of_sight = None
        self.colliding_items = None

    def mousePressEvent(self, event):

        # store current selected tile
        current_selected_tile = self.selected_tile

        # get position (of pixel clicked)
        position = self.mapToScene(event.pos())
        # print(f"tile selected at position {position}")

        # associated tile graphic_item
        new_selected_tile = self.scene.itemAt(position, QtGui.QTransform())

        # if clicked outside of map, remove selection of current selected tile
        if new_selected_tile == None and current_selected_tile != None:
                
            self.selection_removal(current_selected_tile)

            if self.target_tile != None:
                self.target_removal()

        elif new_selected_tile != None and current_selected_tile == None:

            self.selection_new(new_selected_tile)
            self.selection_adjacent_tiles()

        elif new_selected_tile != None and current_selected_tile != None:
            if self.target_tile != None:
                self.target_switch(new_selected_tile)

            elif self.target_tile == None:
                self.target_new(new_selected_tile)

            self.selection_adjacent_tiles()

    def selection_removal(self, current_selected_tile):
        """
        Sets and paints a new selection when there is none yet.
        """

        # check if there is a target tile to wipe
        tiles = [current_selected_tile]

        # add the adjacent tiles
        tiles += self.get_adjacent_tiles(current_selected_tile)

        # remove selection
        self.selected_tile = None

        # rebuild the tiles
        self.rebuild_tiles(tiles)

    def selection_new(self, new_selected_tile):
            
        # paint the new tile
        selectbrush = QtGui.QBrush(QtGui.QColor(0,0,255,255))
        self.paint_graphic_items([new_selected_tile], brush = selectbrush)

        # make new tile the selected tile
        self.selected_tile = new_selected_tile

        # paint adjacent tiles

    def selection_adjacent_tiles(self):

        # get adjacent tiles
        adjacent_tiles = self.get_adjacent_tiles(self.selected_tile)

        # paint adjacent tiles
        adjacent_brush = QtGui.QBrush(QtGui.QColor(0,0,255,100))
        self.paint_graphic_items(adjacent_tiles, brush = adjacent_brush)

        return adjacent_tiles

    def target_removal(self):

        # reset target tile
        tiles_to_reset = [self.target_tile]
        self.target_tile = None
        
        # remove any line of sight
        if self.line_of_sight != None:
            self.scene.removeItem(self.line_of_sight)
            self.line_of_sight = None

        # remove any colliding items
        if self.colliding_items != None:
            tiles_to_reset += self.colliding_items
        
        # repaint tiles
        self.rebuild_tiles(tiles_to_reset)

    def target_new(self, new_selected_tile):

        # set the new tile as the target tile and paint it accordingly
        self.target_tile = new_selected_tile
        target_brush = QtGui.QBrush(QtGui.QColor(255,255,0,100))
        self.paint_graphic_item(new_selected_tile, brush = target_brush)

        # Create a new line of sight between the selected tile and the target tile
        self.colliding_items = self.create_line_of_sight(
            originobject=self.selected_tile,
            targetobject=self.target_tile,
            )

        # paint the colliding items that the line of sight goes through
        collide_brush = QtGui.QBrush(QtGui.QColor(50,50,50,100))
        self.paint_graphic_items(self.colliding_items, brush = collide_brush)

    def target_switch(self, new_selected_tile):
        
        self.target_removal()
        self.target_new(new_selected_tile)

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

        self.build_tiles()
        self.build_overlays()

    def build_tiles(self):

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.SolidLine)
        
        # Create hexagons for all the rows and columns
        row = 1
        while row <= self.rows:

            column = 1
            while column <= self.columns:

                """
                maybe add following to seperate method, so this method can be shape agnostic
                """

                tile = self.add_shape_to_scene(row, column, pen, brush)

                self.map_coordinates_by_tile[tile] = [row, column]
                self.map_tile_by_coordinates[f"{row}-{column}"] = tile

                column += 1
            row += 1

    def build_overlays(self):

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

    def rebuild_tiles(self, tiles):

        for tile in tiles:
            self.rebuild_tile(tile)

    def rebuild_tile(self, tile):

        tile_coordinates = self.map_coordinates_by_tile[tile]

        #  default white background surrounded by a black 1 width line
        brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.SolidLine)
        
        # repaint the tile
        self.paint_graphic_item(tile, pen, brush)

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
          
            for overlay_coordinates in overlay["Positions"]:
                if overlay_coordinates == tile_coordinates:
                                
                    # repaint the tile
                    self.paint_graphic_item(tile, pen, brush)
                    
                    break

    def get_tiles_grid_location(self, tiles):

        coordinate_list = []
        for tile in tiles:
            coordinates = self.get_tile_grid_location(tile)
            coordinate_list.append(coordinates)

        return coordinate_list

    def get_tile_grid_location(self, tile):
        for graphics_item in self.map_coordinates_by_tile:
            if graphics_item == tile:
                coordinates = self.map_coordinates_by_tile[tile]
                return coordinates

    def paint_graphic_items(self, graphic_items, pen = None, brush = None):

        for graphic_item in graphic_items:
            self.paint_graphic_item(graphic_item, pen, brush)

    def paint_graphic_item(self, graphic_item, pen = None, brush = None):
        if pen != None:
            graphic_item.setPen(pen)
        
        if brush != None:
            graphic_item.setBrush(brush)
        
        graphic_item.update()

    def create_line_of_sight(self, originobject, targetobject):

        origin_center_x = originobject.boundingRect().center().x()
        origin_center_y = originobject.boundingRect().center().y()
        target_center_x = targetobject.boundingRect().center().x()
        target_center_y = targetobject.boundingRect().center().y()

        pen = QtGui.QPen(QtGui.QColor(0,0,0), 1, QtCore.Qt.NoPen)

        self.line_of_sight = self.scene.addLine(
            origin_center_x,
            origin_center_y,
            target_center_x,
            target_center_y,
            pen,
            )
        
        # find all the tiles that are collided with the line of sight
        colliding_items = (self.scene.collidingItems(self.line_of_sight))

        # delete selected and target tile from list
        index_selected = colliding_items.index(self.selected_tile)
        colliding_items.pop(index_selected)
        index_target = colliding_items.index(self.target_tile)
        colliding_items.pop(index_target)

        # get an array of the coordinates in order to print
        coordinate_list = self.get_tiles_grid_location(colliding_items)
        # print(coordinate_list)

        return colliding_items

    def get_adjacent_tiles(self, target_tile):

        """
        Needs overwrite to implement kind of shape
        """

        return NotImplemented

    def add_shape_to_scene(self, row, column, pen, brush):

        """
        Needs overwrite to implement kind of shape
        """

        return NotImplemented

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
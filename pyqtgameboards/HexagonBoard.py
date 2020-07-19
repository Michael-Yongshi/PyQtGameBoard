import math

from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import QPointF

from gameboard import QGameboard, test_create_overlay, app, main

class QHexagonboard(QGameboard):
    def __init__(self, rows, columns, size = 4, overlays = [], horizontal = True, relative = True):
        super().__init__(rows, columns, size, overlays, horizontal, relative)

    def add_shape_to_scene(self, row, column, pen, brush):

        # create the hexagon at the specified location
        hexagon_shape = self.create_hexagon_shape(row, column)

        # Create the background tile
        tile = self.scene.addPolygon(hexagon_shape, pen, brush)
        return tile

    def create_hexagon_shape(self, row, column):
        """
        Method to easily determine the angle and position of a hexagon tile
        within a gameboard
        """
       
        # tile size
        radius = (self.size / 2) * self.scalemanual

        if self.horizontal == True:
            # set the angle of the hexagon
            angle = 0
        
            # space between tiles in columns and rows to make a snug fit
            column_default = (self.size * 1.5) * self.scalemanual
            column_offset = column_default / 2

            column_distance_even = column * column_default
            column_distance_odd = column * column_default + column_offset

            row_default = (self.size / 2.353) * self.scalemanual
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

            try:
                tile = self.map_tile_by_coordinates[f"{adjacent_coordinate[0]}-{adjacent_coordinate[1]}"]
                adjacent_tiles.append(tile)
            except:
                pass
        
        return adjacent_tiles
        
class QHexagonShape(QPolygonF):
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
        QPolygonF.__init__(self)
        
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
            self.append(QPointF(x, y)) 

def test_hexagon_board():

    app()
    overlays = test_create_overlay()
    frame = QHexagonboard(rows = 20, columns = 10, size = 6, overlays = overlays)
    main(frame)
    
if __name__ == '__main__':

    test_hexagon_board()
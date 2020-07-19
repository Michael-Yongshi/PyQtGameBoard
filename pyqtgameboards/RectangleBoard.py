from PyQt5.QtCore import QRectF
from gameboard import QGameboard, test_create_overlay, app, main

class QRectangleboard(QGameboard):
    def __init__(self, rows, columns, size = 4, overlays = [], horizontal = True, relative = True):
        super().__init__(rows, columns, size, overlays, horizontal, relative)

    def add_shape_to_scene(self, row, column, pen, brush):

        # create the rectangle at the specified location
        rectangle_shape = self.create_rectangle_shape(row, column)

        # Create the background tile
        tile = self.scene.addRect(rectangle_shape, pen, brush)
        return tile

    def create_rectangle_shape(self, row, column):
        """
        Method to easily determine the position of a rectangle tile
        within a gameboard
        """

        # tile size (only perfect squares for now)
        height = self.size * self.scalemanual
        width = self.size * self.scalemanual

    
        # space between tiles in columns and rows to make a snug fit
        column_default = self.size * self.scalemanual
        column_distance = column * column_default

        row_default = self.size * self.scalemanual
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


        x = column_distance + screen_offset_x
        y = row_distance + screen_offset_y

        # We can use the default QRectF object to create a perfectly fine square
        rectangle_shape = QRectF(x, y, width, height)

        return rectangle_shape

    def get_adjacent_tiles(self, target_tile):
        adjacent_tiles = []
        coordinates = self.get_tile_grid_location(target_tile)

        # adjacent coordinates
        adjacent_offset = [
            [1,0], # top
            [0,-1], # left
            [-1,0], # down
            [0,1], # right
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
        
def test_rectangle_board():

    app()
    overlays = test_create_overlay()
    frame = QRectangleboard(rows = 5, columns = 6, size = 6, overlays = overlays)
    main(frame)


if __name__ == '__main__':

    test_rectangle_board()
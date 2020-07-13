import sys, math

from PyQt5 import QtCore, QtGui, QtWidgets
from guidarktheme import widget_template

class QHexagonboard(QtWidgets.QWidget):
    def __init__(self, horizontal, rows, columns):
        QtWidgets.QWidget.__init__(self)

        # set lineColor
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))
        # set lineWidth
        self.pen.setWidth(1)
        # set fillColor
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))

        # set hexagon parameters
        self.horizontal = horizontal
        self.rows = rows
        self.columns = columns

        # build board array
        self.board = []
        self.buildboard()

        # widget is painted once initialized by the paintevent function

    def buildboard(self):
        """
        Creates a gameboard of rows and columns of hexagons of a sepecific
        size. 
        A row consists of a number of hexagons that touch at the horizontal tip. 
        The offset hexagons in between them, offset above and below, are in
        a different row. This means that 4 columns already look like a board
        with 8 columns as the offset hexes are not counted for the same row.
        """

        row = 0
        while row < self.rows:
            col = 0
            while col < self.columns:
                # default is for horizontal aligned board
                if self.horizontal == False:
                    # if row number is odd, offset the hexes nicely in between the columns of the previous
                    positiony = col * 36 if (row % 2) == 0 else col * 36 + 18
                    positionx = row * 10
                    # set the angle of the hexagon
                    alignment = 90
                else:
                    # if row number is odd, offset the hexes nicely in between the columns of the previous
                    positionx = col * 36 if (row % 2) == 0 else col * 36 + 18
                    positiony = row * 10
                    # set the angle of the hexagon
                    alignment = 0

                # create the hexagon and add to the specified position on the board
                hexagon = self.createPoly(positionx, positiony, 6, 12, alignment)
                self.board.append(hexagon)
                
                col += 1
            row += 1
            
    def createPoly(self, positionx, positiony, sides, radius, angle):
        """
        polygon with number of sides, a radius, angle of the first point
        hexagon is made with 6 sides
        radius denotes the size of the shape, 
        angle of 
        0 makes a horizontal aligned hexagon (first point points flat), 
        90 makes a vertical aligned hexagon (first point points upwards)
        """

        polygon = QtGui.QPolygonF()
        w = 360/sides                                                   # angle per step
        for i in range(sides):                                          # add the points of polygon
            t = w*i + angle
            x = positionx + radius*math.cos(math.radians(t))                        # horizontal alignment
            y = positiony + radius*math.sin(math.radians(t))                        # vertical alignment
            polygon.append(QtCore.QPointF(self.width()/2 +x, self.height()/2 + y))  

        return polygon

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        for hexagon in self.board:
            painter.drawPolygon(hexagon)


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
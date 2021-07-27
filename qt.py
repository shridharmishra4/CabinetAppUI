from PyQt5 import QtCore, QtGui, QtWidgets 
import sys

class imageSelector(QtWidgets.QWidget):

    def __init__(self):
        super(imageSelector,self).__init__()
        self.initIS()

    def initIS(self):
        self.pixmap = self.createPixmap()

        painter = QtGui.QPainter(self.pixmap)
        pen = QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.SolidLine)
        painter.setPen(pen)

        width = self.pixmap.width()
        height = self.pixmap.height()

        numLines = 3
        numHorizontal = width//numLines
        numVertical = height//numLines
        # painter.drawRect(0,0,height,width)

        for x in range(numLines):
            newH = x * numHorizontal
            newV = x * numVertical
            print(0+newH,0,0+newH,height)
            painter.drawLine(0+newH,0,0+newH,height)
            # painter.drawLine(0+newH,0,0+newH,height)
            painter.drawLine(0,0+newV,width,0+newV)

        # label = QtGui.QLabel()
        label = QtWidgets.QLabel()

        label.setPixmap(self.pixmap)
        label.resize(label.sizeHint())

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(label)

        self.setLayout(hbox)
        self.show()          

    def createPixmap(self):
        pixmap = QtGui.QPixmap("door.jpg").scaledToHeight(500)
        return pixmap

def main():
    app = QtWidgets.QApplication(sys.argv)
    Im = imageSelector()
    sys.exit(app.exec_())

if __name__== '__main__':
    main()
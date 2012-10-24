import os, sys
from PyQt4 import QtCore, QtGui

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__inin__(self)
        self.setGeometry(0, 0, 340, 460)
        self.setWindowTitle('TODO')


def main():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

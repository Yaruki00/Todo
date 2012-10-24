import os, sys
from PyQt4 import QtCore, QtGui

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__inin__(self)
        # x, y, width, height
        self.setGeometry(0, 0, 340, 460)
        self.setWindowTitle('TODO')
        
    def closeEvent(self, event):
        # widget, title, message, button1 | button2, default focus
        reply = QtGui.QMessageBox.question(self,
                                           'Confirmation',
                                           "Are you sure to quit?",
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

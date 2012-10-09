import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

def createWindow(posX, posY, lenX, lenY, title):
    w = QtGui.QWidget()
    w.setGeometry(posX, posY, lenX, lenY)
    w.setWindowTitle(title)
    return w

def main():
    app = QtGui.QApplication(sys.argv)
    w = createWindow(300, 300, 250, 150, 'simple')
#    w = QtGui.QWidget()
#    w.resize(250, 150)
#    w.setWindowTitle('simple')
    w.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

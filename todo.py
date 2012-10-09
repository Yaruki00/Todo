import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    w.resize(250, 150)
    w.setWindowTitle('simple')
    w.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

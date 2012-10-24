import os, sys
from PyQt4 import QtCore, QtGui

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # x, y, width, height
        self.setGeometry(0, 0, 340, 460)
        self.setWindowTitle('TODO')
        # tree view
        self.treeView = QtGui.QTreeView()
        self.stdItemModel = QtGui.QStandardItemModel(0, 3)
        self.stdItemModel.setHeaderData(0, QtCore.Qt.Horizontal, 'Task')
        self.stdItemModel.setHeaderData(1, QtCore.Qt.Horizontal, 'Data')
        self.stdItemModel.setHeaderData(2, QtCore.Qt.Horizontal, 'Tags')
        self.treeView.setModel(self.stdItemModel)
        # layout and central widget
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.treeView)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(hbox)
        self.setCentralWidget(self.widget)

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

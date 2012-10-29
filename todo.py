import os, sys
from PyQt4 import QtCore, QtGui
import todoDB

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # x, y, width, height
        self.setGeometry(0, 0, 1060, 690)
        self.setWindowTitle('TODO')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # tree widget
        self.treeWidget = QtGui.QTreeWidget()
        headerItem = QtGui.QTreeWidgetItem(['Task', 'Date', 'Tags'])
        self.treeWidget.setHeaderItem(headerItem)
        self.treeWidget.setAllColumnsShowFocus(True)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setRootIsDecorated(False)
        # layout and central widget
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.treeWidget)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(hbox)
        self.setCentralWidget(self.widget)
        # status bar
        self.statusBar().showMessage('ready')
        # action
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        # menu bar
        menubar = self.menuBar()
        menubar.addMenu('&File')
        menubar.addMenu('&Edit')
        # tool bar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        # load data from DB and add in tree widget
        for task in todoDB.Task.query.all():
            tags = ','.join([t.name for t in task.tags])
            item = QtGui.QTreeWidgetItem([task.text, str(task.date), tags])
            item.task = task
            if task.done:
                item.setCheckState(0, QtCore.Qt.Checked)
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)
            self.treeWidget.addTopLevelItem(item)
        self.treeWidget.itemChanged.connect(self.on_treeWidget_itemChanged)
        for column in range(0, self.treeWidget.columnCount()):
            self.treeWidget.resizeColumnToContents(column)

    def on_treeWidget_itemChanged(self, item, column):
        if item.checkState(0):
            item.task.done = True
        else:
            item.task.done = False
        todoDB.saveData()

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
    todoDB.initDB()
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

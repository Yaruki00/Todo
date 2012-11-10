import os, sys
from PyQt4 import QtCore, QtGui
import todoDB, editor

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
        #expandItems
        self.expandItems = []
        # splitter
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.treeWidget)
        self.editor = editor.Editor(self)
        self.splitter.addWidget(self.editor)
        # layout and central widget
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.splitter)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(hbox)
        self.setCentralWidget(self.widget)
        # status bar
        self.statusBar().showMessage('ready')
        # exit action
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        # new action
        self.newAction = QtGui.QAction(QtGui.QIcon('new.png'), 'New', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('Add new task')
        self.newAction.triggered.connect(self.new)
        # edit action
        self.editAction = QtGui.QAction(QtGui.QIcon('edit.png'), 'Edit', self)
        self.editAction.setShortcut('Ctrl+E')
        self.editAction.setStatusTip('Edit selected task')
        self.editAction.triggered.connect(self.edit)
        # delete action
        self.deleteAction = QtGui.QAction(QtGui.QIcon('delete.png'), 'Delete', self)
        self.deleteAction.setShortcut('Ctrl+D')
        self.deleteAction.setStatusTip('Delete selected task')
        self.deleteAction.triggered.connect(self.delete)
        # menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.newAction)
        editMenu.addAction(self.editAction)
        editMenu.addAction(self.deleteAction)
        # tool bar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(self.newAction)
        toolbar.addAction(self.editAction)
        toolbar.addAction(self.deleteAction)
        # load data from DB and add in tree widget
        self.loadData()
        # connect
        self.treeWidget.itemChanged.connect(self.on_treeWidget_itemChanged)
        self.treeWidget.currentItemChanged.connect(self.on_treeWidget_currentItemChanged)
        self.treeWidget.itemExpanded.connect(self.on_treeWidget_itemExpanded)
        self.treeWidget.itemCollapsed.connect(self.on_treeWidget_itemCollapsed)
        # fix width
        for column in range(0, self.treeWidget.columnCount()):
            self.treeWidget.resizeColumnToContents(column)
        # set current item
        self.treeWidget.setCurrentItem(None)

    def loadData(self):
        self.treeWidget.clear()
        topItemList = []
        childItemList = []
        for task in todoDB.Task.query.all():
            tags = ','.join([t.name for t in task.tags])
            item = QtGui.QTreeWidgetItem([task.text, str(task.date), tags])
            item.task = task
            if task.done:
                item.setCheckState(0, QtCore.Qt.Checked)
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)
            if item.task.parent is None:
                topItemList.append(item)
            else:
                childItemList.append(item)
        for topItem in topItemList:
            for childItem in childItemList:
                if topItem.task.text == childItem.task.parent:
                    topItem.addChild(childItem)
        self.treeWidget.addTopLevelItems(topItemList)
        for i in range(0, self.treeWidget.topLevelItemCount()):
            for item in self.expandItems:
                if self.treeWidget.topLevelItem(i).task.text == item.task.text:
                    self.treeWidget.expandItem(self.treeWidget.topLevelItem(i))

    def on_treeWidget_itemChanged(self, item, column):
        if item.checkState(0):
            item.task.done = True
        else:
            item.task.done = False
        todoDB.saveData()
        for column in range(0, self.treeWidget.columnCount()):
            self.treeWidget.resizeColumnToContents(column)

    def on_treeWidget_currentItemChanged(self, current, previous):
        if current:
            self.deleteAction.setEnabled(True)
        else:
            self.deleteAction.setEnabled(False)

    def on_treeWidget_itemExpanded(self, item):
        self.expandItems.append(item)
        for column in range(0, self.treeWidget.columnCount()):
            self.treeWidget.resizeColumnToContents(column)

    def on_treeWidget_itemCollapsed(self, item):
        self.expandItems.remove(item)

    def new(self):
        topItems = []
        for i in range(0, self.treeWidget.topLevelItemCount()):
            topItems.append(self.treeWidget.topLevelItem(i))
        task = todoDB.Task(text=u"New Task")
        item = QtGui.QTreeWidgetItem([task.text, str(task.date), ""])
        item.setCheckState(0, QtCore.Qt.Unchecked)
        item.task = task
        self.treeWidget.addTopLevelItem(item)
        self.treeWidget.setCurrentItem(item)
        todoDB.saveData()
        self.editor.edit(item, topItems)

    def edit(self):
        selectedItem = self.treeWidget.currentItem()
        if not selectedItem:
            return
        topItems = []
        for i in range(0, self.treeWidget.topLevelItemCount()):
            topItems.append(self.treeWidget.topLevelItem(i))
        self.editor.edit(selectedItem, topItems)

    def delete(self):
        selectedItem = self.treeWidget.currentItem()
        if not selectedItem:
            return
        reply = QtGui.QMessageBox.question(self,
                                   'Confirmation',
                                   "Are you sure to delete?",
                                   QtGui.QMessageBox.Yes |
                                   QtGui.QMessageBox.No,
                                   QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            for i in range(0, selectedItem.childCount()):
                selectedItem.child(i).task.delete()
            selectedItem.task.delete()
            todoDB.saveData()
            self.treeWidget.takeTopLevelItem(
                self.treeWidget.indexOfTopLevelItem(selectedItem))

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

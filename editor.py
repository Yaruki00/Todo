from PyQt4 import QtCore, QtGui
import todoDB
import os, sys
from datetime import datetime

class Editor(QtGui.QWidget):
    def __init__(self, parent, task=None):
        super(Editor, self).__init__()
        self.setGeometry(0, 0, 345, 270)
        self.parent = parent
        vbox = QtGui.QVBoxLayout()
        form = QtGui.QFormLayout()
        # form components
        self.taskLabel = QtGui.QLabel('&Task:')
        self.taskLineEdit = QtGui.QLineEdit()
        self.taskLabel.setBuddy(self.taskLineEdit)
        self.parentCheck = QtGui.QCheckBox('&have parent')
        self.parentCheck.stateChanged.connect(self.parentCheckChanged)
        self.parentLabel = QtGui.QLabel('&Parent:')
        self.selectParent = QtGui.QComboBox()
        self.parentLabel.setBuddy(self.selectParent)
        self.doneCheck = QtGui.QCheckBox('&Finished')
        self.dateLabel = QtGui.QLabel('&Due Date:')
        self.dateTimeEdit = QtGui.QDateTimeEdit()
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateLabel.setBuddy(self.dateTimeEdit)
        self.tagLabel = QtGui.QLabel('&Tag:')
        self.tagLineEdit = QtGui.QLineEdit()
        self.tagLabel.setBuddy(self.tagLineEdit)
        self.ok = QtGui.QPushButton('ok')
        self.ok.clicked.connect(self.save)
        self.canb = QtGui.QPushButton('calcel')
        self.canb.clicked.connect(self.cancel)
        # add components to form
        form.addRow(self.taskLabel, self.taskLineEdit)
        form.addRow(None, self.doneCheck)
        form.addRow(None, self.parentCheck)
        form.addRow(self.parentLabel, self.selectParent)
        form.addRow(self.dateLabel, self.dateTimeEdit)
        form.addRow(self.tagLabel, self.tagLineEdit)
        form.addRow(self.ok, self.canb)
        vbox.addLayout(form)
        self.setLayout(vbox)
        # define tab order
        self.setTabOrder(self.taskLabel, self.doneCheck)
        self.setTabOrder(self.doneCheck, self.dateLabel)
        self.setTabOrder(self.dateLabel, self.tagLabel)
        self.setTabOrder(self.tagLabel, self.ok)
        self.setTabOrder(self.ok, self.canb)
        # init item
        self.item = None
        # init mode
        self.new = False
        # hide
        self.hide()

    def parentCheckChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.selectParent.setEnabled(True)
        else:
            self.selectParent.setEnabled(False)

    def edit(self, item, topItems, new=False):
        self.new = new
        self.item = item
        self.taskLineEdit.setText(self.item.task.text)
        self.doneCheck.setCheckState(self.item.task.done)
        self.selectParent.clear()
        for topItem in topItems:
            self.selectParent.addItem(topItem.task.text)
        if item.task.parent:
            self.parentCheck.setCheckState(QtCore.Qt.Checked)
            for i in range(0, len(topItems)):
                if topItems[i].task.text == item.task.parent:
                    self.selectParent.setCurrentIndex(i)
        else:
            self.selectParent.setEnabled(False)
            self.parentCheck.setCheckState(QtCore.Qt.Unchecked)
        dt = self.item.task.date
        if dt:
            self.dateTimeEdit.setDate(QtCore.QDate(dt.year, dt.month, dt.day))
            self.dateTimeEdit.setTime(QtCore.QTime(dt.hour, dt.minute))
        else:
            self.dateTimeEdit.setDateTime(QtCore.QDateTime())
        self.tagLineEdit.setText(','.join(t.name for t in self.item.task.tags))
        self.show()

    def save(self):
        if self.item == None:
            return
        d = self.dateTimeEdit.date()
        t = self.dateTimeEdit.time()
        self.item.task.date = datetime(
            d.year(),
            d.month(),
            d.day(),
            t.hour(),
            t.minute()
        )
        self.item.task.text = unicode(self.taskLineEdit.text())
        if self.doneCheck.checkState() == QtCore.Qt.Checked:
            self.item.task.done = True
        else:
            self.item.task.done = False
        if self.parentCheck.checkState() == QtCore.Qt.Checked:
            self.item.task.parent = self.selectParent.currentText().__str__()
        tags = [s.strip() for s in unicode(self.tagLineEdit.text()).split(',')]
        self.item.task.tags = []
        for tag in tags:
            dbTag = todoDB.Tag.get_by(name = tag)
            if dbTag is None:
                self.item.task.tags.append(todoDB.Tag(name=tag))
            else:
                self.item.task.tags.append(dbTag)
        self.item.setText(0, self.item.task.text)
        self.item.setText(1, str(self.item.task.date))
        self.item.setText(2, u','.join(t.name for t in self.item.task.tags))
        self.item.setCheckState(0, self.doneCheck.checkState())
        todoDB.saveData()
        self.hide()
        self.parent.loadData()

    def cancel(self):
        if self.new:
            self.item.task.delete()
            todoDB.saveData()
        self.hide()
        self.parent.loadData()

def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    editor = Editor(window)
    window.setCentralWidget(editor)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

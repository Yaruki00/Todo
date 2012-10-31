from PyQt4 import QtCore, QtGui
import todoDB
import os, sys

class Editor(QtGui.QWidget):
    def __init__(self, parent, task=None):
        super(Editor, self).__init__()
        self.setGeometry(0, 0, 345, 270)
        vbox = QtGui.QVBoxLayout()
        form = QtGui.QFormLayout()
        # form components
        self.taskLabel = QtGui.QLabel('&Task:')
        self.taskLineEdit = QtGui.QLineEdit()
        self.taskLabel.setBuddy(self.taskLineEdit)
        self.doneCheck = QtGui.QCheckBox('&Finished')
        self.dateLabel = QtGui.QLabel('&Due Date:')
        self.dateTimeEdit = QtGui.QDateTimeEdit()
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateLabel.setBuddy(self.dateTimeEdit)
        self.tagLabel = QtGui.QLabel('&Task:')
        self.tagLineEdit = QtGui.QLineEdit()
        self.tagLabel.setBuddy(self.tagLineEdit)
        # add components to form
        form.addRow(self.taskLabel, self.taskLineEdit)
        form.addRow(None, self.doneCheck)
        form.addRow(self.dateLabel, self.dateTimeEdit)
        form.addRow(self.tagLabel, self.tagLineEdit)
        vbox.addLayout(form)
        self.setLayout(vbox)
        # define tab order
        self.setTabOrder(self.taskLabel, self.doneCheck)
        self.setTabOrder(self.doneCheck, self.dateLabel)
        self.setTabOrder(self.dateLabel, self.tagLabel)
        self.setTabOrder(self.tagLabel, self.taskLabel)
        # init item
        self.item = None

    def edit(self, item):
        self.item = item
        self.taskLineEdit.setText(self.item.task.text)
        self.doneCheck.setChecked(self.item.task.done)
        dt = self.item.task.date
        if dt:
            self.dateTimeEdit.setDate(QtCore.QDate(dt.year, dt.month, dt.day))
            self.dateTimeEdit.setTime(QtCore.QTime(dt.hour, dt.minute))
        else:
            self.dateTimeEdit.setDateTime(QtCore.QTime())
        self.tagLineEdit.setText(','.join(t.name for t in self.item.task.tags))
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    editor = Editor(window)
    window.setCentralWidget(editor)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

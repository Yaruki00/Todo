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
        taskLabel = QtGui.QLabel('&Task:')
        taskLineEdit = QtGui.QLineEdit()
        taskLabel.setBuddy(taskLineEdit)
        doneCheck = QtGui.QCheckBox('&Finished')
        dateLabel = QtGui.QLabel('&Due Date:')
        dateTimeEdit = QtGui.QDateTimeEdit()
        dateTimeEdit.setCalendarPopup(True)
        dateLabel.setBuddy(dateTimeEdit)
        tagLabel = QtGui.QLabel('&Task:')
        tagLineEdit = QtGui.QLineEdit()
        tagLabel.setBuddy(tagLineEdit)
        # add components to form
        form.addRow(taskLabel, taskLineEdit)
        form.addRow(None, doneCheck)
        form.addRow(dateLabel, dateTimeEdit)
        form.addRow(tagLabel, tagLineEdit)
        vbox.addLayout(form)
        self.setLayout(vbox)
        # define tab order
        self.setTabOrder(taskLabel, doneCheck)
        self.setTabOrder(doneCheck, dateLabel)
        self.setTabOrder(dateLabel, tagLabel)
        self.setTabOrder(tagLabel, taskLabel)

def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    editor = Editor(window)
    window.setCentralWidget(editor)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

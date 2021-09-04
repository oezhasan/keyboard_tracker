from PyQt5.QtWidgets import QSystemTrayIcon, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QApplication
from PyQt5 import QtWidgets, QtGui
import sqlite3
import sys


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self,icon,parent)
        self.setToolTip("Keyboard Tracker")
        menu = QtWidgets.QMenu(parent)

        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            try:
                self.window = KeyboardTrackerWindow()
                self.window.show()
            except Exception as e:
                print(e)


class KeyboardTrackerWindow(QMainWindow):
    def __init__(self, parent=None):
        super(KeyboardTrackerWindow, self).__init__(parent)
        self.resize(1200,800)
        self.setWindowTitle("KEYBOARD TRACKER")

        widget = QWidget()
        layout = QVBoxLayout()

        db_list = get_db_list()
        for list in db_list:
            label = QLabel(f"Button: {list[0]}, Counter: {list[1]}")
            layout.addWidget(label)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        app.aboutToQuit.connect(self.closeEvent)


    def closeEvent(self, event):
        self.hide()
        print ("User has clicked the red x on the main window")


def get_db_list():
    conn = sqlite3.connect('keyboard_counter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM keyboard_counter")
    return c.fetchall()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.ico"))
    tray_icon.show()
    sys.exit(app.exec_())

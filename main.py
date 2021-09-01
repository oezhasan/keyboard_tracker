from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QSystemTrayIcon, QMainWindow, QVBoxLayout, QLabel, QPushButton
from PySide2.QtWidgets import QApplication, QWidget
from pynput import keyboard
import os
import sys
from PyQt5 import QtGui, QtCore
import sqlite3

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self,icon,parent)
        self.setToolTip("Keyboard Tracker")
        menu = QtWidgets.QMenu(parent)

        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.window = Keyboard_Tracker_Window()
            self.window.show()


class Keyboard_Tracker_Window(QMainWindow):
    def __init__(self, parent=None):
        super(Keyboard_Tracker_Window, self).__init__(parent)
        self.resize(1200,800)
        self.setWindowTitle("KEYBOARD TRACKER")

        widget = QWidget()
        layout = QVBoxLayout()

        db_list = get_db_list()
        #for list in db_list:
        #    label = QLabel(f"Button: {list[0]}, Counter: {list[1]}")
        #    layout.addWidget(label)

        label = QLabel("HALLLLO")
        layout.addWidget(label)
        button1 = QPushButton("Button 1")
        layout.addWidget(button1)
        widget.setLayout(layout)

        self.setCentralWidget(widget)





def db(command):
    conn = sqlite3.connect('keyboard_counter.db')
    c = conn.cursor()
    if command == "create":
        c.execute("CREATE TABLE keyboard_counter (key text, counter integer)")
    elif command == "clear":
        c.execute("DELETE FROM keyboard_counter")
    else:
        pass
    conn.commit()
    conn.close()



def key_listener():
    listener = keyboard.Listener(on_release=on_release)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys

def on_release(key):
    try:
        k = key.char
    except:
        k = key.name

    try:
        print(k)
        track_key(k.lower())
    except Exception as e:
        print(e)

def keyboard_representation(k):
    pass

def get_db_list():
    conn = sqlite3.connect('keyboard_counter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM keyboard_counter")
    return c.fetchall()


def track_key(key):
    conn = sqlite3.connect('keyboard_counter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM keyboard_counter WHERE key=?", [key])
    if c.fetchall():
        c.execute("UPDATE keyboard_counter SET counter = counter + 1 WHERE  key=?", [key])
    else:
        c.execute("INSERT INTO keyboard_counter VALUES (?, 1)", [key])

    conn.commit()

    c.execute("SELECT * FROM keyboard_counter")
    print(c.fetchall())
    conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.ico"))
    tray_icon.show()
    app.exec_()

    #db("clear") #create, clear
    #key_listener()









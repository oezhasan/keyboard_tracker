from pynput import keyboard
import os
import sys
import sqlite3

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

    #db("clear") #create, clear
    key_listener()








